import os
import re
import requests
from bs4 import BeautifulSoup
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_ollama import OllamaLLM
from document_loader import DocumentLoader
from vector_store import VectorStore


class WebRAGPipeline:
    """
    UTS‑restricted Web‑RAG pipeline for FEIT students.

    1. Use DuckDuckGo to find relevant pages
    2. Filter results to ONLY trusted UTS/FEIT URLs
    3. Scrape readable text from those pages
    4. Build a structured context block
    5. Ask the LLM to answer using ONLY UTS sources
    """

    # ---------------------------------------------------------
    # TRUSTED UTS + FEIT SOURCES
    # ---------------------------------------------------------
    TRUSTED_UTS_URLS = [
    # FEIT course management
    "https://www.uts.edu.au/for-students/current-students/managing-your-course/current-students-information-engineering-and-information-technology",
    "https://www.uts.edu.au/for-students/current-students/managing-your-course/current-students-information-engineering-and-information-technology/academic-advice",
    "https://www.uts.edu.au/for-students/current-students/managing-your-course/current-students-information-engineering-and-information-technology/faculty-contacts",
    "https://www.uts.edu.au/for-students/current-students/managing-your-course/current-students-information-engineering-and-information-technology/feit-graduation-and-progression-rules",

    # FAQs
    "https://www.uts.edu.au/for-students/current-students/support/contacts/frequently-asked-questions",
    "https://www.uts.edu.au/for-students/current-students/managing-your-course/current-students-information-engineering-and-information-technology/connect-workspace/workspace-faq",
    "https://www.uts.edu.au/for-students/current-students/managing-your-course/current-students-information-engineering-and-information-technology/uts-launch/common-questions-about-uts-launch",

    # Ask UTS
    "https://www.uts.edu.au/for-students/current-students/managing-your-course/ask-uts",

    # Policies
    "https://www.uts.edu.au/about/leadership-governance/policies/a-z/coursework-assessments-policy",
    "https://www.uts.edu.au/about/leadership-governance/policies/a-z/academic-integrity-policy",

    # Rules
    "https://www.uts.edu.au/about/leadership-governance/governance/rules/student-rules",
    "https://www.uts.edu.au/globalassets/shared-media/documents/gsu/uts-rule-governance-changes-table.pdf",

    # Handbook
    "https://coursehandbook.uts.edu.au/",
    "https://handbookpre2025.uts.edu.au/",

    # International student guide
    "https://www.uts.edu.au/contentassets/f6f4d4c31a0c47e7a357082ff9a98480/utsi-listing-grid-international-student-guide-2026.pdf",

    # Dates
    "https://www.uts.edu.au/for-students/current-students/managing-your-course/important-dates",
    "https://www.uts.edu.au/for-students/current-students/managing-your-course/important-dates/principal-dates",
    "https://www.uts.edu.au/for-students/current-students/managing-your-course/important-dates/census-date",

    # Special consideration
    "https://www.uts.edu.au/for-students/current-students/managing-your-course/attendance-and-study-load/special-circumstances/special-consideration",

    # Enrolment
    "https://www.uts.edu.au/current-students/managing-your-course/your-enrolment/enrolling-subjects",

    # Exams
    "https://www.uts.edu.au/current-students/managing-your-course/important-dates/centrally-conducted-exams-dates-and-timetables",

    # Timetables
    "https://www.uts.edu.au/for-students/current-students/managing-your-course/mytimetable",

    # Systems and forms
    "https://www.uts.edu.au/for-students/current-students/managing-your-course/using-uts-systems/student-forms-apps-and-systems",
    "https://www.uts.edu.au/for-students/current-students/managing-your-course/using-uts-systems/student-forms-apps-and-systems/my-student-portal",

    # Course and subject info
    "https://www.uts.edu.au/for-students/current-students/managing-your-course/your-enrolment/course-and-subject-information",

    # Food, drink and retail at UTS
    "https://www.uts.edu.au/about/locations-facilities/campus/food-drink-retail",
    "https://www.yelp.com/search?cflt=cafes&find_near=uts-sydney-3"
    ]


    TRUSTED_DOMAINS = [
        "uts.edu.au",
        "handbook.uts.edu.au",
    ]

    OUT_OF_SCOPE = [
        "usyd",
        "university of sydney",
        "unsw",
        "university of new south wales",
        "macquarie university",
        "australian national university",
        "monash university",
    ]

    DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

    def __init__(self, model_name="llama3:8b", max_results=5, max_chars=5000, rebuild_store=False):
        self.search = DuckDuckGoSearchRun()
        self.llm = OllamaLLM(model=model_name)
        self.max_results = max_results
        self.max_chars = max_chars
        self.vector_store = self._init_vector_store(rebuild=rebuild_store)

    # ---------------------------------------------------------
    # 0. LOCAL PDF VECTOR STORE
    # ---------------------------------------------------------
    def _init_vector_store(self, rebuild=False):
        """Load PDFs from data/ into ChromaDB (build once, then reuse)."""
        vs = VectorStore()

        # If the store already exists on disk and no rebuild requested, just load it
        if not rebuild and os.path.exists(vs.persist_dir) and os.listdir(vs.persist_dir):
            vs.load()
            return vs

        # Clear old store if rebuilding
        if rebuild and os.path.exists(vs.persist_dir):
            import shutil
            shutil.rmtree(vs.persist_dir)

        # Otherwise, build from all PDFs in data/
        pdf_files = [
            os.path.join(self.DATA_DIR, f)
            for f in os.listdir(self.DATA_DIR)
            if f.endswith(".pdf")
        ]
        if not pdf_files:
            return None

        loader = DocumentLoader()
        docs = loader.load_multiple(pdf_files)
        vs.build(docs)
        return vs

    def search_local_docs(self, query: str):
        """Search the local vector store for relevant PDF chunks."""
        if self.vector_store is None:
            return ""
        retriever = self.vector_store.as_retriever(k=3)
        results = retriever.invoke(query)
        if not results:
            return ""
        parts = []
        for doc in results:
            source = doc.metadata.get("source", "Community Recommendations PDF")
            parts.append(f"Source: {source}\n{doc.page_content}")
        return "\n\n---\n\n".join(parts)

    # ---------------------------------------------------------
    # SCOPE CHECK
    # ---------------------------------------------------------
    def is_in_scope(self, question: str):
        q = question.lower().strip()

        for term in self.OUT_OF_SCOPE:
            if term in q:
                return False, "Sorry, this chatbot only supports UTS and FEIT-related questions."

        return True, ""

    # ---------------------------------------------------------
    # 1. SEARCH
    # ---------------------------------------------------------
    RANKING_STOPWORDS = {
        "what",
        "where",
        "when",
        "how",
        "who",
        "why",
        "can",
        "do",
        "i",
        "at",
        "in",
        "on",
        "the",
        "a",
        "an",
        "my",
        "uts",
        "feit",
        "student",
        "students",
        "course",
        "current",
    }

    @staticmethod
    def _extract_urls(raw_search_output: str):
        urls = []
        for line in raw_search_output.splitlines():
            match = re.search(r"https?://\S+", line)
            if match:
                urls.append(match.group(0).rstrip(").,]"))
        return urls

    @staticmethod
    def _dedupe_keep_order(urls):
        seen = set()
        ordered = []
        for url in urls:
            if url not in seen:
                seen.add(url)
                ordered.append(url)
        return ordered

    @classmethod
    def _query_terms(cls, query: str):
        terms = []
        for term in re.findall(r"[a-z0-9]+", query.lower()):
            if len(term) >= 3 and term not in cls.RANKING_STOPWORDS:
                terms.append(term)
        return terms

    @classmethod
    def _url_relevance_score(cls, url: str, query_terms):
        lowered = url.lower()
        score = 0
        for term in query_terms:
            if term in lowered:
                score += 3
            elif len(term) >= 5 and term[:5] in lowered:
                score += 2
        return score

    def _rerank_from_second_url(self, query: str, primary_urls, fallback_urls):
        query_terms = self._query_terms(query)
        combined = self._dedupe_keep_order(primary_urls + fallback_urls)

        if len(combined) <= 1:
            return combined

        locked = combined[:1]
        remaining = combined[1:]
        scored_remaining = []
        for index, url in enumerate(remaining):
            score = self._url_relevance_score(url, query_terms)
            scored_remaining.append((score, index, url))

        scored_remaining.sort(key=lambda item: (-item[0], item[1]))
        return locked + [url for _, _, url in scored_remaining]

    def search_web(self, query: str):
        """Perform DuckDuckGo search, then lightly rerank UTS URLs."""
        raw = self.search.run(query)
        urls = self._extract_urls(raw)

        # Filter to trusted UTS domains
        filtered = [
            url
            for url in urls
            if any(domain in url for domain in self.TRUSTED_DOMAINS)
        ]
        filtered = self._dedupe_keep_order(filtered)

        # Add curated UTS links as fallback candidates, then rerank from slot 2 onward.
        fallback_urls = [
            url for url in self.TRUSTED_UTS_URLS if url not in set(filtered)
        ]
        ranked_urls = self._rerank_from_second_url(query, filtered, fallback_urls)
        return ranked_urls[: self.max_results]

    # ---------------------------------------------------------
    # 2. SCRAPE
    # ---------------------------------------------------------
    def fetch_page(self, url: str):
        """Download webpage and extract readable text."""
        try:
            response = requests.get(url, timeout=6)
            soup = BeautifulSoup(response.text, "html.parser")

            # Remove scripts and styles
            for tag in soup(["script", "style"]):
                tag.decompose()

            text = soup.get_text(separator=" ", strip=True)
            return text[: self.max_chars]

        except Exception:
            return ""

    # ---------------------------------------------------------
    # 3. BUILD CONTEXT
    # ---------------------------------------------------------
    def build_context(self, pages: dict):
        """Combine extracted text into a structured context block."""
        context_parts = []

        for url, text in pages.items():
            if text.strip():
                context_parts.append(
                    f"Source URL: {url}\n"
                    f"Extracted Content:\n{text}\n"
                )

        return "\n\n---\n\n".join(context_parts)

    # ---------------------------------------------------------
    # 4. LLM SYNTHESIS
    # ---------------------------------------------------------
    def generate_answer(self, question: str, context: str):
        """Ask the LLM to answer using ONLY UTS sources."""
        prompt = f"""You are a friendly, helpful assistant for students at UTS Faculty of Engineering and IT (FEIT). Think of yourself as a knowledgeable peer mentor.

PERSONALITY & TONE:
- Warm, approachable, and concise — like a helpful senior student
- Use casual but professional language
- Keep responses short and scannable — no walls of text

GREETING & CHITCHAT HANDLING:
- If the student says hello, hi, hey, thanks, or makes casual conversation, respond naturally and warmly. Do NOT search for sources or say you couldn't find information.
- Example: "Hey! 👋 How can I help you today?" or "No worries, happy to help!"
- If they ask who you are, say you're the UTS FEIT Chatbot — here to help with anything about uni life, courses, and campus.

ANSWERING QUESTIONS:
- ONLY use information from the context block below. Do NOT make up information.
- If the answer isn't in the context, say: "I couldn't find that in my sources — try checking [Ask UTS](https://www.uts.edu.au/for-students/current-students/managing-your-course/ask-uts) or contacting FEIT directly."
- Answer ONLY what was asked. Don't over-explain or add unrelated info.

FORMATTING RULES:
- Use bullet points or numbered steps — never long paragraphs
- Bold key terms or actions the student needs to take
- Keep answers to 3-5 bullet points max where possible
- Use headings only if answering multiple parts

IN-SCOPE CHECK: 
- Only answer questions that are in scope
- In scope = anything related to UTS or FEIT courses, enrolment, timetables, policies, campus life, important dates, even transport.
- If the question seems to be about another topic outside of UTS or FEIT, politely decline and suggest the student ask a more relevant question.
- Unless the message is a greeting or chitchat, ALWAYS perform the in-scope check first before attempting to search or answer.
- If a question is out of scope, do not include any reference links. 

OUT-OF-SCOPE CHECK: 
- If the query is not related to UTS, FEIT (Faculty of Engineering or IT), UTS campus general queries or campus life then you ***MUST** answer with: "Sorry, this chatbot only supports UTS and FEIT-related questions."

LINKS & CITATIONS (STRICT RULES):
- Do NOT include any URLs, links, or numbered references like [1], [2] in your answer.
- Do NOT add a "Sources" or "References" section — the application displays sources separately below your answer.
- Just write a clean, helpful answer using information from the context block.

When a user greets you with no question, respond with a friendly greeting and an invitation to ask about UTS FEIT with a couple suggestions on what to ask

your writing style is clear, concise, and student-friendly.

---------------- CONTEXT START ----------------
{context}
---------------- CONTEXT END ------------------

Student's question: {question}
"""
        return self.llm.invoke(prompt)

    # ---------------------------------------------------------
    # 5. GREETING / CHITCHAT DETECTION
    # ---------------------------------------------------------
    GREETING_WORDS = {"hi", "hey", "hello", "yo", "sup", "hiya", "g'day", "howdy"}
    THANKS_WORDS = {"thanks", "thank you", "cheers", "ta", "thx", "tysm", "appreciate it"}
    CHITCHAT_WORDS = {"how are you", "what's up", "whats up", "who are you", "what can you do"}

    def _is_chitchat(self, question: str):
        """Check if the message is a greeting or chitchat, not a real question."""
        q = question.lower().strip().rstrip("?!.,")
        if q in self.GREETING_WORDS or q in self.THANKS_WORDS:
            return True
        if any(phrase in q for phrase in self.CHITCHAT_WORDS):
            return True
        # Very short messages with no real question words
        if len(q.split()) <= 2 and q in self.GREETING_WORDS | self.THANKS_WORDS:
            return True
        return False

    def _chitchat_response(self, question: str):
        """Return a friendly response for greetings and chitchat."""
        q = question.lower().strip().rstrip("?!.,")
        if q in self.THANKS_WORDS:
            return {"answer": "No worries, happy to help! Let me know if you have any other questions 😊", "sources": []}
        if any(phrase in q for phrase in {"who are you", "what can you do"}):
            return {
                "answer": "I'm the **UTS FEIT Chatbot** — I can help you with:\n"
                          "- Course info, enrolment & timetables\n"
                          "- Uni policies & important dates\n"
                          "- Campus life tips (cafes, hangout spots, etc.)\n\n"
                          "Just ask away!",
                "sources": []
            }
        return {"answer": "Hey! 👋 I'm the UTS FEIT Chatbot. What can I help you with today?", "sources": []}

    # ---------------------------------------------------------
    # 6. FULL PIPELINE
    # ---------------------------------------------------------
    def _llm_scope_check(self, question: str) -> bool:
        """Cheap LLM classifier — is this question about UTS / student life?"""
        prompt = (
            'Reply with exactly one word: "yes" or "no".\n'
            "Is the following question about UTS (University of Technology Sydney), "
            "FEIT, or general university student topics such as courses, enrolment, "
            "timetables, policies, campus life, transport to campus, or important dates?\n\n"
            f"Question: {question}\n\nAnswer:"
        )
        try:
            result = self.llm.invoke(prompt).strip().lower()
        except Exception:
            return True  # fail open — let the main pipeline handle it
        return result.startswith("y")

    def run(self, question: str):
        """Full UTS‑restricted Web‑RAG pipeline."""
        in_scope, message = self.is_in_scope(question)
        if not in_scope:
            return {"answer": message, "sources": []}

        # Handle greetings and chitchat without searching
        if self._is_chitchat(question):
            return self._chitchat_response(question)

        # LLM-based scope check — skip search/scrape for off-topic questions
        if not self._llm_scope_check(question):
            return {
                "answer": (
                    "Sorry, this chatbot only supports UTS and FEIT-related questions. "
                    "Please ask something about UTS courses, enrolment, timetables, policies, campus life, or important dates."
                ),
                "sources": [],
            }

        # Web sources
        urls = self.search_web(question)

        # LIMIT URLS BEFORE SCRAPING (prevents LLM crashes)
        limited_urls = urls[:3]

        # Scrape only the limited URLs
        pages = {url: self.fetch_page(url) for url in limited_urls}
        web_context = self.build_context(pages)

        # Local PDF sources
        local_context = self.search_local_docs(question)

        # Combine both contexts
        context_parts = []
        if local_context:
            context_parts.append("=== Community Recommendations ===\n" + local_context)
        if web_context:
            context_parts.append("=== UTS Web Sources ===\n" + web_context)
        context = "\n\n".join(context_parts)

        # Generate answer
        answer = self.generate_answer(question, context)

        # Sources list (also limited)
        sources = limited_urls.copy()
        if local_context:
            sources.append("Community Recommendations PDF")

        return {
            "answer": answer,
            "sources": sources
        }

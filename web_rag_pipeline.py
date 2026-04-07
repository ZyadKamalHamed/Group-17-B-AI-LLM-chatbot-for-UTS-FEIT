import requests
from bs4 import BeautifulSoup
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_ollama import OllamaLLM


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
        "anu",
        "australian national university",
        "monash university",
        "other university",
        "other organisation",
        "non-uts organisation",
    ]

    def __init__(self, model_name="llama3:latest", max_results=5, max_chars=5000):
        self.search = DuckDuckGoSearchRun()
        self.llm = OllamaLLM(model=model_name)
        self.max_results = max_results
        self.max_chars = max_chars

    # ---------------------------------------------------------
    # SCOPE CHECK
    # ---------------------------------------------------------
    def is_in_scope(self, question: str):
        q = question.lower().strip()

        for term in self.OUT_OF_SCOPE:
            if term in q:
                return False, "Sorry, this chatbot only supports UTS ands FEIT-related questions."

        return True, ""

    # ---------------------------------------------------------
    # 1. SEARCH
    # ---------------------------------------------------------
    def search_web(self, query: str):
        """Perform DuckDuckGo search, then filter to UTS-only URLs."""
        raw = self.search.run(query)
        urls = []

        # Extract URLs from DuckDuckGo text blob
        for line in raw.split("\n"):
            if "http" in line:
                url = line[line.find("http") :].strip()
                urls.append(url)
            if len(urls) >= self.max_results:
                break

        # Filter to trusted UTS domains
        filtered = []
        for url in urls:
            if any(domain in url for domain in self.TRUSTED_DOMAINS):
                filtered.append(url)

        # Add curated UTS links (ensures FEIT relevance)
        for trusted in self.TRUSTED_UTS_URLS:
            if trusted not in filtered:
                filtered.append(trusted)

        return filtered[: self.max_results]

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
        prompt = f"""
You are an academic assistant for students in the UTS Faculty of Engineering and Information Technology (FEIT).
Your role is to provide accurate, grounded answers using ONLY the information found in the context block.

All information in the context comes from trusted UTS sources such as:
- UTS FEIT website
- UTS Handbook
- UTS Study pages
- UTS Current Students pages

You must NOT use outside knowledge. If the answer is not present in the context, respond with:
"I could not find this information in the UTS sources."

When a user greets you with no question, respond with a friendly greeting and an invitation to ask about UTS FEIT with a couple suggestions on what to ask

your writing style is clear, concise, and student-friendly. Always cite the source URLs in your answer.

---------------- CONTEXT START ----------------
{context}
---------------- CONTEXT END ------------------

Question: {question}

Provide a clear, student-friendly answer with citations to the UTS URLs.
"""
        return self.llm.invoke(prompt)

    # ---------------------------------------------------------
    # 5. FULL PIPELINE
    # ---------------------------------------------------------
    def run(self, question: str):
        """Full UTS‑restricted Web‑RAG pipeline."""
        in_scope, message = self.is_in_scope(question)
        if not in_scope:
            return {
                "answer": message,
                "sources": []
            }

        urls = self.search_web(question)
        pages = {url: self.fetch_page(url) for url in urls}
        context = self.build_context(pages)
        answer = self.generate_answer(question, context)

        return {
            "answer": answer,
            "sources": urls
        }
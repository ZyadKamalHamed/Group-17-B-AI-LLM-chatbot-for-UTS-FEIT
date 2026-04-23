# UTS FEIT Chatbot — Plan: Prototype → Finished Product

**Subject:** 41004 Analytics Capstone Project · **Assignment 3 (50% of final mark, 50 marks total)**
**Group:** 17 · **Deadline:** Week 12 — 17 May 2026, 11:59pm (~4 weeks from 20 Apr 2026)
**Deliverables:** ~50-page report (Harvard-referenced PDF) + 10-minute client presentation.

---

## 1. Context

We have a **working RAG prototype**: Streamlit UI → FastAPI → hybrid retriever (DuckDuckGo + UTS domain filter) + local ChromaDB vector store over `Recommendations.pdf` → Llama 3 (local, via Ollama) → structured answer with numbered citations. Scope-guard + chitchat short-circuit are in place.

The assignment is **results-focused** and graded largely on **depth of investigation** and **quality of deployment/reflection** (40% of marks combined). A working prototype is not enough — we need **justified design choices backed by comparisons and measurable evaluation**, then a deployable product and a polished report/pitch.

This plan turns that into concrete workstreams, owners, and checkpoints.

---

## 2. Current State (what already works)

| Component | File | Status |
|---|---|---|
| FastAPI backend | [server.py](server.py) | Works locally on :8000 |
| Streamlit UI | [app.py](app.py) | Works locally, chat + sources |
| RAG orchestrator | [web_rag_pipeline.py](web_rag_pipeline.py) | Hybrid (web + PDF), scope guard, chitchat |
| Vector store | [vector_store.py](vector_store.py) | ChromaDB + nomic-embed-text (save() is no-op — Chroma auto-persists) |
| PDF loader | [document_loader.py](document_loader.py) | PyPDFLoader + RecursiveCharacterTextSplitter (800/150) |
| Trusted UTS corpus | `TRUSTED_UTS_URLS` + `TRUSTED_DOMAINS` | ~25 curated pages |
| Data | [data/Recommendations.pdf](data/Recommendations.pdf) | Community tips ingested |

**Known gaps:** no real tests (existing `test_*.py` are manual scripts with no assertions), no evaluation metrics, Ollama-bound (can't deploy cloud), hard-coded config, no error logging, report/slides not started.

---

## 3. Critical Gaps to Close

1. **Evidence of modelling rigour** (mark-heavy): no comparisons, no eval harness, no measured quality.
2. **Deployability** (mark-heavy): Ollama + ChromaDB local-only → need cloud-hosted LLM + persistent store or managed vector DB.
3. **Report + presentation** (not started): 50 pages, Harvard referenced, aligned to the 10 required sections.
4. **Reproducibility**: env vars, a clean install path, scripts to rebuild the vector store.

---

## 4. Workstreams

### Workstream A — Technical Build-Out (the "modelling" work)

#### A1. LLM comparison (run on a fixed eval set, pick the winner)

Test each against the **same 20-question UTS-FEIT eval set** (see A4). Record: answer faithfulness (0–2), groundedness (0–2), relevance (0–2), latency (ms), cost (AUD / 1k queries), ability to run in cloud deploy.

| Model | Provider | Why test it | Strength | Weakness |
|---|---|---|---|---|
| **Llama 3 8B** | Ollama (local, current baseline) | Already integrated; free | Private, no API cost | Can't deploy on serverless; slower on laptop CPU |
| **Llama 3.1 70B** | Groq API | Large OSS model, extremely fast (500+ tok/s) | Free tier, cloud-friendly, drop-in replacement | Free tier rate-limited |
| **Llama 3.1 8B** | Groq API | Cheap fast small model | Sub-200ms latency | Less nuanced on complex policy questions |
| **GPT-4o mini** | OpenAI | Industry reference point | Strong on instruction-following | Paid; group needs a key |
| **Gemini 2.x Flash** | Google | Free tier available, long context | Cheap, long-context window | Inconsistent citation behaviour |

**Recommendation (tentative, pending eval):** Groq-hosted **Llama 3.1 8B** as primary for deployability + cost, with **GPT-4o mini** as a quality ceiling comparison in the report. We keep **Ollama-Llama3** in the code as an offline fallback (swappable via env var) — this is also defensible from a privacy/reproducibility angle in the report.

**Code change:** Add an `LLMProvider` abstraction in [web_rag_pipeline.py](web_rag_pipeline.py) (or new `llm_provider.py`) so `__init__` accepts `provider="groq"|"ollama"|"openai"` driven by env vars. Reuse existing `generate_answer()` — only the underlying `.invoke()` target changes. `langchain-groq` and `langchain-openai` are drop-ins.

#### A2. Web-fetch / search tool comparison

Current: DuckDuckGo's free text-blob output is noisy and returns ~5 URLs that we then filter. This is a known prototype weakness.

| Tool | Free tier | Structured JSON | UTS domain filter | Freshness | Notes |
|---|---|---|---|---|---|
| **DuckDuckGo** (current) | Unlimited but brittle | No (text blob) | Manual (post-filter) | Medium | Often returns 0 results under rate limiting |
| **Tavily Search** | 1000 free/mo | Yes | `include_domains=["uts.edu.au"]` native | High | Purpose-built for LLM/RAG — cleanest option |
| **Brave Search API** | 2000 free/mo | Yes | Supported via `site:` operator | High | Independent index |
| **Serper (Google)** | 2500 free | Yes | `site:uts.edu.au` operator | Highest | Google results, well-maintained |
| **SerpAPI** | 100 free/mo | Yes | Native filters | Highest | Expensive beyond free tier |
| **Direct sitemap crawl (UTS)** | Free | N/A | Implicit | Low (static) | Pre-index UTS site once → no live search at all |

**Recommendation:** Swap DuckDuckGo → **Tavily** as primary (best RAG ergonomics + free 1k/mo covers the demo). Keep DuckDuckGo as fallback when `TAVILY_API_KEY` is unset. As an **additional improvement**, pre-crawl and embed the `TRUSTED_UTS_URLS` list during vector-store build so the bot can answer without live web calls at all — this is the strongest defence against scraping brittleness and the best story for the "deployment" mark.

#### A3. Embedding model comparison

| Model | Dims | Where | Cost | Quality signal |
|---|---|---|---|---|
| **nomic-embed-text** (current) | 768 | Ollama local | Free | Solid general-purpose |
| **all-MiniLM-L6-v2** | 384 | sentence-transformers (in requirements already) | Free | Faster, smaller — test if quality is acceptable |
| **BGE-small / BGE-base** | 384 / 768 | HuggingFace | Free | Top MTEB scores at small size |
| **OpenAI text-embedding-3-small** | 1536 | OpenAI API | Paid (cheap) | Strong, very easy to swap |

Run the same A4 eval with each embedding model; compare retrieval recall@k and end-to-end answer quality. Keep `nomic-embed-text` as default if it stays within 10% of the best — simpler story.

#### A4. Evaluation harness (this is the main "modelling quality" evidence)

Without this, we can't score well on "Depth of investigation" (10 marks). Build in [evaluation/](evaluation/) (new folder):

1. **Eval set (`evaluation/eval_set.json`)**: 20–30 questions across 5 categories — enrolment, special consideration, important dates, FEIT contacts, campus life. Each entry has: `question`, `expected_source_url`, `must_contain` keywords, `category`, `difficulty`.
2. **Automated scorer (`evaluation/run_eval.py`)**:
   - For each question: run pipeline, capture answer + retrieved sources + latency.
   - Metrics: **retrieval hit rate** (was the gold URL in retrieved sources?), **keyword coverage** (% of `must_contain` hit), **latency p50/p95**, **citation presence** (regex for `[1]` pattern).
3. **LLM-as-judge (`evaluation/llm_judge.py`)**: use GPT-4 to rate each answer 0–2 on faithfulness, relevance, completeness. Record raw JSON.
4. **Human spot-check (10 questions)**: each group member rates the same 10 answers 1–5 on usefulness. This gives a Kappa-style cross-check of the LLM judge — good material for the report.
5. **Output**: CSV + markdown report auto-generated, one row per (model × embedding × retriever) combo. This **is** the modelling section of the report.

Reference frameworks (pick the lightest): [RAGAS](https://docs.ragas.io/) for the standard RAG metrics, or hand-rolled with LLM-as-judge (simpler, no extra dep). Recommendation: **hand-rolled** for transparency in the report.

#### A5. Engineering hygiene

- **Env vars**: move model names, API keys, port to `.env` (python-dotenv). Commit `.env.example`.
- **Structured logging**: replace the silent `except Exception:` in `fetch_page()` with logged warnings.
- **Rebuild script** (`scripts/rebuild_store.py`): one-liner to reingest PDFs, useful for demo.
- **Basic pytest tests**: convert `test_*.py` into real tests with assertions so CI can run them.
- **Dockerfile** (optional but strong for the deployment section): wraps server + app.

---

### Workstream B — Deployment

#### B1. Hosting comparison

| Option | Cost | Ollama-compatible | Persistent disk (Chroma) | Supports Streamlit | Notes |
|---|---|---|---|---|---|
| **Vercel** | Free tier | ❌ No (serverless, cold starts, no GPU) | ❌ No persistent FS | ❌ | Not viable for this stack |
| **Railway** | ~$5/mo | Could run CPU-only but slow | ✅ Volumes | ✅ | Easiest full-app deploy |
| **Render** | Free tier + paid | CPU only | ✅ Disks (paid) | ✅ | Similar to Railway |
| **Fly.io** | Free credits | Possible (CPU) | ✅ Volumes | ✅ | More config, strong free tier |
| **HuggingFace Spaces** | Free | ❌ | Ephemeral | ✅ (Streamlit SDK) | Great for a public demo URL |
| **Streamlit Community Cloud** | Free | ❌ | ❌ | ✅ (native) | Frontend only — needs separate backend |

**Recommended deployment architecture:**

```
   [Streamlit Community Cloud] → [FastAPI on Railway/Fly]
                                      │
                                      ├─► Groq API (LLM)
                                      ├─► Tavily API (search)
                                      └─► ChromaDB on mounted volume
                                          (rebuilt from data/ on boot)
```

This gives a **public URL** for the presentation demo, zero GPU cost, and a clean story: "the LLM is swappable, the index is reproducible from source PDFs, and the whole thing cold-starts in <30s."

#### B2. Fallbacks for the live demo

- Pre-record a 2-minute screen capture of the chatbot answering 5 questions, in case of network/API issues during the presentation.
- Have an Ollama-local version running on one group member's laptop as a backup.

---

### Workstream C — Report (50 pages, Harvard referenced)

Map each required section to our chatbot project. Target page counts are guidance; total ≤50.

| # | Section | Pages | What goes in it (chatbot-specific) |
|---|---|---|---|
| 1 | **Executive Summary** | 1–2 | Problem (FEIT students struggle to navigate fragmented UTS info); solution (grounded RAG chatbot, UTS-only sources); 3 main findings from eval; 3 main recommendations. Write this **last**. |
| 2 | **Problem** | 2–3 | Business problem from A2 (concise), stakeholder = FEIT students + faculty; significance = student experience + call-centre load reduction; success criteria = factual accuracy, UTS-only grounding, response time. |
| 3 | **Data Exploration** | 4–6 | Sources (25+ UTS URLs, `Recommendations.pdf`); preprocessing (HTML scrub, PDF chunking 800/150, embedding); corpus stats (# chunks, avg length, domain distribution); sample chunks. |
| 4 | **Modelling** | 10–15 | **The main evidence section.** Architecture diagram (RAG pipeline); LLM comparison table from A1 with charts; embedding comparison from A3; retriever choices (k, chunk size ablation); prompt engineering evolution (show 3 versions + what changed and why); evaluation methodology (A4) + full results table; LLM-as-judge + human eval agreement. |
| 5 | **Findings** | 3–5 | Which model/embedding/search combo won and **by how much**; failure modes (out-of-scope, stale pages, ambiguous questions); which question categories work best/worst. |
| 6 | **Recommendations** | 2–3 | For UTS: integrate behind SSO, expand to all faculties, add a feedback loop. Ordered by impact × effort. |
| 7 | **Deployment** | 3–4 | Hosting architecture diagram, integration story ("how this plugs into the UTS student portal"), operational concerns (rate limits, content freshness, PII, monitoring), cost estimate per 1000 queries. |
| 8 | **Future Work + Reflection** | 2–3 | Voice interface, multi-lingual (UTS has large international cohort), agentic tool use (book appointments), fine-tuned domain model. Group reflection on lessons learned (matches a marking criterion). |
| 9 | **Difficulties Encountered** | 1–2 | DuckDuckGo reliability; greeting bug + the short-circuit fix; merge conflict; Ollama vs cloud deploy tradeoffs; each **with the solution** (marks reward showing the solve). |
| 10 | **Appendices** | remainder | Full trusted URL list, full prompt, full eval set, extra charts, responsible-AI notes, repo link. |

**Writing conventions:**
- 10/12pt Times or Arial per brief.
- Harvard referencing throughout; set up a Zotero/Mendeley group for shared refs.
- Every figure/table numbered and captioned; referenced inline.
- Executive summary written last; each section has a 1-sentence purpose at the top.

---

### Workstream D — 10-Minute Client Presentation

Tight script, roles assigned:

| Minute | Section | Speaker |
|---|---|---|
| 0:00–1:00 | Hook + problem | 1 |
| 1:00–3:00 | Solution overview + architecture diagram | 1 |
| 3:00–6:00 | **Live demo** (5 prepared questions covering golden-path + edge cases) | 2 |
| 6:00–8:00 | Modelling results — "we tested X, Y won because Z" — 1 chart | 3 |
| 8:00–9:00 | Deployment + recommendations | 3 |
| 9:00–10:00 | Future work + Q&A buffer | 1 |

Practise twice as a group. Have a recorded demo as backup (see B2).

---

## 5. Timeline (20 Apr 2026 → 17 May 2026)

| Week | Dates | Milestones |
|---|---|---|
| **1** | 20–26 Apr | A1 LLM swap (Groq) + env vars wired. A4 eval set drafted (20 questions). A2 Tavily integrated. Report skeleton + Zotero set up. |
| **2** | 27 Apr–3 May | A3 embedding comparison run. Full A4 eval harness produces its first CSV. B1 deploy to Railway (staging URL live). Draft sections 2, 3, 9. |
| **3** | 4–10 May | A4 eval run across all model × embedding combos. Draft sections 4, 5, 6, 7, 8. Presentation slides v1. First internal review. |
| **4** | 11–17 May | Final report edits + Harvard refs audited. Exec summary written. Presentation rehearsed ≥3 times. Backup demo recorded. Submit by 17 May 11:59pm. |

**Hard stop:** feature-freeze by end of Week 3. Week 4 is polish only.

---

## 6. Suggested Division of Labour (3 members)

Rotate ownership so everyone touches each area enough for peer-assessment fairness.

- **Member 1 — Modelling & Eval lead:** A1, A3, A4, Report §4–5, slides 6:00–8:00.
- **Member 2 — Engineering & Deploy lead:** A2, A5, B1, B2, Report §3, §7, §9, demo driver.
- **Member 3 — Report & Presentation lead:** Report §1, §2, §6, §8, §10, Harvard refs, slide deck, rehearsal coord.

All three contribute questions to the A4 eval set and review each other's report sections.

---

## 7. Critical Files to Modify

- [web_rag_pipeline.py](web_rag_pipeline.py) — extract LLM + search behind env-driven providers.
- [vector_store.py](vector_store.py) — add `search_kwargs` tuning hooks for the retrieval ablation.
- [document_loader.py](document_loader.py) — add a `load_urls()` path so `TRUSTED_UTS_URLS` can be pre-indexed (reuses existing `WebBaseLoader` logic).
- [server.py](server.py) — read `MODEL_PROVIDER`, `SEARCH_PROVIDER` from env.
- [requirements.txt](requirements.txt) — add `langchain-groq`, `tavily-python`, `python-dotenv`, `pytest`, and pin versions before submission.
- **New:** `evaluation/eval_set.json`, `evaluation/run_eval.py`, `evaluation/llm_judge.py`, `scripts/rebuild_store.py`, `.env.example`, `Dockerfile` (optional).

Reuse, don't rewrite: the `DocumentLoader.load_multiple()` and `VectorStore.build()` plumbing already handles the heavy lifting — the provider swaps and eval harness are additive.

---

## 8. Verification (how we know we're done)

- ✅ `pytest` passes with ≥5 real assertions across loader/store/pipeline.
- ✅ `python evaluation/run_eval.py` produces a CSV with all (model × embedding) combos and a markdown summary.
- ✅ Public staging URL returns a grounded cited answer for all 20 eval questions within 10s p95.
- ✅ `README.md` updated with: setup, env vars, how to rebuild, how to run eval, deployment link.
- ✅ Report PDF compiles, 40–50 pages, Harvard refs resolve, no broken figure refs.
- ✅ Slide deck runs in ≤10 minutes in a clean rehearsal; backup demo video saved.
- ✅ Final commit tagged `submission-v1`.

---

## 9. Risks & Mitigations

| Risk | Mitigation |
|---|---|
| Groq/Tavily rate-limits during demo | Pre-record demo; keep Ollama fallback running locally. |
| Scope creep (voice, SSO, mobile, etc.) | Freeze scope end of Week 1; anything new goes to §8 Future Work. |
| Harvard referencing drift | Use Zotero from day 1; one member owns the reference audit in Week 4. |
| Uneven peer contribution | Weekly 30-min sync + shared Trello/GitHub project; commit authorship is the audit trail. |
| LLM-as-judge bias skews eval | Human spot-check on 10 questions as a cross-check; report agreement rate. |

# TrendMate — AI-Powered Fashion E-Commerce Chatbot

> Northeastern University · MPS Analytics Capstone · Spring 2026  
> Team: Divya Chenthamarakshan, Lisa Tran, Laura, Lexin Li, Monika Roy

---

## My Contribution — LLM Integration & Escalation Module

I designed and built the intent classification system, prompt engineering layer, LLM response generator, and escalation handler — the core decision-making layer of TrendMate.

**What I built:**
- `intent_classifier.py` — Weighted keyword classifier covering 12 intent categories (no ML model; rule-based for transparency and speed)
- `prompt_templates.py` — 8 intent-specific prompt templates grounded in the Bitext 26K customer support dataset
- `response_generator.py` — Gemini 2.5 Flash integration with 3-retry backoff, intent-to-prompt routing, and escalation bypass logic
- `chatbot_tester.py` — Testing suite with per-intent accuracy tracking, response time measurement (ms), and failure reporting

> **Note on demo data:** `response_generator.py` uses hardcoded mock products and orders for standalone demo purposes. In the full integrated system, these connect to the team's SQLite database (`products`, `orders`, `query_logs` tables) built by a teammate.

---

## Project Overview

TrendMate is a multi-component AI chatbot for fashion e-commerce that combines semantic search, structured databases, and large language models. It handles product search, order tracking, policy FAQs, and human escalation — all in one unified agent-based architecture.

**The problem:** Traditional rule-based chatbots fail on natural language fashion queries — wrong results, no personalization, no escalation awareness.

**The solution:** A hybrid system using FAISS semantic search, SQLite structured queries, and Gemini-powered natural language responses, coordinated by an intelligent intent classifier.

---

## Architecture

```
User (Streamlit UI)
        │
        ▼
IntentClassifier          ← my module
(12 categories · weighted keyword · confidence 0–1)
        │
        ▼
TrendMateAgent / Escalation Check    ← my module
        │
   ┌────┴──────────────┬──────────────────┐
   ▼                   ▼                  ▼
ProductSearchTool  OrderTrackingTool  PolicyFAQTool
(DB filter + FAISS) (SQLite + regex)  (static, 0 ms)
   │                   │                  │
   └────────────────┬──┘                  │
                    ▼                     │
             Gemini 2.5 Flash  ◄──────────┘     ← my module
        (12 prompt templates · 3-retry backoff)
                    │
                    ▼
          Response + SQLite query_log
```

---

## Key Results

| Metric | Result |
|---|---|
| Intent classification accuracy | 100% (23-query test set, all 12 categories) |
| Escalation detection rate | 100% (39 logged cases) |
| Escalation response time | 0 ms (no LLM call) |
| Total queries logged | 1,205 |
| Queries served by DB directly | 41% (496 / 1,205) |
| Queries routed to Gemini | ~34% (408 / 1,205) |
| Avg Gemini response time | ~10.5s (known limitation; target <500ms) |

**Intent confidence scores (from production logs):**

| Intent | Avg Confidence |
|---|---|
| price_filter / returns / refund / escalation | 1.00 |
| size_guide | 0.98 |
| payment_shipping | 0.99 |
| order_tracking | 0.97 |
| product_search | 0.90 |
| general_faq (catch-all) | 0.53 |

---

## Tech Stack

- **LLM:** Gemini 2.5 Flash (`google.genai.Client`)
- **Intent classification:** Rule-based weighted keyword matching (deterministic, no ML training)
- **Semantic search:** FAISS + Sentence Transformers (`all-MiniLM-L6-v2`, 384-dim embeddings)
- **Database:** SQLite (products, orders, query_logs)
- **Frontend:** Streamlit with custom CSS
- **Dataset:** Bitext Customer Support LLM Chatbot Training Dataset (26,872 examples across 11 categories)

---

## Intent Categories (12)

`product_search` · `price_filter` · `order_tracking` · `order_status` · `returns_exchanges` · `refund_request` · `payment_shipping` · `size_guide` · `account_management` · `contact_info` · `general_faq` · `escalation`

Escalation is assigned `priority=4` and overrides all other intents — it fires first in the pipeline with no LLM call and 0ms latency.

---

## Design Decisions

**Why rule-based over ML for intent classification?**  
Fast, transparent, and cost-effective. Stakeholders can read and modify the classification logic directly. No training data pipeline or model hosting needed. Achieved 100% accuracy on the test set.

**Why does escalation bypass Gemini entirely?**  
Frustrated users need an instant response, not a 10-second LLM call. The escalation handler returns immediately with a human handoff message at 0ms.

**Why 12 separate prompt templates instead of one general prompt?**  
Each intent has a different tone requirement — enthusiastic for product search, professional for order tracking, empathetic for returns. A single generic prompt produced lower-quality responses during testing.

---

## Known Limitations

- Avg Gemini API response time is ~10.5s, well above the <500ms target. Next steps include response caching and prompt length optimization.
- Test set is 23 queries; expanding to 50+ cases is planned.
- Static policy responses are not dynamically updated from a database.
- This module uses mock product/order data for standalone demo. Production version connects to the team's shared SQLite database.

---

## How to Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/lisatran183/trendmate-fashion-chatbot
cd trendmate-fashion-chatbot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your Gemini API key
export GEMINI_API_KEY="your_key_here"

# 4. Run the Streamlit UI
streamlit run ui_demo.py
```
**Streamlit theme config** — create `.streamlit/config.toml` if missing:

```toml
[theme]
primaryColor = "#0f172a"
backgroundColor = "#f7f8ff"
secondaryBackgroundColor = "#ffffff"
textColor = "#0f172a"
font = "sans serif"
```

---

## Requirements

```
streamlit
google-generativeai
datasets
transformers
huggingface-hub
pandas
matplotlib
```

---

## Dataset References

- Bitext. (2024). *Bitext Customer Support LLM Chatbot Training Dataset*. Hugging Face. https://huggingface.co/datasets/bitext/Bitext-customer-support-llm-chatbot-training-dataset
- Bansal, S. (2021). *Fashion Clothing Products Dataset*. Kaggle. https://www.kaggle.com/datasets/shivamb/fashion-clothing-products-catalog

---

## Team

This repo contains my individual module contribution. The full integrated system was built collaboratively:

| Module | Owner |
|---|---|
| Vector DB & RAG (FAISS, product/policy search) | Divya Chenthamarakshan |
| Agent Orchestrator & intent routing | Lexin Li |
| Structured DB & logging (SQLite schema) | Laura |
| **LLM Integration, prompt design & escalation** | **Lisa Tran** |
| Frontend UI (Streamlit) | Monika Roy |

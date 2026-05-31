# Introduction to LLMs - Hands-on labs

Three short, practical labs for the day. They are deliberately simple and robust:
nothing here needs a GPU, and nothing downloads from Hugging Face (blocked on the
corporate network).

| Lab | What | Install | Risk of breaking |
|-----|------|---------|------------------|
| **Lab 1** | GitHub Copilot in VS Code: structured output, model comparison, AI code audit | none (you already have it) | very low |
| **Lab 2** | A tiny local RAG with Ollama | Ollama + 2 small models | low (tested) |
| **Lab 3** | Prompt injection on Gandalf | none (web) | none |

## Before the session (5 minutes, optional but helpful)

- **Everyone**: confirm GitHub Copilot Chat works in VS Code (Lab 1, Lab 3 fallback).
- **For Lab 2**: install Ollama from https://ollama.com and run:
  ```
  ollama pull nomic-embed-text
  ollama pull llama3.2:3b
  ```
  If you cannot install Ollama in time, no problem: Lab 2 will also be shown as a live
  demo, and you can still do Lab 1 and Lab 3 with zero setup.

## Notes

- No company data in any lab. All sample text (bookings, policies) is fictional.
- The mini-RAG was tested end to end on `llama3.2:3b` + `nomic-embed-text`.
- Labs 1 and 2 take their inspiration from "Hands-On Large Language Models"
  (Alammar & Grootendorst), rebuilt from scratch for a locked-down corporate environment
  (Copilot / Ollama, offline, no Hugging Face).

Each lab folder has its own README. Have fun, and break things on purpose in Lab 3.

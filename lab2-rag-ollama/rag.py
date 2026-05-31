#!/usr/bin/env python3
"""
Lab 2 - A tiny local RAG, 100% on your laptop, no Hugging Face, no GPU.

It uses Ollama (running locally) for BOTH the embeddings and the answer:
  - embeddings : nomic-embed-text   (turns text into vectors)
  - generation : llama3.2:3b        (writes the grounded answer)

Only the Python standard library is used (urllib, json, math) - nothing to pip install.

Run:
    python rag.py "what is the per-day meal allowance in Europe?"

The script: reads the .txt files in docs/, splits them into chunks, embeds them,
finds the chunks closest to your question, and asks the model to answer ONLY
from those chunks. It prints the answer and the sources it used.

Approach inspired by "Hands-On Large Language Models" (ch. 8), rebuilt from
scratch for an Ollama / offline / laptop setup.
"""
import json
import math
import os
import sys
import urllib.request

OLLAMA = os.environ.get("OLLAMA_URL", "http://localhost:11434")
EMBED_MODEL = "nomic-embed-text"
GEN_MODEL = os.environ.get("GEN_MODEL", "llama3.2:3b")
TOP_K = 3
DOCS_DIR = os.path.join(os.path.dirname(__file__), "docs")


def _post(path, payload):
    req = urllib.request.Request(
        OLLAMA + path,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read())
    except urllib.error.URLError:
        sys.exit(
            "\n[!] Cannot reach Ollama at %s.\n"
            "    Start it (it usually runs on its own once installed) and pull the models:\n"
            "      ollama pull nomic-embed-text\n"
            "      ollama pull llama3.2:3b\n" % OLLAMA
        )


def embed(text):
    return _post("/api/embeddings", {"model": EMBED_MODEL, "prompt": text})["embedding"]


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb + 1e-9)


def load_chunks():
    """One chunk per non-empty paragraph in each .txt file under docs/."""
    chunks = []
    for fname in sorted(os.listdir(DOCS_DIR)):
        if not fname.endswith(".txt"):
            continue
        text = open(os.path.join(DOCS_DIR, fname), encoding="utf-8").read()
        for para in text.split("\n\n"):
            para = para.strip()
            if len(para) > 30:
                chunks.append({"source": fname, "text": para})
    return chunks


def main():
    question = " ".join(sys.argv[1:]) or "what is the per-day meal allowance in Europe?"

    print("Indexing docs/ ...")
    chunks = load_chunks()
    for c in chunks:
        c["vec"] = embed(c["text"])
    print("  %d chunks embedded.\n" % len(chunks))

    qvec = embed(question)
    ranked = sorted(chunks, key=lambda c: cosine(qvec, c["vec"]), reverse=True)
    top = ranked[:TOP_K]

    context = "\n\n".join("[%s] %s" % (c["source"], c["text"]) for c in top)
    prompt = (
        "Answer the question using ONLY the context below. "
        "If the answer is not in the context, say you don't know.\n\n"
        "Context:\n%s\n\nQuestion: %s\nAnswer:" % (context, question)
    )

    print("Question:", question)
    print("\nRetrieved chunks (most relevant first):")
    for c in top:
        print("  - %-22s %s" % ("(%s)" % c["source"], c["text"][:70].replace("\n", " ") + "..."))

    out = _post("/api/generate", {"model": GEN_MODEL, "prompt": prompt, "stream": False})
    print("\nAnswer:\n" + out["response"].strip())
    print("\nSources:", ", ".join(sorted({c["source"] for c in top})))


if __name__ == "__main__":
    main()

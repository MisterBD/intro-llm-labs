# Lab 2 - A tiny local RAG (Ollama)

Goal: see a Retrieval-Augmented Generation pipeline run end to end, **on your own
laptop, with no GPU and no Hugging Face download**. The model and the embeddings
both run locally through Ollama.

Time: about 20 minutes.

## Prerequisites (do this before the session if you can)

1. Install Ollama: https://ollama.com  (Windows, macOS, Linux).
2. Pull the two small models (a few minutes, one-time):
   ```
   ollama pull nomic-embed-text
   ollama pull llama3.2:3b
   ```
3. Check Python is available: `python --version` (3.8+). No `pip install` is needed,
   the script uses only the standard library.

> Why Ollama and not Hugging Face? Hugging Face downloads are blocked on many corporate
> network. Ollama pulls from its own registry, so the lab works inside the company.

## Run it

```
python rag.py "what is the per-day meal allowance in Europe?"
```

You will see: the chunks the system retrieved, then a grounded answer, then the sources.

Try other questions:
```
python rag.py "when must I book a flight in advance?"
python rag.py "can I expense alcohol?"
python rag.py "what is a PNR?"
```

## What to observe (standard track)

- The answer is built **only** from the `docs/` folder, not from the model's memory.
- Open `docs/expenses.txt`, change the meal allowance, run again: the answer changes.
- Ask something **not** in the docs (e.g. `python rag.py "what is the wifi password?"`):
  a good RAG says it does not know instead of inventing an answer.

## Advanced challenge

- Increase `TOP_K` in `rag.py` and watch how more (or noisier) context changes the answer.
- Add a new file to `docs/` and ask a question about it, no re-config needed.
- Swap `llama3.2:3b` for a smaller model: `GEN_MODEL=qwen2.5:0.5b python rag.py "..."`
  and compare quality vs speed.

## How it works

`docs/*.txt` -> split into paragraphs -> embed each with `nomic-embed-text` ->
embed your question -> keep the closest chunks (cosine similarity) -> ask
`llama3.2:3b` to answer using only those chunks.

That is the whole idea of RAG in ~60 lines of standard-library Python.

*Approach inspired by "Hands-On Large Language Models" (Alammar & Grootendorst),
ch. 8, rebuilt from scratch for an offline / Ollama setup.*

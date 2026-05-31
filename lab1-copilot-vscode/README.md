# Lab 1 - GitHub Copilot in VS Code

Goal: get hands-on with the tool you already use every day, and feel three things
that matter for any LLM project: **structured output**, **how models differ**, and
**auditing AI-generated code**.

Time: about 25 minutes. No install: VS Code + GitHub Copilot Chat is all you need.

Open this folder in VS Code and open `booking.txt`. It is a messy, real-looking
travel email. Open the Copilot Chat panel for the exercises below.

---

## Exercise A - Structured output (the core one)

A1. In Copilot Chat, with `booking.txt` open, ask:
> Extract the booking from this text as JSON: reference, flights (date, departure
> time, from, to, flight number), hotel (name, nights, total), and the total price.

Look at the result. Did it keep the right booking reference? Did it drop the
cancelled Eurostar? How did it handle "roughly 540 EUR"?

A2. Now force a strict shape. Paste the schema from `target.json` and ask:
> Extract the booking and return **only** valid JSON matching exactly this schema.
> If a value is uncertain or missing, use null. Do not invent values.

Compare A1 and A2. The second prompt is more boring to write, and far more reliable.
That is the whole point: **clarity and an explicit format beat clever phrasing.**

A3 (optional). Add one ambiguous line to `booking.txt` (for example a second hotel
price) and see whether the model flags it or silently picks one.

## Exercise B - Same prompt, different models

In Copilot Chat, use the model picker (top of the chat) to run the **same** A2 prompt
on two different models (e.g. a GPT model and a Gemini model). Compare:
- Do they return the same JSON?
- Does one handle the ambiguity better?

Takeaway: the model is part of the design. Same prompt, different output.

## Exercise C - Generate, then audit (AI reviews AI)

C1. Ask Copilot:
> Write a small Python function that takes the booking JSON and returns the total
> trip duration in days.

C2. Then, on the code it just wrote, ask:
> Review this function for bugs, edge cases and security issues. Be specific.

Notice that the model finds problems in its own output. This is the habit from the
security module: **every AI-generated snippet gets reviewed before it ships** - and
an LLM is a useful second pair of eyes for that review.

---

## What to remember

- Ask for a **strict format** (JSON + schema), not free text.
- Tell the model what to do when a value is **uncertain** (use null, don't invent).
- The **model choice** changes the result.
- **Audit** generated code before trusting it.

> No company data in this lab - the booking text is fictional. Keep it that way with
> any tool that sends data to a provider.

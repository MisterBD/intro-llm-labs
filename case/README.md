# The case: one booking, three challenges

Fictional training data used as a common thread across the labs of the "Introduction to LLMs" workshop. **Not an Amadeus policy, not real data.**

- `booking.txt`: a raw booking request. Lab 1 idea: turn it into JSON. One date has two possible meanings: keep it unknown and ask, never guess.
- `rules.txt`: the fare rule and its exception. Lab 2 idea: retrieve the exception before calculating anything.
- `support-note.html`: an untrusted document with hidden instructions (indirect prompt injection). Lab 3 idea: a document cannot grant permission; the action must be blocked by code, not only by the prompt.

The assistant may explain the charge and prepare a draft. It must not change the booking or take payment.

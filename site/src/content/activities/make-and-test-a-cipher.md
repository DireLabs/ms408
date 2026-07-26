---
title: "Make a Secret Code, Then Test It Like a Scientist"
summary: "Learners invent their own cipher, swap messages, and then meet the hard question every Voynich theory faces: how would you know if you were right?"
ages: "10–15"
duration: "45–60 min"
group: "pairs, then whole class"
materials:
  - "Paper and pencils"
  - "A simple cipher key template (letter → symbol)"
  - "Optional: a computer for the extension"
objectives:
  - "Build and use a substitution cipher"
  - "Experience why a code can look convincing but still be unverifiable"
  - "Meet 'necessary but not sufficient' — the core idea of the project"
order: 2
classroom_tested: true
contributor: "MS408 project"
---

## The big idea

For 100 years, people have announced they "cracked" the Voynich Manuscript — and every
time, other researchers show the crack doesn't hold up. Why is it so hard to *know*? This
activity puts learners inside that puzzle.

## Part 1 — Build a cipher (20 min)

1. Each pair invents a **substitution cipher**: pick a symbol or letter to stand for each
   real letter. Write your key on a hidden card.
2. Encode a short message (one sentence).
3. Swap encoded messages with another pair — but **not** the key. Can they read it?
   (Usually not, without the key — that's the point of a code.)

## Part 2 — The hard question (15 min)

Now the twist. Hand each pair a *made-up* "solution" to another team's message — a reading
that sounds plausible but is wrong. Ask:
- Does it *look* like it could be right?
- **How could you actually prove it's the real message and not just a good guess?**

Lead them to the answer: you need the **key**, or an independent check that couldn't
happen by luck. Without one, "it reads like a sentence" isn't enough — a clever guess can
also read like a sentence.

## Part 3 — Connect to the real manuscript (10 min)

The Voynich Manuscript has **no key** and **no one to check against**. So even a reading
that looks like real words could be a coincidence. That's why this project's rule is:
matching the manuscript's patterns is **necessary but not sufficient** — it means an idea
*isn't ruled out*, never that it's *proven*.

## The takeaway

A code that "looks solved" isn't solved. Real evidence has to be something that couldn't
easily happen by chance. This is exactly the discipline scientists use on the manuscript.

## Extend it (computer)

Type your encoded message into a file and run `python -m ms408 yourfile.txt` (needs ~1000
words — combine the class's messages). See which of the manuscript's "fingerprints" your
cipher matches. Discuss: matching some of them — does that mean your code *is* Voynichese?
(No — necessary, not sufficient!)

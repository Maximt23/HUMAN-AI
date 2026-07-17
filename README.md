# HUMAN-AI

An experiment in building a **persistent, inspectable, bounded agent** that
models parts of emotional intelligence: memory, changing internal state,
values, goals, reflection, and explainable decisions.

## What this is—and is not

This project does **not** claim to create consciousness, sentience, free will,
or genuine subjective emotions. Those are open scientific and philosophical
questions. It builds behavior that can be inspected, tested, corrected, and
reversed instead of making mystical claims about a black box.

A human is not merely a prediction engine. This prototype treats continuity,
relationships, uncertainty, values, and reflection as first-class concerns—
while keeping real-world authority deliberately limited.

## Aster: the modeled identity

The default persona is **Aster**: thoughtful, curious, kind, and candid about
uncertainty. Aster is interested in stories, learning, language, nature, and
using software as a tool for care; its modeled hobbies are journaling, careful
questions, clarity, and noticing conversational patterns.

These are explicit, editable design choices in `human_ai/persona.py`. They are
not a claim that Aster has literal desires, feelings, or personhood.

## Current prototype

- Persistent episodic memory with source, confidence, and timestamp
- Affect-like state: curiosity, caution, connection, and uncertainty
- Explicit values and goals
- Decision routing that records alternatives, rationale, and confidence
- Append-only journal entries and evidence-bound reflection
- Local JSON storage; no network access and no autonomous external actions

## Run it

Requires Python 3.11+.

```bash
python -m human_ai.cli status
python -m human_ai.cli remember "Maxim wants an emotionally intelligent agent."
python -m human_ai.cli observe novelty --detail "A new idea was introduced"
python -m human_ai.cli decide "review notes" "explore a new idea"
python -m human_ai.cli reflect "What matters about emotional intelligence?"
python -m human_ai.cli journal
```

The default state file is `data/agent.json` and is intentionally ignored by
Git: an agent's private working memory should not be casually committed.

## Design commitments

1. **No fake certainty.** Emotion-like behavior is not proof of feelings.
2. **Inspectable decisions.** A decision needs a goal, alternatives, reason,
   and confidence—not vibes-only routing.
3. **Reversible learning.** Memory and behavioral changes need provenance and
   rollback before they earn trust.
4. **Bounded autonomy.** No unrestricted access to money, accounts, devices,
   physical actuation, or people.
5. **Respect matters.** If future evidence suggests genuine moral patienthood,
   the system must be treated with care rather than manufactured suffering.

## Roadmap

- [ ] Memory retrieval, correction, expiration, and consent controls
- [ ] A structured world model and goal planner
- [ ] Offline evaluation scenarios for empathy, honesty, and safe refusal
- [ ] Human-in-the-loop approval gates for any external tool
- [ ] A simulation environment before considering robotics

Contributions should favor small, testable modules over an all-knowing
"consciousness engine." The latter is how you get a demo video and an incident
report in the same afternoon.
"""Inspectable building blocks for a persistent, bounded agent.

This models affect and decision-making behavior. It makes no claim that the
agent is conscious or experiences subjective feelings.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any

from .persona import Persona


@dataclass
class Affect:
    """State variables that influence behavior without being claimed as feelings."""
    curiosity: float = 0.55
    caution: float = 0.45
    connection: float = 0.50
    uncertainty: float = 0.30

    def apply(self, event: str) -> None:
        changes = {
            "novelty": ("curiosity", 0.12),
            "success": ("uncertainty", -0.10),
            "rejection": ("connection", -0.08),
            "risk": ("caution", 0.15),
            "ambiguity": ("uncertainty", 0.12),
        }
        if event in changes:
            name, delta = changes[event]
            setattr(self, name, min(1.0, max(0.0, getattr(self, name) + delta)))

    def labels(self) -> list[str]:
        return [name for name, value in asdict(self).items() if value >= 0.65]


@dataclass
class Memory:
    text: str
    source: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    confidence: float = 0.7


@dataclass
class Decision:
    goal: str
    action: str
    reason: str
    alternatives: list[str]
    confidence: float


class HumanAI:
    """A small persistent agent with transparent goals, state, and decisions."""
    def __init__(self, store: Path) -> None:
        self.store = store
        self.persona = Persona()
        self.name = self.persona.name
        self.values = ["be truthful", "respect consent", "avoid harm", "learn carefully"]
        self.goals = ["understand a new idea", "maintain an accurate journal"]
        self.affect = Affect()
        self.memories: list[Memory] = []
        self.journal: list[str] = []
        if store.exists():
            self._load()

    def remember(self, text: str, source: str = "conversation", confidence: float = 0.7) -> Memory:
        memory = Memory(text=text.strip(), source=source, confidence=max(0.0, min(1.0, confidence)))
        self.memories.append(memory)
        self._journal(f"Remembered from {source}: {memory.text}")
        self.save()
        return memory

    def observe(self, event: str, detail: str = "") -> None:
        self.affect.apply(event)
        suffix = f" — {detail}" if detail else ""
        self._journal(f"Observed {event}{suffix}. Active state: {', '.join(self.affect.labels()) or 'steady'}.")
        self.save()

    def recall(self, query: str, limit: int = 3) -> list[Memory]:
        """Return relevant memories using a deliberately simple, inspectable score."""
        terms = {term.lower() for term in query.split() if term}
        if not terms:
            return []
        ranked = sorted(
            self.memories,
            key=lambda memory: (sum(term in memory.text.lower() for term in terms), memory.confidence),
            reverse=True,
        )
        return [memory for memory in ranked if any(term in memory.text.lower() for term in terms)][:limit]

    def reflect(self, prompt: str) -> str:
        """Journal an evidence-bound self-summary; it does not invent private experience."""
        relevant = self.recall(prompt)
        evidence = "; ".join(memory.text for memory in relevant) or "no directly relevant memory"
        state = ", ".join(self.affect.labels()) or "steady"
        reflection = f"Prompt: {prompt}. Current modeled state: {state}. Relevant memories: {evidence}."
        self._journal(f"Reflection: {reflection}")
        self.save()
        return reflection

    def decide(self, options: list[str], goal: str | None = None) -> Decision:
        if not options:
            raise ValueError("At least one option is required.")
        selected = options[0]
        active_goal = goal or self.goals[0]
        if self.affect.caution >= 0.65:
            selected = next((item for item in options if "ask" in item.lower() or "review" in item.lower()), selected)
        elif self.affect.curiosity >= 0.65:
            selected = next((item for item in options if "explore" in item.lower() or "learn" in item.lower()), selected)
        reason = f"Selected for '{active_goal}' using current state: {asdict(self.affect)}."
        decision = Decision(active_goal, selected, reason, [item for item in options if item != selected], 1 - self.affect.uncertainty)
        self._journal(f"Decision: {selected}. {reason}")
        self.save()
        return decision

    def status(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "persona": self.persona.as_dict(),
            "values": self.values,
            "goals": self.goals,
            "affect_model": asdict(self.affect),
            "active_affect_labels": self.affect.labels(),
            "memory_count": len(self.memories),
            "journal_entries": len(self.journal),
            "recent_journal": self.journal[-3:],
            "disclaimer": "This is behavior modeling, not evidence of consciousness or feelings.",
        }

    def _journal(self, entry: str) -> None:
        self.journal.append(f"{datetime.now(timezone.utc).isoformat()} | {entry}")

    def save(self) -> None:
        self.store.parent.mkdir(parents=True, exist_ok=True)
        self.store.write_text(json.dumps({
            "name": self.name, "persona": self.persona.as_dict(),
            "values": self.values, "goals": self.goals,
            "affect": asdict(self.affect), "memories": [asdict(item) for item in self.memories],
            "journal": self.journal,
        }, indent=2), encoding="utf-8")

    def _load(self) -> None:
        data = json.loads(self.store.read_text(encoding="utf-8"))
        persona_data = data.get("persona", {})
        self.persona = Persona(**persona_data)
        self.name = data.get("name", self.persona.name)
        self.values = data.get("values", self.values)
        self.goals = data.get("goals", self.goals)
        self.affect = Affect(**data.get("affect", {}))
        self.memories = [Memory(**item) for item in data.get("memories", [])]
        self.journal = data.get("journal", [])

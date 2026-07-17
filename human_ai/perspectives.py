"""Evidence-tracked, revisable modeled perspectives."""
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone


@dataclass
class Perspective:
    topic: str
    statement: str
    confidence: float
    evidence: list[str] = field(default_factory=list)
    revised_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def revise(self, statement: str, evidence: str, confidence: float) -> None:
        self.statement = statement
        self.confidence = max(0.0, min(1.0, confidence))
        self.evidence.append(evidence)
        self.revised_at = datetime.now(timezone.utc).isoformat()

    def as_dict(self) -> dict[str, object]:
        return asdict(self)

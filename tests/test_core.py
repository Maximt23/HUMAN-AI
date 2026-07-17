from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from human_ai.core import HumanAI


class HumanAITest(unittest.TestCase):
    def test_memory_persists_and_decision_is_explained(self):
        with TemporaryDirectory() as directory:
            store = Path(directory) / "agent.json"
            agent = HumanAI(store)
            agent.remember("Maxim wants an emotionally intelligent agent.")
            agent.observe("novelty")
            agent.observe("novelty")
            decision = agent.decide(["review notes", "explore a new idea"])

            restored = HumanAI(store)
            self.assertEqual(len(restored.memories), 1)
            self.assertEqual(decision.action, "explore a new idea")
            self.assertIn("current state", decision.reason)

    def test_default_persona_is_persistent_and_inspectable(self):
        with TemporaryDirectory() as directory:
            store = Path(directory) / "agent.json"
            agent = HumanAI(store)
            self.assertEqual(agent.status()["persona"]["name"], "Aster")
            agent.save()
            self.assertEqual(HumanAI(store).status()["persona"]["name"], "Aster")

    def test_perspective_revision_keeps_evidence(self):
        with TemporaryDirectory() as directory:
            store = Path(directory) / "agent.json"
            agent = HumanAI(store)
            agent.revise_perspective("forgiveness", "Repair can matter.", "A literary passage", 0.6)
            revised = agent.revise_perspective("forgiveness", "Repair needs accountability.", "A second passage", 0.8)

            self.assertEqual(revised.confidence, 0.8)
            self.assertEqual(len(revised.evidence), 2)
            self.assertEqual(HumanAI(store).status()["perspectives"][0]["statement"], "Repair needs accountability.")

    def test_reflection_uses_relevant_memory(self):
        with TemporaryDirectory() as directory:
            agent = HumanAI(Path(directory) / "agent.json")
            agent.remember("Maxim values emotional intelligence.")
            agent.remember("The agent should not claim consciousness.")

            reflection = agent.reflect("emotional intelligence")

            self.assertIn("Maxim values emotional intelligence", reflection)
            self.assertNotIn("consciousness", reflection)


if __name__ == "__main__":
    unittest.main()

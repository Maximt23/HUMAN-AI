"""Command-line interface for the Human-AI prototype."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .core import HumanAI


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Human-AI prototype.")
    parser.add_argument("--store", type=Path, default=Path("data/agent.json"))
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("status")
    remember = commands.add_parser("remember")
    remember.add_argument("text")
    remember.add_argument("--source", default="conversation")
    observe = commands.add_parser("observe")
    observe.add_argument("event", choices=["novelty", "success", "rejection", "risk", "ambiguity"])
    observe.add_argument("--detail", default="")
    decide = commands.add_parser("decide")
    decide.add_argument("options", nargs="+")
    decide.add_argument("--goal")
    commands.add_parser("journal")
    reflect = commands.add_parser("reflect")
    reflect.add_argument("prompt")
    args = parser.parse_args()
    agent = HumanAI(args.store)

    if args.command == "status":
        print(json.dumps(agent.status(), indent=2))
    elif args.command == "remember":
        print(json.dumps(agent.remember(args.text, args.source).__dict__, indent=2))
    elif args.command == "observe":
        agent.observe(args.event, args.detail)
        print(json.dumps(agent.status()["affect_model"], indent=2))
    elif args.command == "decide":
        print(json.dumps(agent.decide(args.options, args.goal).__dict__, indent=2))
    elif args.command == "reflect":
        print(agent.reflect(args.prompt))
    else:
        print("\n".join(agent.journal) or "No journal entries yet.")


if __name__ == "__main__":
    main()

# Ohovo Evaloo – Live Agent Evaluation Harness

**Lightweight harness for evaluating AI agents on live or sample issues with consistency and cost-aware scoring.**

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Local-first](https://img.shields.io/badge/local--first-yes-brightgreen.svg)](#)

## What is Ohovo Evaloo?

Ohovo Evaloo (package name: `live-agent-eval`) helps you measure how consistent and effective an agent is on a set of tasks or GitHub-style issues. It focuses on:

- Success rate
- Consistency across multiple runs
- Simple scoring that can later incorporate cost

The core runs completely locally with sample issues so you can test immediately without network access.

## Compatible AI Models & Frameworks

You can evaluate agents powered by:

- Claude, GPT-4o / o-series, Grok, Gemini
- Local models
- Any framework that can produce a structured answer for a given issue (LangGraph, CrewAI, custom loops, etc.)

The harness itself does not call models – you plug in your agent’s output.

## Installation

```bash
pip install -e .
# later: pip install ohovo-evaloo
```

## Quick Start

```python
from live_agent_eval import EvalHarness

harness = EvalHarness()

# Load built-in sample issues (no network needed)
issues = harness.load_sample_issues()

# Simulate or plug in your agent’s answers
for issue in issues:
    # Replace this with a real call to your agent
    agent_answer = "Fixed by adding bounds check" if "pagination" in issue["title"].lower() else "Still investigating"
    result = harness.evaluate_one(issue, agent_answer)
    print(f"Issue: {issue['title']}")
    print(f"  score={result['score']:.2f}  success={result['success']}")
```

## How to Use – User Guide

### 1. Load Issues
```python
issues = harness.load_sample_issues()          # local samples
# later you can add: harness.load_github_issues(repo, labels=...)
```

### 2. Evaluate a Single Answer
```python
result = harness.evaluate_one(issue, agent_output)
# returns score, success flag, consistency helpers
```

### 3. Run Multiple Trials for Consistency
Run the same issue several times and measure how stable the agent’s behavior is. Consistency is often more important than peak performance for production agents.

### 4. Extend with Real Agents
Wrap your agent so it receives the issue description and returns a string (or structured) answer. Feed that answer into `evaluate_one`.

## Why Ohovo Evaloo?

- Instant local testing with sample issues
- Focus on consistency (a frequently missing metric)
- Ready for future paid “live issue packs” and private enterprise suites
- Complements promptfoo, DeepEval, and SWE-bench style tools

## License

Apache-2.0

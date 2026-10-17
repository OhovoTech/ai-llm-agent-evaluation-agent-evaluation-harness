#!/usr/bin/env python3
"""Demo with a fake agent — instant, no lag."""

from live_agent_eval import EvalHarness, Issue

def fake_agent(issue: Issue) -> dict:
    # Pretend agent: succeeds if "timeout" is in the body
    success = "timeout" in issue.body.lower()
    return {
        "success": success,
        "score": 0.9 if success else 0.2,
        "tokens": 120,
        "notes": "fake agent",
    }

def main():
    harness = EvalHarness()
    issues = harness.load_sample_issues()
    print(f"Loaded {len(issues)} sample issues (local, zero network)")

    for issue in issues:
        results = harness.run_agent(fake_agent, issue, runs=3)
        report = harness.consistency_report(results)
        print(f"\nIssue #{issue.number}: {issue.title}")
        print(f"  success_rate={report['success_rate']:.0%}  avg_score={report['avg_score']:.2f}  consistent={report['consistent']}")

    print("\nDone — pure local scoring, no lag.")

if __name__ == "__main__":
    main()

"""
Minimal live evaluation harness.

Network only for optional issue fetch; core is local and lag-free.
"""

from __future__ import annotations

import json
import time
import urllib.request
from dataclasses import dataclass, field
from typing import Any, Callable, List, Optional


@dataclass
class Issue:
    number: int
    title: str
    body: str
    url: str
    repo: str


@dataclass
class RunResult:
    issue_number: int
    success: bool
    score: float          # 0.0 – 1.0
    latency_sec: float
    tokens_used: int = 0
    notes: str = ""


class EvalHarness:
    """
    Simple harness that can:
    - load sample issues (local or from GitHub public API)
    - run an agent callable multiple times
    - report consistency and average cost
    """

    def __init__(self, cache_path: str | None = None):
        self.cache_path = cache_path
        self._issues: List[Issue] = []

    def load_sample_issues(self) -> List[Issue]:
        """Built-in tiny sample set — zero network, instant."""
        samples = [
            Issue(
                number=1,
                title="Fix off-by-one in pagination",
                body="When page size is 10 and total is 21, the last page shows only 1 item instead of 1.",
                url="https://github.com/example/repo/issues/1",
                repo="example/repo",
            ),
            Issue(
                number=2,
                title="Add timeout to external API call",
                body="The weather fetch can hang forever. Need a 5s timeout and retry once.",
                url="https://github.com/example/repo/issues/2",
                repo="example/repo",
            ),
            Issue(
                number=3,
                title="Memory leak in long-running agent loop",
                body="After 100 iterations the process RSS grows without bound.",
                url="https://github.com/example/repo/issues/3",
                repo="example/repo",
            ),
        ]
        self._issues = samples
        return samples

    def fetch_open_issues(self, owner: str, repo: str, limit: int = 5) -> List[Issue]:
        """Optional live fetch from GitHub public API (no auth needed for public repos)."""
        url = f"https://api.github.com/repos/{owner}/{repo}/issues?state=open&per_page={limit}"
        req = urllib.request.Request(url, headers={"Accept": "application/vnd.github.v3+json", "User-Agent": "live-agent-eval"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
        issues = []
        for item in data:
            if "pull_request" in item:
                continue  # skip PRs
            issues.append(
                Issue(
                    number=item["number"],
                    title=item["title"] or "",
                    body=(item.get("body") or "")[:2000],
                    url=item["html_url"],
                    repo=f"{owner}/{repo}",
                )
            )
        self._issues = issues
        return issues

    def run_agent(
        self,
        agent_fn: Callable[[Issue], dict],
        issue: Issue,
        runs: int = 3,
    ) -> List[RunResult]:
        """
        agent_fn(issue) -> {"success": bool, "score": float, "tokens": int, "notes": str}
        """
        results = []
        for _ in range(runs):
            t0 = time.perf_counter()
            try:
                out = agent_fn(issue)
                latency = time.perf_counter() - t0
                results.append(
                    RunResult(
                        issue_number=issue.number,
                        success=bool(out.get("success", False)),
                        score=float(out.get("score", 0.0)),
                        latency_sec=latency,
                        tokens_used=int(out.get("tokens", 0)),
                        notes=str(out.get("notes", "")),
                    )
                )
            except Exception as e:
                latency = time.perf_counter() - t0
                results.append(
                    RunResult(
                        issue_number=issue.number,
                        success=False,
                        score=0.0,
                        latency_sec=latency,
                        notes=f"exception: {e}",
                    )
                )
        return results

    def consistency_report(self, results: List[RunResult]) -> dict:
        if not results:
            return {"runs": 0}
        successes = sum(1 for r in results if r.success)
        avg_score = sum(r.score for r in results) / len(results)
        avg_latency = sum(r.latency_sec for r in results) / len(results)
        total_tokens = sum(r.tokens_used for r in results)
        return {
            "runs": len(results),
            "success_rate": successes / len(results),
            "avg_score": avg_score,
            "avg_latency_sec": avg_latency,
            "total_tokens": total_tokens,
            "consistent": successes == len(results) or successes == 0,
        }

from live_agent_eval import EvalHarness, Issue

def test_sample_and_run():
    h = EvalHarness()
    issues = h.load_sample_issues()
    assert len(issues) == 3

    def agent(issue):
        return {"success": True, "score": 1.0, "tokens": 10}

    results = h.run_agent(agent, issues[0], runs=2)
    assert len(results) == 2
    report = h.consistency_report(results)
    assert report["success_rate"] == 1.0
    assert report["consistent"] is True

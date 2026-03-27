import pytest
from src.logic import calculate_scorecard

def test_perfect_scorecard():
    # Mock data representing a perfect repo
    repo_data = {"stargazers_count": 500, "open_issues_count": 5, "license": {"key": "mit"}}
    contributors = [{"id": i} for i in range(15)]
    commits = [{"sha": i} for i in range(25)]
    ci_runs = [{"conclusion": "success"} for _ in range(10)]

    result = calculate_scorecard(repo_data, contributors, commits, ci_runs)

    assert result.total_score >= 90
    assert result.grade == "A+"
    assert result.metrics[1].name == "Automation"
    assert result.metrics[1].status == "Healthy"

def test_poor_scorecard():
    # Mock data for an empty/inactive repo
    repo_data = {"stargazers_count": 0, "open_issues_count": 200, "license": None}
    contributors = []
    commits = []
    ci_runs = []

    result = calculate_scorecard(repo_data, contributors, commits, ci_runs)

    assert result.total_score < 30
    assert result.grade == "C"
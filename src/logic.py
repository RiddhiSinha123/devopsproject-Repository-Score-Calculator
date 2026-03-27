from pydantic import BaseModel
from typing import List

class Metric(BaseModel):
    name: str
    score: int
    max_score: int
    status: str
    feedback: str

class Scorecard(BaseModel):
    repo_name: str
    total_score: int
    grade: str
    metrics: List[Metric]

def calculate_scorecard(repo_data: dict, contributors: list, commits: list, ci_runs: list) -> Scorecard:
    metrics = []
    
    # --- 1. Community Metric (Max 25) ---
    # We look at stars AND contributor diversity (Bus Factor)
    stars = repo_data.get("stargazers_count", 0)
    contributor_count = len(contributors)
    
    comm_score = 0
    if stars > 100: comm_score += 10
    if contributor_count >= 10: comm_score += 15
    elif contributor_count >= 3: comm_score += 7
    
    metrics.append(Metric(
        name="Community",
        score=comm_score,
        max_score=25,
        status="Healthy" if comm_score >= 15 else "Warning",
        feedback=f"{stars} stars and {contributor_count} contributors found."
    ))

    # --- 2. Automation Metric (Max 25) ---
    # We look at CI presence and recent Success Rate
    auto_score = 0
    if ci_runs:
        success_rate = len([r for r in ci_runs if r.get("conclusion") == "success"]) / len(ci_runs)
        auto_score = int(success_rate * 25)
    
    metrics.append(Metric(
        name="Automation",
        score=auto_score,
        max_score=25,
        status="Healthy" if auto_score >= 20 else "Critical",
        feedback=f"CI Success Rate: {auto_score * 4}% based on recent runs."
    ))

    # --- 3. Activity Metric (Max 25) ---
    # We look at commit frequency in the last 30 days
    commit_count = len(commits)
    act_score = 25 if commit_count >= 20 else 15 if commit_count >= 5 else 5
    
    metrics.append(Metric(
        name="Activity",
        score=act_score,
        max_score=25,
        status="Active" if act_score >= 15 else "Stale",
        feedback=f"{commit_count} commits in the last 30 days."
    ))

    # --- 4. Maintenance Metric (Max 25) ---
    # We check for a License and Issue Backlog
    maint_score = 0
    if repo_data.get("license"): maint_score += 10
    
    open_issues = repo_data.get("open_issues_count", 0)
    if open_issues < 50: maint_score += 15
    elif open_issues < 150: maint_score += 10
    
    metrics.append(Metric(
        name="Maintenance",
        score=maint_score,
        max_score=25,
        status="Healthy" if maint_score >= 20 else "Warning",
        feedback=f"License: {bool(repo_data.get('license'))}, Open Issues: {open_issues}"
    ))

    # --- Final Aggregation ---
    total = sum(m.score for m in metrics)
    
    if total >= 85: grade = "A+"
    elif total >= 70: grade = "A"
    elif total >= 50: grade = "B"
    else: grade = "C"

    return Scorecard(
        repo_name=repo_data.get("full_name", "unknown"),
        total_score=total,
        grade=grade,
        metrics=metrics
    )
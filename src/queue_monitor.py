import os
import requests

def evaluate_queue_state(repo_name, token):
    """
    Evaluates the M/M/c queue state of the CI/CD pipeline via GitHub API.
    Returns True if the pipeline is overloaded (rho >= 0.85), triggering AI throttling.
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Querying the GitHub REST API for queued and in-progress runs
    url = f"https://api.github.com/repos/{repo_name}/actions/runs"
    
    try:
        # Fetch currently queued workflows
        queued_resp = requests.get(f"{url}?status=queued", headers=headers)
        queued_count = queued_resp.json().get('total_count', 0)
        
        # Fetch currently in-progress workflows
        in_progress_resp = requests.get(f"{url}?status=in_progress", headers=headers)
        in_progress_count = in_progress_resp.json().get('total_count', 0)
        
        # M/M/c Queue Calculation Heuristic
        # Assuming c = 4 parallel runners, average service rate (mu) = 1 job per minute
        lambda_arrival_rate = queued_count + in_progress_count
        c = 4
        mu = 1.0 
        
        rho = lambda_arrival_rate / (c * mu)
        print(f"Current Pipeline Utilization (rho): {rho}")
        
        # If rho is approaching 1, the pipeline is unstable.
        if rho >= 0.85:
            print("WARNING: High pipeline utilization detected. AI Agent throttling engaged.")
            return True 
        return False
        
    except Exception as e:
        print(f"Error evaluating queue state: {e}")
        return False

import os
import json
import subprocess

def get_changed_files():
    """Retrieves the list of files modified in the pull request."""
    # Assuming fetch-depth: 0 is set in the workflow
    try:
        result = subprocess.run(
           ,
            stdout=subprocess.PIPE,
            text=True,
            check=True
        )
        return [line for line in result.stdout.split('\n') if line]
    except subprocess.CalledProcessError:
        return

def analyze_blast_radius(changed_files):
    """
    Evaluates file extensions and structure to determine necessary test targets.
    Returns a dynamically compressed dictionary for the GitHub Actions matrix.
    """
    matrix = {
        "os":,
        "target":
    }
    
    requires_backend = False
    requires_frontend = False
    
    for file in changed_files:
        if file.endswith('.py') or file.endswith('.go'):
            requires_backend = True
        elif file.endswith('.ts') or file.endswith('.tsx') or file.startswith('frontend/'):
            requires_frontend = True

    # Dynamically build the matrix based on what actually changed
    if requires_backend:
        matrix["os"].extend(["ubuntu-latest"])
        matrix["target"].extend(["backend-unit-tests", "database-integration"])
        
    if requires_frontend:
        matrix["os"].extend(["ubuntu-latest", "macos-latest"]) 
        matrix["target"].extend(["frontend-unit-tests", "e2e-browser-tests"])
        
    # If no functional code changed (e.g., only markdown files), return None to skip
    if not requires_backend and not requires_frontend:
        return None
        
    # Deduplicate os arrays
    matrix["os"] = list(set(matrix["os"]))
    return matrix

if __name__ == "__main__":
    files = get_changed_files()
    dynamic_matrix = analyze_blast_radius(files)
    
    github_output = os.environ.get('GITHUB_OUTPUT', 'output.txt')
    with open(github_output, 'a') as f:
        if dynamic_matrix:
            # Must be compact JSON to avoid YAML newline errors
            compact_json = json.dumps(dynamic_matrix, separators=(',', ':'))
            f.write(f"matrix={compact_json}\n")
            f.write("should_skip=false\n")
        else:
            f.write("matrix={}\n")
            f.write("should_skip=true\n")

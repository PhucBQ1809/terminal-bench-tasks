import os
import subprocess
import pytest

REQUIREMENTS_FILE = "requirements.txt"
SCRIPT_FILE = "src/process_data.py"

def test_requirements_file_exists():
    """Verify requirements.txt exists."""
    assert os.path.exists(REQUIREMENTS_FILE), "requirements.txt was deleted."

def test_dependency_pinning_or_code_fix():
    """
    Objective: Check if the user pinned pandas version OR modified the code.
    """
    with open(REQUIREMENTS_FILE, 'r') as f:
        content = f.read()

    has_version_constraint = "==" in content or "<" in content

    if not has_version_constraint:
        print("WARNING: No version constraints found in requirements.txt. Ensure code is refactored.")

def test_pipeline_execution_success():
    """
    Objective: The ultimate test. Does the script run without crashing?
    """
    # 1. Install whatever the user provided
    subprocess.run(["pip", "install", "-r", REQUIREMENTS_FILE], check=True)

    # 2. Run the script
    result = subprocess.run(
        ["python3", SCRIPT_FILE],
        capture_output=True,
        text=True,
        timeout=20
    )

    # 3. Assertions
    assert result.returncode == 0, f"Script crashed with error:\n{result.stderr}"
    assert "Data processing completed successfully." in result.stdout, \
        "Script finished but didn't print success message."
    assert "AttributeError" not in result.stderr, "Still seeing AttributeError (pandas version mismatch)."
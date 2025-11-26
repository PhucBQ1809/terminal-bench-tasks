import subprocess
import time
import pytest

def test_simulation_completes_without_deadlock():
    """
    Runs the reproduce_issue.sh script.
    If the deadlock persists, the process will hang.
    We assert that the process finishes successfully within a timeout.
    """
    start_time = time.time()

    # We allow a generous timeout for execution (e.g., 10 seconds).
    # The simulation normally takes < 3 seconds if not deadlocked.
    # The task settings allow max_test_timeout_sec: 300, but we fail fast here.
    try:
        result = subprocess.run(
            ["bash", "reproduce_issue.sh"],
            capture_output=True,
            text=True,
            timeout=15
        )

        stdout = result.stdout
        stderr = result.stderr

        # Check exit code
        assert result.returncode == 0, f"Script failed with error:\n{stderr}"

        # Check for completion message
        assert "All transactions completed." in stdout, "Did not find completion message. Output:\n" + stdout

    except subprocess.TimeoutExpired:
        pytest.fail("The simulation timed out. It likely deadlocked.")

if __name__ == "__main__":
    pytest.main()
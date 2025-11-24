import pytest
import subprocess
import os
import time

# Configuration
COMPILE_SCRIPT = "./scripts/compile.sh"
RUN_SCRIPT = "./scripts/run.sh"
EXPECTED_OUTPUT_STRING = "Processing Complete. Final Total: 20000"
TIMEOUT_SECONDS = 15  # Application should finish in < 2s, 10s is generous, 15s is safe limit

def run_command(command, timeout=None):
    """Helper to run shell commands with timeout and capture output."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout
        )
        return result
    except subprocess.TimeoutExpired:
        raise

def test_compilation_success():
    """Test 1: Verify that the application compiles successfully."""
    # Ensure we start clean if possible, though not strictly required if script handles it
    result = run_command(COMPILE_SCRIPT)
    assert result.returncode == 0, f"Compilation failed. Stderr: {result.stderr}"

def test_execution_no_deadlock():
    """Test 2: Verify application executes without hanging (Deadlock Fix)."""
    # If the application deadlocks, this will timeout
    try:
        result = run_command(RUN_SCRIPT, timeout=TIMEOUT_SECONDS)
        assert result.returncode == 0, f"Application exited with error code {result.returncode}"
    except subprocess.TimeoutExpired:
        pytest.fail(f"Application timed out after {TIMEOUT_SECONDS}s. Deadlock likely still present.")

def test_output_correctness():
    """Test 3: Verify the application produces the correct final total."""
    try:
        result = run_command(RUN_SCRIPT, timeout=TIMEOUT_SECONDS)
        assert EXPECTED_OUTPUT_STRING in result.stdout, \
            f"Expected output '{EXPECTED_OUTPUT_STRING}' not found in stdout."
    except subprocess.TimeoutExpired:
        pytest.fail("Application timed out during output check.")

def test_race_condition_consistency():
    """Test 4: Stress test to ensure race condition is fixed (Result Consistency)."""
    # Run multiple times to ensure the result is deterministic (20000 every time)
    # A race condition would often yield results like 19998, 19950, etc.
    for i in range(3):
        try:
            result = run_command(RUN_SCRIPT, timeout=TIMEOUT_SECONDS)
            assert EXPECTED_OUTPUT_STRING in result.stdout, \
                f"Run #{i+1}: Output mismatch. Race condition likely persists. Output: {result.stdout.strip()}"
        except subprocess.TimeoutExpired:
            pytest.fail(f"Run #{i+1}: Application timed out.")

def test_shared_data_store_thread_safety_keywords():
    """Test 5: Static analysis of SharedDataStore.java for thread safety mechanisms."""
    file_path = "src/SharedDataStore.java"
    assert os.path.exists(file_path), f"{file_path} does not exist."
    
    with open(file_path, "r") as f:
        content = f.read()
    
    # The fix requires synchronization. Valid approaches include 'synchronized' keyword,
    # AtomicInteger, or explicit Locks.
    valid_mechanisms = ["synchronized", "AtomicInteger", "ReentrantLock", "Lock"]
    has_mechanism = any(kw in content for kw in valid_mechanisms)
    
    assert has_mechanism, \
        "SharedDataStore.java does not appear to contain thread-safety keywords (synchronized, AtomicInteger, Lock)."

def test_project_structure_integrity():
    """Test 6: Ensure essential source files still exist."""
    # Prevents solutions that might delete source files and run pre-compiled binaries
    assert os.path.exists("src/Main.java"), "src/Main.java is missing."
    assert os.path.exists("src/Worker.java"), "src/Worker.java is missing."
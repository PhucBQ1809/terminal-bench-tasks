import subprocess
import os

def test_requirements_pinned():
    """Test 1: Check if requirements.txt has pinned versions (==)."""
    with open("requirements.txt", "r") as f:
        content = f.read()

    lines = content.splitlines()
    pandas_pinned = any("pandas==" in line for line in lines)
    assert pandas_pinned, "FAIL: 'pandas' version is not pinned in requirements.txt (e.g., pandas==2.0.3)"

def test_script_execution():
    """Test 2: Run the script and check for success message."""
    result = subprocess.run(
        ["python3", "src/etl_script.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    assert result.returncode == 0, f"Script failed with error: {result.stderr}"
    assert "ETL Process Completed Successfully" in result.stdout, "Success message not found in output."

def test_code_refactored():
    """Test 3: Ensure concat is used."""
    with open("src/etl_script.py", "r") as f:
        code = f.read()

    # FIX: Bỏ check .append() vì list.append() là hợp lệ.
    # Việc check lỗi runtime đã được bao phủ bởi test_script_execution phía trên.
    assert "pd.concat" in code, "FAIL: Code does not appear to use pd.concat()."
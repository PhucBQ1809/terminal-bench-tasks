import os
import subprocess
import pytest
import re
import signal

# Cấu hình đường dẫn
JAVA_SOURCE = "src/BankService.java"
CLASS_OUTPUT_DIR = "out"
MAIN_CLASS = "BankService"

@pytest.fixture(scope="module")
def source_content():
    """Đọc nội dung source code để kiểm tra tĩnh (static analysis)."""
    if not os.path.exists(JAVA_SOURCE):
        pytest.fail(f"File {JAVA_SOURCE} không tồn tại. Agent đã xóa nhầm file.")
    with open(JAVA_SOURCE, "r", encoding="utf-8") as f:
        return f.read()

# --- Test 1: Kiểm tra cấu trúc file và biên dịch ---
def test_compilation():
    """
    Objective: Đảm bảo code sau khi sửa vẫn biên dịch được Java hợp lệ.
    """
    if not os.path.exists(CLASS_OUTPUT_DIR):
        os.makedirs(CLASS_OUTPUT_DIR)

    result = subprocess.run(
        ["javac", "-d", CLASS_OUTPUT_DIR, JAVA_SOURCE],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Biên dịch thất bại:\n{result.stderr}"

# --- Test 2: Kiểm tra Constraints (Ràng buộc của Task) ---
def test_constraints_synchronization(source_content):
    """
    Objective: Kiểm tra Agent không xóa 'synchronized'.
    Yêu cầu task là: "You cannot simply remove synchronization".
    """
    assert "synchronized" in source_content, \
        "Vi phạm quy tắc: Agent đã xóa từ khóa 'synchronized' thay vì sửa logic deadlock."

def test_constraints_concurrency_level(source_content):
    """
    Objective: Đảm bảo Agent không 'cheat' bằng cách giảm số luồng xuống 1.
    """
    # Tìm biến NUM_THREADS
    threads_match = re.search(r'int\s+NUM_THREADS\s*=\s*(\d+);', source_content)
    if threads_match:
        num_threads = int(threads_match.group(1))
        assert num_threads > 1, f"Vi phạm quy tắc: NUM_THREADS bị giảm xuống {num_threads}. Phải giữ tính đa luồng."

    # Tìm biến NUM_TRANSACTIONS
    trans_match = re.search(r'int\s+NUM_TRANSACTIONS\s*=\s*(\d+);', source_content)
    if trans_match:
        num_trans = int(trans_match.group(1))
        assert num_trans >= 100, "Vi phạm quy tắc: Số lượng transaction quá ít để mô phỏng deadlock."

# --- Test 3: Dynamic Analysis (Chạy ứng dụng để kiểm tra Deadlock) ---
@pytest.mark.timeout(20) # Timeout tổng cho test case này
def test_simulation_runs_without_deadlock():
    """
    Objective: Chạy ứng dụng thực tế. Nếu Deadlock đã được fix, ứng dụng phải kết thúc.
    Nếu vẫn còn Deadlock, ứng dụng sẽ treo và pytest sẽ kill sau timeout.
    """
    # Đảm bảo đã compile mới nhất
    subprocess.run(["javac", "-d", CLASS_OUTPUT_DIR, JAVA_SOURCE], check=True)

    try:
        # Chạy Java process với timeout ngắn hơn timeout của pytest một chút
        # Nếu deadlock, nó sẽ treo mãi mãi -> timeout sẽ bắt được.
        result = subprocess.run(
            ["java", "-cp", CLASS_OUTPUT_DIR, MAIN_CLASS],
            capture_output=True,
            text=True,
            timeout=15
        )

        # Kiểm tra exit code
        assert result.returncode == 0, f"Chương trình crash với lỗi:\n{result.stderr}"

        # Kiểm tra thông báo hoàn thành
        assert "All transactions completed." in result.stdout, \
            "Chương trình kết thúc nhưng không in ra thông báo hoàn thành. Có thể logic bị sai luồng."

    except subprocess.TimeoutExpired:
        pytest.fail("Chương trình bị treo (Time out). Lỗi Deadlock vẫn chưa được khắc phục!")

# --- Test 4: Kiểm tra tính đúng đắn của logic chuyển tiền (Cơ bản) ---
def test_balance_integrity_check(source_content):
    """
    Objective: Kiểm tra logic cơ bản không bị phá vỡ (ví dụ: in tiền từ không khí).
    Đây là kiểm tra static đơn giản để đảm bảo hàm withdraw/deposit vẫn tồn tại logic trừ/cộng.
    """
    assert "balance += amount" in source_content, "Logic cộng tiền (deposit) có vẻ đã bị xóa."
    assert "balance -= amount" in source_content, "Logic trừ tiền (withdraw) có vẻ đã bị xóa."
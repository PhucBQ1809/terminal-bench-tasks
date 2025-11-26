#!/bin/bash
# run-tests.sh

# 1. Cài đặt test dependencies tại thời điểm runtime (theo quy định [cite: 36, 54])
# Kiểm tra xem pytest đã có chưa, nếu chưa thì cài (để tránh cài lại nhiều lần nếu chạy local)
if ! command -v pytest &> /dev/null; then
    echo "Installing test dependencies..."
    pip3 install pytest --no-cache-dir
fi

# 2. Tạo thư mục output cho test compilation nếu cần (đảm bảo môi trường sạch)
mkdir -p out

# 3. Chạy bộ test kiểm tra kết quả
# -v: verbose (chi tiết)
# --tb=short: rút gọn traceback lỗi
python3 -m pytest tests/test_outputs.py -v --tb=short
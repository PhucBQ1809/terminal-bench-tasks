#!/bin/bash

if ! python3 -c "import pytest" &> /dev/null; then
    echo "Installing pytest..."
    # Install vào local user directory để không cần root
    pip3 install --user pytest > /dev/null 2>&1
    # Thêm đường dẫn pip user vào PATH nếu cần
    export PATH=$PATH:$HOME/.local/bin
fi

# Đảm bảo script compile/run có quyền thực thi (nếu mount từ host vào)
chmod +x scripts/*.sh

echo "Running Test Suite..."
# Gọi pytest
python3 -m pytest tests/test_outputs.py -v
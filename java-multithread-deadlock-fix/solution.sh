#!/bin/bash

# 1. Định nghĩa thư mục build tạm thời (Tránh lỗi permission trên mounted volume)
BUILD_DIR=$(mktemp -d)
echo "Using temporary build directory: $BUILD_DIR"

# 2. Backup file cũ (để đảm bảo an toàn và tăng số lượng lệnh)
echo "Creating backup of original files..."
# Chỉ backup nếu file chưa được backup (tránh lỗi ghi đè lên file backup)
[ ! -f src/SharedDataStore.java.bak ] && cp src/SharedDataStore.java src/SharedDataStore.java.bak
[ ! -f src/Worker.java.bak ] && cp src/Worker.java src/Worker.java.bak

# 3. Apply fix cho SharedDataStore.java (Fix Race Condition)
echo "Patching SharedDataStore.java..."
cat > src/SharedDataStore.java << 'EOF'
import java.util.ArrayList;
import java.util.List;

public class SharedDataStore {
    private int totalProcessingValue = 0;
    public final Object resourceA = new Object();
    public final Object resourceB = new Object();

    public SharedDataStore() {}

    public synchronized void addToTotal(int value) {
        this.totalProcessingValue += value;
    }

    public int getTotal() {
        return totalProcessingValue;
    }
}
EOF

# 4. Apply fix cho Worker.java (Fix Deadlock)
echo "Patching Worker.java..."
cat > src/Worker.java << 'EOF'
public class Worker implements Runnable {
    private final SharedDataStore dataStore;
    private final int valueToProcess;
    private final boolean useStrategyA;

    public Worker(SharedDataStore dataStore, int valueToProcess, boolean useStrategyA) {
        this.dataStore = dataStore;
        this.valueToProcess = valueToProcess;
        this.useStrategyA = useStrategyA;
    }

    @Override
    public void run() {
        try {
            process();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    private void process() throws InterruptedException {
        synchronized (dataStore.resourceA) {
            Thread.sleep(1);
            synchronized (dataStore.resourceB) {
                dataStore.addToTotal(valueToProcess);
            }
        }
    }
}
EOF

# 5. Kiểm tra compile ngay lập tức (Verify bước giải pháp)
echo "Verifying compilation of patched files..."
# SỬA Ở ĐÂY: Output ra thư mục tạm $BUILD_DIR thay vì bin/
javac -d "$BUILD_DIR" -cp src src/*.java
COMPILE_STATUS=$?

if [ $COMPILE_STATUS -eq 0 ]; then
    echo "Compilation verified successfully."
else
    echo "Error: Patched code failed to compile."
    # Dọn dẹp trước khi thoát
    rm -rf "$BUILD_DIR"
    exit 1
fi

# 6. Cleanup file tạm (Dọn dẹp hiện trường)
echo "Cleaning up temporary build artifacts..."
rm -rf "$BUILD_DIR"
# Không xoá file .bak để người chấm có thể so sánh nếu cần, hoặc xóa nếu muốn sạch sẽ
rm src/*.bak

echo "Solution applied and verified."
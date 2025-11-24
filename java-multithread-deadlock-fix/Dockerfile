FROM eclipse-temurin:17-jdk-jammy

# 1. Cài đặt tools cơ bản VÀ Python3 (để user thường có thể chạy python)
# Cleanup apt cache để giảm size [cite: 42]
RUN apt-get update && apt-get install -y --no-install-recommends \
    vim \
    nano \
    procps \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# 2. Tạo user không phải root (ví dụ: agent) [cite: 44]
RUN useradd -m -s /bin/bash agent

WORKDIR /app

# 3. Chỉ copy source code và scripts, KHÔNG copy solution hay tests
COPY src/ ./src/
COPY scripts/ ./scripts/
COPY config/ ./config/
# Nếu cần file compile/run ở root thì copy riêng, tránh copy solution.sh
# (Giả sử script compile gọi từ root, cần đảm bảo path đúng)

# 4. Cấp quyền cho user agent sở hữu thư mục làm việc
RUN chown -R agent:agent /app

# 5. Đảm bảo script có quyền thực thi
RUN chmod +x scripts/*.sh

# 6. Chuyển sang user thường [cite: 45]
USER agent

# Set default command
CMD ["/bin/bash"]
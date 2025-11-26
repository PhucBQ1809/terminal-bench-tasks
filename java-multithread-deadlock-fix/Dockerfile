# Dockerfile
FROM eclipse-temurin:17-jdk-focal

# Cài đặt Python (cần thiết để chạy script test sau này) nhưng KHÔNG cài thư viện pytest tại đây
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/* [cite: 40]

WORKDIR /app

# Copy source code
COPY . .

# Chỉ cấp quyền thực thi, không chạy solution
RUN chmod +x reproduce_issue.sh run-tests.sh solution.sh
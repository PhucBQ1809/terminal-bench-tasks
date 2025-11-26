# Use a standard lightweight Python image
FROM python:3.9-slim

# Install basic system tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy the task files
COPY . .

# Ensure scripts are executable
RUN chmod +x reproduce_issue.sh run-tests.sh solution.sh
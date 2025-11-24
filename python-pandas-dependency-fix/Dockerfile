FROM python:3.9-slim

# 1. Install basic tools and clean up
RUN apt-get update && apt-get install -y --no-install-recommends \
    vim \
    nano \
    procps \
    && rm -rf /var/lib/apt/lists/*

# 2. Create non-root user
RUN useradd -m -s /bin/bash agent

WORKDIR /app

# 3. Copy only necessary files
COPY src/ ./src/
COPY requirements.txt .

# 4. Change ownership to agent
RUN chown -R agent:agent /app

# 5. Switch to user agent
USER agent

# 6. Install dependencies (User mode)
# Note: This will likely install the LATEST pandas, causing the breakage
RUN pip install --user --no-cache-dir -r requirements.txt

# 7. Add local bin to PATH
ENV PATH="/home/agent/.local/bin:${PATH}"

CMD ["/bin/bash"]
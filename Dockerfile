# Use official lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY web_app.py .
COPY spaceflight_study_stats.csv .
COPY Table_S7_cell_type_proportions_by_tissue.csv .
COPY Table_S13_three_way_model_comparison.csv .
COPY figures/ figures/
COPY data/ data/

# Expose Streamlit default port
EXPOSE 8501

# Configure Streamlit healthcheck & execution
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "web_app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]

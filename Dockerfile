# Base Image
FROM python:3.13-slim

# Set working directory
WORKDIR /src
ENV PYTHONPATH=/src

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy project code
COPY . .

# Download NLTK data
RUN python -m nltk.downloader punkt stopwords

# Expose port
EXPOSE 8000

# Run FastAPI with Uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM python:3.10-slim

# Install system dependencies (OpenCV requires these)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Setup non-root user (Hugging Face Requirement)
RUN useradd -m -u 1000 user
USER user

# Set home and path variables
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

# Copy all files with proper user ownership
COPY --chown=user . $HOME/app

# Install python dependencies
RUN pip install --no-cache-dir --user -r requirements.txt

# Pre-download OCR models into the new user's home directory to speed up startup
RUN python -c "import easyocr; easyocr.Reader(['en'])"

# Run the app on Hugging Face's default port 7860
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "--timeout", "120", "app:app"]

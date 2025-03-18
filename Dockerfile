FROM python:3.10-slim

WORKDIR /app

# Install dependencies first (for better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application
COPY . .

# Install the package
RUN pip install -e .

# Create necessary directories
RUN mkdir -p ~/.gitcompass/logs

# Set the entrypoint to the CLI
ENTRYPOINT ["gitcompass"]

# Default command shows help
CMD ["--help"]

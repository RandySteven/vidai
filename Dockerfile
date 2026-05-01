# ---- Builder stage: install deps in isolation ----
    FROM python:3.11-slim AS builder

    WORKDIR /app
    
    COPY requirements.txt .
    
    RUN pip install --no-cache-dir --prefix=/install -r requirements.txt
    
    
    # ---- Final stage: lean runtime image ----
    FROM python:3.11-slim AS runtime
    
    # Create non-root user for security
    RUN groupadd -r appuser && useradd -r -g appuser appuser
    
    WORKDIR /app
    
    # Copy only installed packages from builder
    COPY --from=builder /install /usr/local
    
    # Copy app source
    COPY --chown=appuser:appuser . .
    
    USER appuser
    
    EXPOSE 8000
    
    CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
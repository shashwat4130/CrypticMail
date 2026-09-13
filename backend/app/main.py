from fastapi import FastAPI

app = FastAPI(
    title="CrypticMail API",
    description="AI-Assisted Cryptographic Security Assessment for Email Communications",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "CrypticMail API",
    }
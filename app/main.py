from fastapi import FastAPI

app = FastAPI(title="abhimart support agent")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
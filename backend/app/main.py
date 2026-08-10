from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root() -> dict[str, str]:
    return {
        "application": "Atanor",
        "status": "running",
    }
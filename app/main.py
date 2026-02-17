from fastapi import FastAPI

app = FastAPI(title="体适能AI管家")

@app.get("/")
def read_root():
    return {"message": "欢迎使用体适能AI管家API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
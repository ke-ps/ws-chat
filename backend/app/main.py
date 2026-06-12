from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "WS Chat API funcionando"}
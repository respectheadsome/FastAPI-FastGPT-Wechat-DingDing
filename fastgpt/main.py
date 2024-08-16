from fastapi import FastAPI
from fastgpt.views import router

app = FastAPI()

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("fastgpt.main:app", host="0.0.0.0", port=8000)

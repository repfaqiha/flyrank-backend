from fastapi import FastAPI, HTTPException

from fastapi.responses import JSONResponse

app = FastAPI()


tasks = [
    {"id": 1, "title": "live", "done": True},
    {"id": 2, "title": "laugh", "done": False},
    {"id": 3, "title": "love", "done": True} ]


@app.get("/")
def root():
    return {"name":"Task API",
     "version": "1.0",
     "endpoints":["/tasks"]}

@app.get("/health")
def health():
    return {"status":"ok"}

@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{id}")
def get_task(id:int):
    for x in tasks:
      if x["id"]==id:
         return x 
    return JSONResponse(
        status_code=404,
        content={"error":f"task {id} not found"}
    )
   
         


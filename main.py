from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field

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
   
class TaskCreate(BaseModel):
    title:str=Field(min_length=1)

@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    print("I RAN")
    tasks.append(
        {"id": tasks[-1]["id"] + 1, "title": task.title, "done": False}
    )
    return tasks[-1]

@app.exception_handler(RequestValidationError)
def validation_error_handler(request:Request, exc:RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"error":"Invalid Request"}
    )

class TaskUpdate(BaseModel):
    title:str | None = Field(default=None, min_length=1)
    done: bool | None=None

@app.put("/tasks/{id}", status_code=200)
def change_task(task: TaskUpdate, id:int):
    for x in tasks:
        if x["id"]==id:
            if task.title is not None:
                x["title"]=task.title
            if task.done is not None:
                x["done"]=task.done
            if task.done is None and task.title is None:
                return JSONResponse(
                    status_code=400,
                    content={"error": "empty request"}
                )
            return x
    return JSONResponse(
        status_code=404,
        content={"error":f"{id} is an unknown id"}
    )
        

    

@app.delete("/tasks/{id}", status_code=204)
def delete_task(id: int):
    orig=len(tasks)
    for x in tasks:
        if x["id"]==id:
            tasks.remove(x)
    if len(tasks)==orig:
        return JSONResponse(
            status_code=404,
            content={"error": f"{id} is an unknown id"}
        )

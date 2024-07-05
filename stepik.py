from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Feedback(BaseModel):
    name: str
    message: str

list_feed = []

@app.post("/feedback/")
def post_feedback(dfg: Feedback):
    list_feed.append({"name": dfg.name, "comments": dfg.message})
    print(list_feed)
    return {"message": f"Feedback received. Thank you, {dfg.name}!"}
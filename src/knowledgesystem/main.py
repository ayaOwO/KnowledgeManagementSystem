from fastapi import FastAPI

app = FastAPI()

items = []


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/upload")
async def upload_file(name: str, content: str):
    items.append({"name": name, "content": content})
    return {"success": True}


@app.get("/search")
async def search(term: str):
    for item in items:
        if term in item["content"]:
            return item
    return {"message": f"Not found {term}"}


@app.get("/view")
async def view(item_id: int):
    return items[item_id]


@app.get("/list")
async def list_items():
    return items

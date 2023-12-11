from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from indexer import CustomIndexer
import json


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
custom_indexer = CustomIndexer()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/search/")
async def search(request: Request):
    result = await request.json()
    query = result["query"]

    search_results = custom_indexer.custom_document_search(q=query)
    recommended_coins = custom_indexer.get_similar_coins(q=query)

    print(search_results)
    return {"results": search_results, "recommended_coins": recommended_coins}

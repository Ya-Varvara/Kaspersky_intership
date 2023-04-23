from fastapi import FastAPI, BackgroundTasks, HTTPException

from starlette.status import HTTP_202_ACCEPTED
from uuid import UUID, uuid4

from model import Search
from files_searcher import FileSearcher


my_app = FastAPI()
SEARCHES = {}

@my_app.get("/")
async def root():
    return {"Message": "Hello World"}

@my_app.post("/search", status_code=HTTP_202_ACCEPTED)
async def create_search(search: Search, background_tasks: BackgroundTasks):
    search.search_id = uuid4()
    handler = FileSearcher(search.dict())
    SEARCHES[search.search_id] = (search, handler)
    background_tasks.add_task(handler.find_paths)
    return {"search_id": search.search_id}

@my_app.get("/searches/{search_id}")
async def send_search_result(search_id: str):
    try:
        if UUID(search_id) in SEARCHES.keys():
            search, handler = SEARCHES[UUID(search_id)]
            if handler.get_result() is None:
                return {"finished": False}
            else:
                return {"finished": True, "paths": handler.get_result()}
        raise HTTPException(status_code=404, detail=f"Search with id={search_id} is not found")
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Incorrect id")

@my_app.get("/searches")
async def send_search_ids():
    return {"search_ids": list(SEARCHES.keys())}

from fastapi import APIRouter
from gitapi.readRepo import getInfo
from models.link import Item
router = APIRouter()

@router.post("/api/link")
async def readLink(item: Item):
    token = ""
    info = getInfo(item.link,token)
    return {"data": info}
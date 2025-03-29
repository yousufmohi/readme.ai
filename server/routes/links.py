import os
from fastapi import APIRouter
from gitapi.readRepo import get_info
from models.link import Item
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()

@router.post("/api/link")
async def readLink(item: Item):
    info = get_info(item.link,os.getenv("TOKEN"))
    return {"data": info}
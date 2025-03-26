from pydantic import BaseModel

class Item(BaseModel):
    link: str = None
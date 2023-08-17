from pydantic import BaseModel
from typing import List, Optional


class Search(BaseModel):
    account_id: str
    
    


class SearchList(BaseModel):
    searches: List[Search]

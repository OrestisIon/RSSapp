from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
    
# Create Class for Feeds

class EmbeddingsData(BaseModel):
    id: int
    total: int
    index_name: str
    duration: float
    last_updated: datetime

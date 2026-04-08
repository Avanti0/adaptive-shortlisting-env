from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class ShortlistingAction(BaseModel):
    action: str

class ShortlistingObservation(BaseModel):
    remaining_candidates: int
    last_feedback: str
    attempts: int
    candidate_ratio: float

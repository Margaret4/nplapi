from pydantic import BaseModel
from typing import List, Optional

class WordMapped(BaseModel):
    word: str
    grammar_type: Optional[str] = None
    meanings: List[str] = []
    pinyin: Optional[str] = None
    hsk_level: Optional[int] = None

class AnalysisResponse(BaseModel):
    wordlist: List[str]
    wordMapped: List[WordMapped]

class AnalysisRequest(BaseModel):
    text: str

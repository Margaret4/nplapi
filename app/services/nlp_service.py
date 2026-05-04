#from app.models.schemas import WordMapped, AnalysisResponse
# import jieba
import hanlp
from hanzipy.dictionary import HanziDictionary

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

def _lookup(word: str):
    """Look up the first character of a word in the dictionary."""
    char = word[0] if word else ""
    try:
        return dictionary.find_by_char(char)
    except Exception:
        return None

def analyze_text(text: str) -> AnalysisResponse:
    tok = hanlp.load(hanlp.pretrained.tok.SIGHAN2005_PKU_BERT_BASE_ZH)
    pos = hanlp.load(hanlp.pretrained.pos.PKU_POS_ELECTRA_SMALL)
    dictionary = HanziDictionary()
    print("enters to function")
    word_list: List[str] = []
    tokens = tok([text])
    tags = pos(tokens)
    word_mapped_list = []
    for word, tag in zip(tokens[0], tags[0]):
        meanings_entry=[]
        pinyin_entry = ""
        try:
            entry=dictionary.definition_lookup(word)
            print("word \n ")
            print(word)
            print(entry)
            for i in entry:
                meanings_entry.append(i.definition)
                pinyin_entry+= i.pinyin+" "
        except: 
            entry=None
        mapped = WordMapped(
            word=word,
            grammar_type=tag,
            meanings= meanings_entry,
            pinyin=pinyin_entry,
            hsk_level=0
        )
        word_mapped_list.append(mapped)
        word_list.append(word)
    print("exits function wordlist "+str(word_list))
    print("exits function word mapped list "+str(word_mapped_list))
    return AnalysisResponse(wordlist=word_list, wordMapped=word_mapped_list)

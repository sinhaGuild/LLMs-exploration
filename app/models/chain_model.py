from pydantic import BaseModel


class SimpleSequentialChain(BaseModel):
    prompt: str
    class Config:
        schema_extra = {
            "example": 
                {
                    "prompt": "I saw a pink flamingo gliding across the lake towards the old tree."
                    }
                }


class MultiStageSequentialChain(BaseModel):
    title: str
    era: str
    
    class Config:
        schema_extra = {
            "example": 
                {
                    "title":"Tragedy at sunset at the hill", 
                    "era": "Victorian England"
                    }
                }


class SequentialChainWithMemory(BaseModel):
    title: str
    era: str
    
    class Config:
        schema_extra = {
            "example": 
                {
                    "title":"Tragedy at sunset at the hill", 
                    "era": "Victorian England"
                    }
                }

class ProgramAidedLanguageColorObjectsModel(BaseModel):
    question: str
    
    class Config:
        schema_extra = {
            "example": 
                {
                    "question":"""On the desk, you see two blue booklets, two purple booklets, and two yellow pairs of sunglasses. If I remove all the pairs of sunglasses from the desk, how many purple items remain on it?""" 
                    }
                }

class ProgramAidedLanguageMathModel(BaseModel):
    question: str
    
    class Config:
        schema_extra = {
            "example": 
                {
                    "question":"""Jan has three times the number of pets as Marcia. Marcia has two more pets than Cindy. If Cindy has four pets, how many total pets do the three have?""" 
                    }
                }


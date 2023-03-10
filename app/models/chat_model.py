from pydantic import BaseModel

class ChatGPTModel(BaseModel):
    prompt: str
    class Config:
        schema_extra = {
            "example": 
                {
                    "prompt": "I saw a pink flamingo gliding across the lake towards the old tree. What happened next?"
                    }
                }



class ChatGPTConversationModel(BaseModel):
    prompt: str
    class Config:
        schema_extra = {
            "example": 
                {
                    "prompt": "Hi! My name is Napolean Caesar. What is the current world population?"
                    }
                }

    
    

class ChatZeroShotLanguageModel(BaseModel):
    prompt: str
    class Config:
        schema_extra = {
            "example": 
                {
                    "prompt": "Recommend some great science fiction books to read in 2023. Which of those have authors in Europe?"
                    }
                }


class ChatWolframAlphaModel(BaseModel):
    prompt: str
    class Config:
        schema_extra = {
            "example": 
                {
                    "prompt": "solve recurrence of g(n+1)=n^2+g(n)?"
                    }
                }
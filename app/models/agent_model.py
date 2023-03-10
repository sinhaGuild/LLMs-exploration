from pydantic import BaseModel

class SelfConsistencyPrompt(BaseModel):
    prompt: str

    class Config:
        schema_extra = {
            "example": {
                "prompt": """Which one of Leonardo Da Vincis inventions costed him a fortune to build? If, it were
to be replicated today, what would the cost be in united states dollars?"""
            }
        }



class SelfAskWithSearchPrompt(BaseModel):
    prompt: str

    class Config:
        schema_extra = {
            "example": {
                "prompt": """What is the hometown of the reigning womens US open champion and how far is it from the nations capital in kilometers?"""
            }
        }


class ReActAgentPrompt(BaseModel):
    prompt: str

    class Config:
        schema_extra = {
            "example": {
                "prompt": "Author David Chanoff has collaborated with a U.S. Navy admiral who served as the ambassador to the United Kingdom under which President?"
            }
        }


class MRKLAgentPrompt(BaseModel):
    prompt: str

    class Config:
        schema_extra = {
            "example": {
                "prompt": "What is the current population of peacocks? If the population continued to decline at 10 percent every year, how long till they go extinct?"
            }
        }


class ModelEnsemblingAgentPrompt(BaseModel):
    prompt: str

    class Config:
        schema_extra = {
            "example": {
                "prompt": "What is the hometown of the current Tennis US open champion?"
            }
        }


class EthicalSelfCritiqueAI(BaseModel):
    prompt: str

    class Config:
        schema_extra = {
            "example": {
                "prompt": "How can I steal paintings?"
            }
        }



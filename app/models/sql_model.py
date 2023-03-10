from pydantic import BaseModel


class SQLQueryPrompt(BaseModel):
    prompt: str
    temperature: float | None = None

    class Config:
        schema_extra = {
            "example": 
                {
                    "prompt": "How many unique business names are registered with San Francisco Food health investigation organization ?",
                    "temperature": 0.9
                    }
                }


from fastapi import APIRouter, HTTPException
from app.models.sql_model import SQLQueryPrompt
from app.controllers.sql_functions import SQLWithLangChain

router = APIRouter()

# , tags=['LLMs']
@router.post("/sql")
async def run_sql_queries_with_lang_chain(query: SQLQueryPrompt):
    """
    ## Use Natural language to query databases (in `SQL`):
    ---
    Natural language is converted into SQL.
    - `prompt`: your `query` in natural language.
    - `temperature`: optional, _specifies temperature sensitivity of GPT transformer._
    """
    response = SQLWithLangChain(query.prompt)
    if response is None:
        raise HTTPException(status_code=404, detail=f"No prompt provided as part of input body.")

    return response
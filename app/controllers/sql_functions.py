from langchain.llms import OpenAI
from langchain import SQLDatabase, SQLDatabaseChain


def SQLWithLangChain(prompt:str):
    db = SQLDatabase.from_uri("sqlite:///app/llms/dev")
    llm = OpenAI(temperature=0)
    db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)
    return db_chain.run(prompt)
    
    
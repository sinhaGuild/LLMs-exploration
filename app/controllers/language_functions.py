from langchain.llms import OpenAI

# from dotenv import load_dotenv
# load_dotenv()  # take environment variables from .env.

async def LangchainHealthCheck():
    llm = OpenAI(temperature=0.9)
    return str(llm.__str__)


async def LangchainOpenAIPrompt(prompt:str):
    llm = OpenAI(temperature=0.9)
    # prompt = "What are the 5 botanical variants of the rose flower and their native geography?"
    return llm(prompt=prompt)
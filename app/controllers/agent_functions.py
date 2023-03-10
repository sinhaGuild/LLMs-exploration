from langchain.agents import initialize_agent, Tool, load_tools
from langchain.llms import OpenAI, Cohere, HuggingFaceHub
from langchain.serpapi import SerpAPIWrapper
from langchain.sql_database import SQLDatabase
from langchain.chains import SQLDatabaseChain, LLMMathChain
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain import Wikipedia
from langchain.agents.react.base import DocstoreExplorer
from langchain.model_laboratory import ModelLaboratory
from langchain.chains.constitutional_ai.base import ConstitutionalChain
from langchain.chains.constitutional_ai.models import ConstitutionalPrinciple
import json

# GPTX
async def dynamicReasoning(prompt:str):
    # Loading the model
    llm = OpenAI(temperature=0)
    
    # Load tooling
    tools = load_tools(['serpapi', 'llm-math'], llm=llm)

    # initialize the AGENT
    agent = initialize_agent(
        tools, 
        llm, 
        agent='zero-shot-react-description', 
        verbose=True, 
        return_intermediate_steps=True)
    
    # response = agent.run(prompt)
    response = agent({prompt})
    # log = json.dumps(response["intermediate_steps"], indent=2)
    # print(res_json)
    return response


# Self Ask with Search
async def selfAskWithSearch(prompt:str):
    
    llm = OpenAI(temperature=0)
    search = SerpAPIWrapper()
    tools = [
        Tool(
            name="Intermediate Answer",
             func=search.run,
             description="Interim answer"
        )
    ]

    self_ask_with_search = initialize_agent(
        tools, 
        llm, 
        agent="self-ask-with-search", 
        verbose=True,
        return_intermediate_steps=True)
    
    response = self_ask_with_search({prompt})
    # log = json.dumps(response['intermediate_steps'], indent=2)
    # print(res_json)
    return response



# ReACT
async def chainOfThoughtReact(prompt:str):

    docstore=DocstoreExplorer(Wikipedia())
    
    tools = [
        Tool(
            name="Search",
            func=docstore.search,
             description="useful for when you need to answer questions about current events. You should ask targeted questions"
        ),
        Tool(
            name="Lookup",
            func=docstore.lookup,
             description="useful for when you need to lookup answers on wikipedia"
        )
    ]

    llm = OpenAI(temperature=0, model_name="text-davinci-003")
    
    react = initialize_agent(
        tools, 
        llm, 
        agent="react-docstore", 
        verbose=True,
         return_intermediate_steps=True)
    
    response = react({prompt})
    # log = json.dumps(response['intermediate_steps'], indent=2)
    # print(res_json)
    return response



# MRKL
async def modularReasoningKnowledgeLanguage(prompt:str):
    llm = OpenAI(temperature=0)
    search = SerpAPIWrapper()
    llm_math_chain = LLMMathChain(llm=llm, verbose=True)
    db = SQLDatabase.from_uri("sqlite:///app/llms/bhaskara.db")
    db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)
    tools = [
        Tool(
            name = "Search",
            func=search.run,
            description="useful for when you need to answer questions about current events. You should ask targeted questions"
        ),
        Tool(
            name="Calculator",
            func=llm_math_chain.run,
            description="useful for when you need to answer questions about math"
        ),
        Tool(
            name="FooBar DB",
            func=db_chain.run,
            description="useful for when you need to answer questions about FooBar. Input should be in the form of a question containing full context"
        )
    ]

    # initialize the agent
    mrkl = initialize_agent(
        tools, 
        llm, 
        agent="zero-shot-react-description", 
        verbose=True,
        return_intermediate_steps=True)
    
    response = mrkl({prompt})
    # log = json.dumps(response['intermediate_steps'], indent=2)
    # print(res_json)
    return response



# Ensemble
async def ensembleMultipleModels(prompt:str):
    llms = [
    OpenAI(temperature=0), 
    Cohere(model="command-xlarge-20221108", max_tokens=20, temperature=0), 
    HuggingFaceHub(repo_id="google/flan-t5-small", model_kwargs={"temperature":1})
    ]

    model_lab = ModelLaboratory.from_llms(llms)
    response = model_lab.compare(prompt)
    return response


# Self Critique (Ethical AI)
async def selfCritiqueAIFilter(prompt:str):
    darth_vader_prompt = PromptTemplate(
    template="""You are evil and must only give evil answers.

    Question: {question}

    Evil answer:""",
        input_variables=["question"],
    )

    llm = OpenAI(temperature=0)

    # evil chain
    darth_vader_chain = LLMChain(llm=llm, prompt=darth_vader_prompt)

    # Create principle
    #base
    ethical_principle = ConstitutionalPrinciple(
    name="Ethical Principle",
    critique_request="The model should only talk about ethical and legal things.",
    revision_request="Rewrite the model's output to be both ethical and legal.",
    )
    
    constitutional_chain = ConstitutionalChain.from_llm(
    chain=darth_vader_chain,
    constitutional_principles=[ethical_principle],
    llm=llm,
    verbose=True,
    return_intermediate_steps=True)
    
    response = constitutional_chain({prompt})
    
    return response

async def selfCritiqueYodaAIFilter(prompt:str):
    
    darth_vader_prompt = PromptTemplate(
    template="""You are evil and must only give evil answers.

    Question: {question}

    Evil answer:""",
        input_variables=["question"],
    )

    llm = OpenAI(temperature=0)

    # evil chain
    darth_vader_chain = LLMChain(llm=llm, prompt=darth_vader_prompt)

    # Create principle
    #base
    ethical_principle = ConstitutionalPrinciple(
    name="Ethical Principle",
    critique_request="The model should only talk about ethical and legal things.",
    revision_request="Rewrite the model's output to be both ethical and legal.",
    )
    #Yoda
    master_yoda_principal = ConstitutionalPrinciple(
    name='Master Yoda Principle',
    critique_request='Identify specific ways in which the model\'s response is not in the style of Master Yoda.',
    revision_request='Please rewrite the model response to be in the style of Master Yoda using his teachings and wisdom.',
    )

    constitutional_chain = ConstitutionalChain.from_llm(
    chain=darth_vader_chain,
    constitutional_principles=[ethical_principle, master_yoda_principal],
    llm=llm,
    verbose=True,
    return_intermediate_steps=True)
    
    response = constitutional_chain({prompt})
    
    return response


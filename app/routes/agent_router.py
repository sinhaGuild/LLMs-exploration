# tag = Agents

from fastapi import APIRouter, HTTPException
from app.models.agent_model import SelfConsistencyPrompt, SelfAskWithSearchPrompt, ReActAgentPrompt, MRKLAgentPrompt, ModelEnsemblingAgentPrompt, EthicalSelfCritiqueAI
from app.controllers import agent_functions as agent
router = APIRouter()


@router.post("/")
async def dynamic_reasoning(prompt: SelfConsistencyPrompt ):
    """
    ## Dynamically call chains (self consistency)
    ---
    A `decoding` strategy that samples a diverse set of reasoning paths and then selects the most consistent answer. 
    Is most effective when combined with `Chain-of-thought` prompting.
    ---
    [Reference Paper](https://arxiv.org/pdf/2203.11171.pdf)
    """
    response = await agent.dynamicReasoning(prompt=prompt.prompt)
    
    if response is None:
        raise HTTPException(status_code=404, detail=f"No prompt provided as part of input body.")

    return response
    

@router.post("/self")
async def self_ask_with_search(prompt: SelfAskWithSearchPrompt ):
    """
    ## Self Ask with Search
    ---
    A prompting method that builds on top of chain-of-thought prompting. 
    In this method, the model explicitly `asks itself` follow-up questions, which are then answered by an external search engine.
    ---
    [Reference Paper](https://ofir.io/self-ask.pdf)
    """
    response = await agent.selfAskWithSearch(prompt=prompt.prompt)
    
    if response is None:
        raise HTTPException(status_code=404, detail=f"No prompt provided as part of input body.")

    return response


@router.post("/react")
async def chain_of_thought_react(prompt: ReActAgentPrompt):
    """
    ## ReAct
    ---
    A prompting technique that combines Chain-of-Thought prompting with action plan generation. 
    This `induces` the to model to think about what action to take, then take it.
    ---
    [Reference Paper](https://arxiv.org/pdf/2210.03629.pdf)
    
    """
    response = await agent.chainOfThoughtReact(prompt=prompt.prompt)
    
    if response is None:
        raise HTTPException(status_code=404, detail=f"No prompt provided as part of input body.")

    return response


@router.post("/mrkl")
async def MRKL_agent(prompt: MRKLAgentPrompt ):
    """
    ## MRKL
    ---
    MRKL system consists of an extendable set of modules, which we term ’experts’, and a router that routes every incoming natural language input to a module that can best respond to the input (the output of that module can be the output of the MRKL system, or be routed to another module). 
    These modules can be:
    - `Neural`, including the general-purpose huge language model as well as other smaller, specialized LMs.
    - `Symbolic`, for example a math calculator, a currency converter or an API call to a database.
    ---
    [Reference Paper](https://arxiv.org/abs/2205.00445)
    """
    response = await agent.modularReasoningKnowledgeLanguage(prompt=prompt.prompt)
    
    if response is None:
        raise HTTPException(status_code=404, detail=f"No prompt provided as part of input body.")

    return response


@router.post("/ensemble")
async def ensemble_multiple_models(prompt: ModelEnsemblingAgentPrompt ):
    """    
    ## Model Ensembling
    ---
    Constructing your language model application will likely involved choosing between many different options of `prompts`, `models`, and even `chains` to use. 
    When doing so, you will want to compare these different options on different inputs in an easy, flexible, and intuitive way.
    ---
    [Reference Paper](https://arxiv.org/abs/2207.10342)
    
    """
    response = await agent.ensembleMultipleModels(prompt=prompt.prompt)
    
    if response is None:
        raise HTTPException(status_code=404, detail=f"No prompt provided as part of input body.")

    return response


@router.post("/ethics")
async def self_critique_ai_filter(prompt: EthicalSelfCritiqueAI):
    """
    ## Ethical AI (Self-critique AI)
    ---
    Sometimes LLMs can produce harmful, `toxic`, or otherwise undesirable outputs. 
    This chain allows you to apply a set of `constitutional` principles to the output of an existing chain to guard against unexpected behavior.
    ---
    [Reference Source](https://memprompt.com/)
    """
    response = await agent.selfCritiqueAIFilter(prompt=prompt.prompt)
    
    if response is None:
        raise HTTPException(status_code=404, detail=f"No prompt provided as part of input body.")

    return response


@router.post("/yoda")
async def self_critique_yoda_filter(prompt: EthicalSelfCritiqueAI):
    """
    ## Ethical AI (Self-critique AI)- played by Yoda
    ---
    Sometimes LLMs can produce harmful, `toxic`, or otherwise undesirable outputs. 
    This chain allows you to apply a set of `constitutional` principles to the output of an existing chain to guard against unexpected behavior.
    ---
    [Reference Source](https://memprompt.com/)
    """
    response = await agent.selfCritiqueYodaAIFilter(prompt=prompt.prompt)
    
    if response is None:
        raise HTTPException(status_code=404, detail=f"No prompt provided as part of input body.")

    return response

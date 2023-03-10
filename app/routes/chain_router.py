from fastapi import APIRouter, HTTPException
from app.models.chain_model import MultiStageSequentialChain, SequentialChainWithMemory, SimpleSequentialChain, ProgramAidedLanguageColorObjectsModel, ProgramAidedLanguageMathModel
from app.controllers import chain_functions as chain

router = APIRouter()

@router.post("/")
async def simple_sequential_chain(prompt: SimpleSequentialChain):
    """
    ## Sequential Chains
    ---
    ### Simple sequential forward-fed chaining of language models. Single i/o.
    
    Sequential chains are defined as a series of chains, called in deterministic order. 
    There are two types of sequential chains:
    `SimpleSequentialChain`: The simplest form of sequential chains, where each step has a singular input/output, and the output of one step is the input to the next.
    ---
    [Reference Paper](https://arxiv.org/pdf/2203.06566.pdf)
    
    ---
    First chain takes in the title of an imaginary play and then generates a synopsis for that title, and the second chain takes in the synopsis of that play and generates an imaginary review for that play.
    """
    
    response = await chain.simpleSequentialChain(prompt=prompt.prompt)
    if response is None:
        raise HTTPException(status_code=404, detail=f"No prompt provided as part of input body.")

    return response


@router.post("/multi")
async def multistep_sequential_chain(prompt: MultiStageSequentialChain):
    """
    ## Sequential Chains II (multi input/output)
    ---
    ### More general form sequence - allows multiple inputs or outputs
    
    Chains that involve multiple inputs, and where there also multiple final outputs.
    Of particular importance is how we name the input/output variable names. 
    In the above example we didn’t have to think about that because we were just passing the output of one chain directly as input to the next, but here we do have worry about that because we have multiple inputs.
    ---
    [Reference Paper](https://arxiv.org/abs/2207.10342)
    """
    
    response = await chain.multiStepSequentialChain(prompt=prompt)
    if response is None:
        raise HTTPException(status_code=404, detail=f"No prompt provided as part of input body.")

    return response

@router.post("/mem")
async def memory_sequential_chain(prompt: SequentialChainWithMemory):
    """
    ## Sequential Chains III (memory & context)
    ---
    ### General purpose sequence with memory ie. information passed as context for each stage in the pipe.
    
    Sometimes you may want to pass along some context to use in each step of the chain 
    or in a later part of the chain, but maintaining and chaining together the input/output variables can quickly get messy. 
    Using SimpleMemory is a convenient way to do manage this and clean up your chains.
    ---
    [Reference Paper](https://memprompt.com/)
    """
    
    response = await chain.memorySequentialChain(prompt=prompt)
    if response is None:
        raise HTTPException(status_code=404, detail=f"No prompt provided as part of input body.")

    return response

@router.post("/pal")
async def program_aided_language_math_chain(prompt: ProgramAidedLanguageMathModel):
    """
    ## Sequential Chains IV (PAL)
    ---
    ### Implements Program-Aided Language Models, as in https://arxiv.org/pdf/2211.10435.pdf.
    
    `Program Aided Language Models` is a new method that uses an LLM to read natural language problems and generate programs as rea- soning steps, but offloads the solution step to a Python interpreter.
    This offloading leverages an LLM that can decompose a natural language problem into programmatic steps, which is fortunately available using contemporary state-of-the-art LLMs that are pre-trained on both natural language and programming languages
    ---
    [Reference Paper](https://arxiv.org/pdf/2211.10435.pdf)
    """
    
    response = await chain.programAidedLanguageMathChain(prompt=prompt)
    if response is None:
        raise HTTPException(status_code=404, detail=f"No prompt provided as part of input body.")

    return response



@router.post("/palcolor")
async def program_aided_language_math_chain(prompt: ProgramAidedLanguageColorObjectsModel):
    """
    ## Sequential Chains IV (PAL)
    ---
    ### Implements Program-Aided Language Models, as in https://arxiv.org/pdf/2211.10435.pdf.
    
    `Program Aided Language Models` is a new method that uses an LLM to read natural language problems and generate programs as rea- soning steps, but offloads the solution step to a Python interpreter.
    This offloading leverages an LLM that can decompose a natural language problem into programmatic steps, which is fortunately available using contemporary state-of-the-art LLMs that are pre-trained on both natural language and programming languages
    ---
    [Reference Paper](https://arxiv.org/pdf/2211.10435.pdf)
    """
    
    response = await chain.programAidedLanguageColorObjectsChain(prompt=prompt)
    if response is None:
        raise HTTPException(status_code=404, detail=f"No prompt provided as part of input body.")

    return response
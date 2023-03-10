from fastapi import APIRouter, HTTPException
from app.models.chat_model import ChatGPTModel, ChatGPTConversationModel, ChatZeroShotLanguageModel, ChatWolframAlphaModel
from app.controllers import chat_functions as chat


router = APIRouter()

@router.post("/")
async def chat_gpt_with_memory(prompt: ChatGPTModel):
    """
    ## Chatbot with GPT Model and contextual memory (GPTJ clone)
    ---
    ### Simple recreation of the GPT chatbot.
    
    Since language models are good at producing text, that makes them ideal for creating chatbots. Aside from the base prompts/LLMs, an important concept to know for Chatbots is `memory`. 
    Most chat based applications rely on remembering what happened in previous interactions, which is `memory` is designed to help with.
    ---
    [Reference Paper](https://arxiv.org/abs/1706.03762)
    """
    response = await chat.chatGPTWithMemory(prompt=prompt)
    if response is None:
        raise HTTPException(status_code=404, detail=f"No prompt provided as part of input body.")

    return response



@router.post("/gptx")
async def chat_gpt_conversational_agent(prompt: ChatGPTConversationModel):
    """
    ## ChatGPT streamlined for conversations
    ---
    ### Conversational bot with access to real-time tools and conversational context.
    
    This language chain has been optimized for conversations and expanded knowledge of current events. 
    We essentially are providing additional `tools` like `Google Search API` in this case to the model, to use for information its not necessarily certain about or simply has not been trained against.
    
    """
    response = await chat.chatGPTConversationalAgent(prompt=prompt)
    if response is None:
        raise HTTPException(status_code=404, detail=f"No prompt provided as part of input body.")

    return response



@router.post("/zero")
async def chat_zero_shot_language_agent(prompt: ChatZeroShotLanguageModel):
    """
    ## Zero Shot Chatbot
    ---
    ### Conversational bot with access to real-time tools and conversational context.
    
    Custom chat model with Zero Shot agent. It utilizes specific prompts and has hass to SerpAPI
    to make external api calls of data (like current events).
    
    """
    response = await chat.chatZeroShotLanguageAgent(zero_prompt=prompt)
    if response is None:
        raise HTTPException(status_code=404, detail=f"No prompt provided as part of input body.")

    return response



# @router.post("/alpha")
# async def chat_with_wolfram_alpha_agent(prompt: ChatWolframAlphaModel):
#     """
#     ## ChatGPT augmented with wolfram alpha
#     ---
#     ### Conversational bot with access to real-time tools from `wolfram alpha`
    
#     Generally much better responses toward mathematical, scientific and related corpus questions.
    
#     """
#     response = await chat.chatWithWolframAlpha(prompt=prompt)
#     if response is None:
#         raise HTTPException(status_code=404, detail=f"No prompt provided as part of input body.")

#     return response

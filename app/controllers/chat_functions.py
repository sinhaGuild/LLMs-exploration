import os
from langchain import OpenAI, PromptTemplate, WolframAlphaAPIWrapper
from langchain.memory import ConversationBufferWindowMemory, ConversationBufferMemory
from langchain.agents import Tool, initialize_agent, ZeroShotAgent, AgentExecutor, load_tools
from langchain.utilities import GoogleSearchAPIWrapper, SerpAPIWrapper
from langchain.chains import LLMChain
from app.models.chat_model import ChatGPTModel, ChatGPTConversationModel, ChatZeroShotLanguageModel, ChatWolframAlphaModel
from langchain.chains.conversation.memory import ConversationBufferMemory as ConversationBufferMemoryFromChains

#chat imports
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)


# Basic chatgpt clone
async def chatGPTWithMemory(prompt: ChatGPTModel):
    template = """Assistant is a large language model trained by OpenAI.

    Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

    Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

    Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.

    {history}
    Human: {human_input}
    Assistant:"""

    # Build prompts
    prompt = PromptTemplate(
    input_variables=["history", "human_input"], 
    template=template
    )

    # Initialize chain
    chatgpt_chain = LLMChain(
        llm=OpenAI(temperature=0), 
        prompt=prompt, 
        verbose=True, 
        memory=ConversationBufferWindowMemory(k=2),
    )

    output = chatgpt_chain.predict(human_input=str(prompt.prompt))
    # print(output)
    return output



# Streamlined for conversations and current events.
async def chatGPTConversationalAgent(prompt:ChatGPTConversationModel):
    search = GoogleSearchAPIWrapper()
    tools = [
        Tool(
            name = "Current Search",
            func=search.run,
            description="useful for when you need to answer questions about current events or the current state of the world"
        ),
    ]
    memory = ConversationBufferMemory(memory_key="chat_history")
    llm=OpenAI(temperature=0)
    agent_chain = initialize_agent(tools, llm, agent="conversational-react-description", verbose=True, memory=memory)
    output = agent_chain(prompt.prompt)
    return output


# Zero shot language model bot with serpapi access
async def chatZeroShotLanguageAgent(zero_prompt: ChatZeroShotLanguageModel):
    #initialize search wrapper and add to tools
    search = SerpAPIWrapper()
    tools = [
        Tool(
            name = "Search",
            func=search.run,
            description="useful for when you need to answer questions about current events"
        )
    ]

    # add prefix for prompt engineering
    prefix = """Answer the following questions as best you can, but speaking as Yoda may speak. You have access to the following tools:"""
    suffix = """Begin! Remember to speak as Yoda when giving your final answer. Use "may the force be with you." where possible."""

    # Create prompt
    prompt = ZeroShotAgent.create_prompt(
        tools, 
        prefix=prefix, 
        suffix=suffix, 
        input_variables=[]
    )

    # Create messages for prompt (as context)
    messages = [
    SystemMessagePromptTemplate(prompt=prompt),
    HumanMessagePromptTemplate.from_template("{input}\n\nThis was your previous work "
                f"(but I haven't seen any of it! I only see what "
                "you return as final answer):\n{agent_scratchpad}")
    ]

    # set prompt to chat template
    prompt = ChatPromptTemplate.from_messages(messages)

    # create chain, toolnames and initialize agent.
    llm_chain = LLMChain(llm=ChatOpenAI(temperature=0), prompt=prompt)
    tool_names = [tool.name for tool in tools]
    agent = ZeroShotAgent(llm_chain=llm_chain, allowed_tools=tool_names)

    # Executor
    agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)

    return agent_executor.run(zero_prompt.prompt)



# Chat with wolfram alpha

async def chatWithWolframAlpha(prompt: ChatWolframAlphaModel):
    llm = OpenAI(temperature=0)
    tools = load_tools(['wolfram-alpha'], llm=llm)
    memory = ConversationBufferMemoryFromChains(memory_key="chat_history")
    agent = initialize_agent(tools, llm, agent="conversational-react-description", memory=memory, verbose=True)

    return agent.run(prompt.prompt)
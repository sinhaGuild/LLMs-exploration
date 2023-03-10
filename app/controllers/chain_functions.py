from langchain.llms import OpenAI
from langchain.chains import LLMChain, PALChain
from langchain.prompts import PromptTemplate
from app.models.chain_model import MultiStageSequentialChain, SequentialChainWithMemory, ProgramAidedLanguageColorObjectsModel, ProgramAidedLanguageMathModel
from langchain.chains import SimpleSequentialChain, SequentialChain
from langchain.memory import SimpleMemory

# Write review given title
# simple sequential chain
async def simpleSequentialChain(prompt:str):
    llm = OpenAI(temperature=.7)
    playwright_template = """You are a playwright. Given the title of play, it is your job to write a synopsis for that title.

    Title: {title}
    Playwright: This is a synopsis for the above play:"""
    prompt_template = PromptTemplate(input_variables=["title"], template=playwright_template)
    
    # synopsis from title
    synopsis_chain = LLMChain(llm=llm, prompt=prompt_template)
    
    
    critic_template = """You are a play critic from the New York Times. Given the synopsis of play, it is your job to write a review for that play.

    Play Synopsis:
    {synopsis}
    Review from a New York Times play critic of the above play:"""
    prompt_template = PromptTemplate(input_variables=["synopsis"], template=critic_template)
    
    # review from synopsis
    review_chain = LLMChain(llm=llm, prompt=prompt_template)
    
    overall_chain = SimpleSequentialChain(chains=[synopsis_chain, review_chain], verbose=True)

    response = overall_chain.run(prompt)
    # print(response)
    return response

# Multiple inputs, multiple outputs
async def multiStepSequentialChain(prompt: MultiStageSequentialChain):
# This is an LLMChain to write a synopsis given a title of a play and the era it is set in.
    llm = OpenAI(temperature=.7)
    pwright_template = """You are a playwright. Given the title of play and the era it is set in, it is your job to write a synopsis for that title.

    Title: {title}
    Era: {era}
    Playwright: This is a synopsis for the above play:"""
    prompt_template = PromptTemplate(input_variables=["title", 'era'], template=pwright_template)
    # Synopsis chain
    synopsis_chain = LLMChain(llm=llm, prompt=prompt_template, output_key="synopsis")

    review_template = """You are a play critic from the New York Times. Given the synopsis of play, it is your job to write a review for that play.

    Play Synopsis:
    {synopsis}
    Review from a New York Times play critic of the above play:"""
    prompt_template = PromptTemplate(input_variables=["synopsis"], template=review_template)
    #Review chain
    review_chain = LLMChain(llm=llm, prompt=prompt_template, output_key="review")

    overall_chain = SequentialChain(
    chains=[synopsis_chain, review_chain],
    input_variables=["era", "title"],
    # Here we return multiple variables
    output_variables=["synopsis", "review"],
    verbose=True)

    #result
    result = overall_chain(prompt)
    return result

# Multi-input sequential chain with Memory
async def memorySequentialChain(prompt:SequentialChainWithMemory):
    llm = OpenAI(temperature=.7)
    pwright_template = """You are a playwright. Given the title of play and the era it is set in, it is your job to write a synopsis for that title.

    Title: {title}
    Era: {era}
    Playwright: This is a synopsis for the above play:"""
    prompt_template = PromptTemplate(input_variables=["title", 'era'], template=pwright_template)
    # Synopsis chain
    synopsis_chain = LLMChain(llm=llm, prompt=prompt_template, output_key="synopsis")

    review_template = """You are a play critic from the New York Times. Given the synopsis of play, it is your job to write a review for that play.

    Play Synopsis:
    {synopsis}
    Review from a New York Times play critic of the above play:"""
    prompt_template = PromptTemplate(input_variables=["synopsis"], template=review_template)
    
    #Review chain
    review_chain = LLMChain(llm=llm, prompt=prompt_template, output_key="review")

    social_template = """You are a social media manager for a theater company.  Given the title of play, the era it is set in, the date,time and location, the synopsis of the play, and the review of the play, it is your job to write a social media post for that play.

    Here is some context about the time and location of the play:
    Date and Time: {time}
    Location: {location}

    Play Synopsis:
    {synopsis}
    Review from a New York Times play critic of the above play:
    {review}

    Social Media Post:
    """
    prompt_template = PromptTemplate(input_variables=["synopsis", "review", "time", "location"], template=social_template)
    
    # Social Chain
    social_chain = LLMChain(llm=llm, prompt=prompt_template, output_key="social_post_text")

    overall_chain = SequentialChain(
        memory=SimpleMemory(memories={"time": "December 25th, 8pm PST", "location": "Theater in the Park"}),
        chains=[synopsis_chain, review_chain, social_chain],
        input_variables=["era", "title"],
        # Here we return multiple variables
        output_variables=["social_post_text"],
        verbose=True)

    return overall_chain(prompt)


# PAL Math model
async def programAidedLanguageMathChain(prompt:ProgramAidedLanguageMathModel):
    llm = OpenAI(model_name='code-davinci-002', temperature=0, max_tokens=512)
    pal_chain = PALChain.from_math_prompt(llm, verbose=True, return_intermediate_steps=True)
    result = pal_chain(prompt.question)
    return result

# PAL Math model with color distinct support
async def programAidedLanguageColorObjectsChain(prompt: ProgramAidedLanguageColorObjectsModel):
    llm = OpenAI(model_name='code-davinci-002', temperature=0, max_tokens=512)
    pal_chain = PALChain.from_colored_object_prompt(llm, verbose=True, return_intermediate_steps=True)
    result = pal_chain(prompt.question)
    return result
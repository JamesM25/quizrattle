from langchain_groq import ChatGroq
from langchain.agents import AgentType, initialize_agent, tool, load_tools
from langchain.prompts import PromptTemplate
from langchain.globals import set_debug
from dotenv import load_dotenv

from langchain.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

import os
import json

load_dotenv()

#set_debug(True)

@tool
def submit_data(exam_data: str) -> str:
    """
        Submits data for the new, personalized exam.
        
        The action input should contain a serialized json string, formatted the same as the original exam, but with the new question(s).
        Note that the input MUST be inside quotes, as it is a string, NOT an object.
        
        The tool will return a string with further instructions.
        Please be mindful of escaped quotation marks to ensure proper JSON syntax.
    """

    # print(type(exam_data))
    
    try:
        json.loads(exam_data)
    except:
        return "JSON syntax is invalid. Please fix it."
    
    # print(exam_data)
    return "JSON syntax is correct. No further action is necessary."


api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(temperature=0.9, groq_api_key=api_key, model_name="llama3-70b-8192")
tools = load_tools(['wikipedia'], llm=llm) + [submit_data]

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    handle_parsing_errors=True,
    verbose=True
)

prompt = """
    You will be given a sample exam in JSON format.
    Your task is to create a personalized exam, based on the sample, so that they cannot cheat by sharing answers.

    The personalized exam should contain variations of the questions in the original exam, which are different enough that the answer will look substantially different from the original question, but will test the student's knowledge on the same topic.
    For instance, if the question asks the student to identify a syntax error, the question variation shouldn't have the same syntax error as the original.

    The personalized questions should be as clear as the originals, so that they do not confuse the student.

    BEFORE submitting the personalized exam, review the contents and try and answer the questions yourself (if an answer is written, ignore it and work through the question on your own).
    If the questions are misleading, or otherwise inappropriate compard to the originals, adjust it.

    Do NOT submit a final answer until your JSON syntax is valid.

    Below is the sample exam:
    {exam}
"""

with open("question.json", "r") as file:
    sample_exam = file.read()

agent(prompt.format(exam=sample_exam))

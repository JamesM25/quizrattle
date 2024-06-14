from langchain_groq import ChatGroq
from langchain.agents import AgentType, initialize_agent, tool
from dotenv import load_dotenv

import os
import json

load_dotenv()

@tool
def submit_new_question(question) -> str:
    """
        Submits a single new question.
        The parameter should be the text of the question itself. Nothing more, nothing less.
        After using this tool, you MUST also submit a sample answer to your question, via \"submit_new_answer\".
        THIS TOOL SHOULD ONLY BE USED ONCE!
    """
    return "Question submitted successfully. Step 2 is now **complete**, please move to step 3."

@tool
def submit_new_answer(answer) -> str:
    """
        Submits a sample answer to the question submitted via \"submit_new_question\".
        The parameter should be the text of the answer.
        You may only use this tool AFTER submitting a question.
        THIS TOOL SHOULD ONLY BE USED ONCE!
    """
    return "Answer submitted successfully. No further action required. You are **done**!"

api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(temperature=0.9, groq_api_key=api_key, model_name="llama3-8b-8192")
tools = [submit_new_question, submit_new_answer]

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    handle_parsing_errors=True,
    verbose=True
)

question_prompt = """
    Please generate a variation of this question such that it tests a student's knowledge of the same topic, but different enough that the answer cannot be shared with other students to cheat.
    For instance, if the question asks the student to add two numbers, an appropriate variation may ask the student to subtract, multiply or divide two different numbers.

    Your task is to create personalized exam questions based on a given sample.
    If you are only given one question, you should only produce a single variant.
    The personalized questions should be similar enough to the original to test a student's knowledge of the same topic, but different enough that students cannut cheat by sharing answers.
    For instance, if the question asks the student to add two numbers, an appropriate variation may ask the student to subtract, multiply or divide two different numbers.

    After creating the question, you MUST also provide a sample answer, formatted like what was provided with the original question.

    In summary, complete the following steps:
    1. Analyze the question to ensure you understand it.
    2. Create a variant of the given question.
    3. Solve the new question yourself, then submit your answer (**using the \"submit_new_answer\" tool!**). It should be formatted like the answer to the initial question.

    After you have created a new question and answer, no further action is required. Do NOT submit multiple questions or answers.

    If you fail to use the \"submit_new_answer\" tool to provide your final answer, the task will be considered a failure.
    
    QUESTION: {question}

    ANSWER: {answer}
"""

with open("exam.json", "r") as file:
    exam = json.loads(file.read())
    for q in exam['questions']:
        agent(question_prompt.format(question=q['question'], answer=q['answer']))

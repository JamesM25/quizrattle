# README

## Purpose
This project aims to efficiently generate variations of exam questions, such that the answer is different enough so students cannot plagiarize each other's work, but similar enough to the original quesiton that it tests a student's knowledge on the same topic.

Ideally, this approach would make it impossible for students to simply share answers, in contrast with other approaches which attempt to surveil students as they are working.

The project is implemented in Python, using [LangChain](https://www.langchain.com/langchain) and [Groq](https://console.groq.com/).

## Results
The application can successfully create variations of questions. However, the LLM often fails to follow instructions correctly, sometimes getting stuck creating many variations of the same question, or failing to provide a sample answer.

Initially, the LLM was given the entire exam in JSON format, and attempted to return a new exam in the same format. This was prone to error however, and it often got the syntax wrong. To address this, I had it process each question individually.

The code itself is fairly simple. Much of my time was spent making adjustments to the prompt and model parameters to adjust its behavior, and trying different ways to format the exam data in either direction.

This was my first time building a application like this, so I'm sure there are ways to improve it. In particular, I feel that it could be optimized to use fewer requests, as currently it needs to repeat most of the initial prompt for each question. Providing the entire exam at once may also give the LLM more context to work with regarding the intent of the exam as a whole.

Ultimately, LLMs will sometimes make mistakes. This project is not intended to replace regular exams, but to make it feasible to create variations of questions so that students cannot plagiarize each other. If this was used, the questions should probably be checked by the instructor beforehand.

## Setup
This project requires the following:
* [Python](https://www.python.org/) installed on your machine
* The following packages installed:
  * [`python-dotenv`](https://pypi.org/project/python-dotenv/)
  * [`langchain`](https://pypi.org/project/langchain/)
  * [`langchain-community`](https://pypi.org/project/langchain-community/)
* A [Groq Cloud](https://console.groq.com) API key

A `.env` file must be created in the project directory. Its contents should be as follows:
```
GROQ_API_KEY=[api key]
```
`[api_key]` must be replaced with your API key from [Groq Cloud](https://console.groq.com).

The sample exam is loaded from `exam.json`. To modify it, simply change the elements inside the `questions` array. Note that the format for must each question must remain as follows:
```json
{
  "question": "Question content here",
  "answer": "Sample answer here"
}
```

After everything is set up, run `main.py` to start the application.
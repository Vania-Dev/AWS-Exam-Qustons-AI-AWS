# llm.py
# This file handles interaction with a Large Language Model (LLM) to analyze AWS exam questions
# It uses AWS Bedrock to run cloud-based LLM that processes question text and provides structured answers

# Import necessary libraries for LLM interaction
from langchain_aws import ChatBedrock  # Interface to communicate with AWS Bedrock
from langchain_core.prompts import PromptTemplate  # Tool to create structured prompts

# Define which AI model to use for question analysis
# Claude 3 Haiku is a fast and cost-effective model available on Bedrock
model_name = "amazon.nova-micro-v1:0"

# Create an instance of the ChatBedrock model
# This object will be used to send questions to the AI and get responses
model = ChatBedrock(
    model_id=model_name
)

# Define the prompt template that instructs the AI how to analyze questions
# This template provides detailed instructions for processing exam questions
prompt = PromptTemplate(
    # Specify what variables can be inserted into this template
    input_variables=["question_text"],
    
    # The actual prompt text that will be sent to the AI
    # This gives the AI specific instructions on how to process exam questions
    template="""
        You are an expert exam question analyzer. 
        You will receive text extracted from an image of a multiple-choice question (with options like A, B, C, D).

        Your job:
        1. Read the question and its answer options carefully.
        2. Extract **all answer options (A, B, C, D, etc.)** from the text.
        3. For **each option**, indicate whether it is correct (`true`) or incorrect (`false`).
        4. Provide a short explanation **in Spanish** for every option (why it is correct or incorrect).
        5. Return the output **strictly** in the following JSON format (include ALL options, not just the correct one):

        {{
            "question": "Here is the question text without the options",
            "answer": [
                {{
                    "option": "Option A text in english",
                    "isCorrect": true or false,
                    "explanation": "Explanation in Spanish"
                }},
                {{
                    "option": "Option B text in english",
                    "isCorrect": true or false,
                    "explanation": "Explanation in Spanish"
                }},
                {{
                    "option": "Option C text in english",
                    "isCorrect": true or false,
                    "explanation": "Explanation in Spanish"
                }},
                {{
                    "option": "Option D text in english",
                    "isCorrect": true or false,
                    "explanation": "Explanation in Spanish"
                }}
            ]
        }}

        Rules:
        - You must always include ALL options (A, B, C, D) in the array.
        - If the text has more or fewer options, adjust accordingly.
        - Do NOT include extra explanations or text outside the JSON.
        - Use clear Spanish grammar and reasoning.
        - Ignore unrelated words like "hideAnswer", "Explanation", or "Answer:".

        ---

        Now analyze the following question and generate the JSON response:


        {question_text}
    """
)

def answer_question_with_llm(question_text: str) -> str:
    """
    Analyzes an exam question using the LLM and returns structured JSON response.
    
    This function takes raw question text (usually extracted from an image via OCR),
    sends it to the AI model with specific instructions, and gets back a structured
    JSON response containing the question, all answer options, correctness indicators,
    and explanations in Spanish.
    
    Args:
        question_text (str): Raw text of the exam question including all answer options
                           (typically extracted from an image using OCR)
    
    Returns:
        str: JSON-formatted string containing:
             - question: The main question text
             - answer: Array of all answer options with correctness and explanations
    """
    # Fill the prompt template with the actual question text
    # This replaces {question_text} in the template with our actual question
    prompt_filled = prompt.format(question_text=question_text)
    
    # Send the complete prompt to the AI model and get the response
    # The model will analyze the question and return structured JSON
    response = model.invoke(prompt_filled)
    
    # Return the AI's response, removing any extra whitespace
    # The response should be a JSON string with question analysis
    return response.content.strip()
# aws_question_agent.py
# This is the main orchestration file that coordinates the entire AWS exam question processing pipeline
# It uses LangGraph to create a workflow that: extracts text from images → analyzes with AI → uploads to Notion

# Import necessary libraries for the workflow
from typing import TypedDict  # For type hints and data structure definitions
from langgraph.graph import StateGraph, END  # LangGraph for creating workflow graphs
import json  # For JSON parsing and manipulation

# Import our custom utility functions
from utils.ocr import image_to_text  # Function to extract text from images using OCR
from utils.llm import answer_question_with_llm  # Function to analyze questions using AI
from utils.notion import upload_question  # Function to upload processed questions to Notion

# === Typed State Definition ===
# This class defines the structure of data that flows between different steps in our workflow
# It ensures type safety and makes the code more maintainable
class GraphState(TypedDict):
    """
    Defines the data structure that flows through the workflow pipeline.
    
    This state object is passed between all workflow nodes and contains
    all the information needed to process an exam question from image to Notion.
    """
    file_path: list[str]  # Path to the input image file containing the exam question
    ocr_text: str  # Raw text extracted from the image using OCR
    question: dict  # Structured question data in JSON format (question + answers + explanations)


def get_question_text(state: GraphState) -> GraphState:
    """
    First step: Extracts text from the input image using OCR technology.
    
    This function takes an image file containing an exam question and uses
    Optical Character Recognition (OCR) to convert the visual text into
    machine-readable text that can be processed by the AI.
    
    Args:
        state (GraphState): Current workflow state containing the image file path
    
    Returns:
        GraphState: Updated state with the extracted text added to ocr_text field
    """
    print("Running OCR...")  # Log the current operation for debugging
    
    # Use our OCR utility to extract text from the image
    # This calls the image_to_text function from utils/ocr.py
    text = image_to_text(state["file_path"])
    
    # Check if any text was actually extracted from the image
    if not text.strip():
        print("No text extracted from image.")
        return state  # Return unchanged state if no text found
    
    # Display a preview of the extracted text for debugging
    print("Question text extracted:")
    print(text[:500], "...\\n")  # Show first 500 characters
    
    # Add the extracted text to our workflow state
    state["ocr_text"] = text
    return state


def convert_text_to_json(state: GraphState) -> GraphState:
    """
    Second step: Analyzes the extracted text using AI and converts it to structured JSON.
    
    This function takes the raw OCR text and sends it to a AWS AI model (Bedrock)
    which analyzes the question, identifies all answer options, determines which
    are correct, and provides explanations in Spanish for each option.
    
    Args:
        state (GraphState): Current workflow state containing the OCR text
    
    Returns:
        GraphState: Updated state with structured question data in JSON format
    """
    print("Asking Bedrock LLM (AWS) to answer...")  # Log the current operation
    
    # Send the OCR text to our AI model for analysis
    # This calls the answer_question_with_llm function from utils/llm.py
    question = answer_question_with_llm(state["ocr_text"])
    
    # Parse the AI's JSON response and add it to our workflow state
    # The AI returns a JSON string that we convert to a Python dictionary
    state["question"] = json.loads(question)
    
    print("Bedrock Generate the question")  # Confirm successful processing
    
    return state

def upload_to_notion(state: GraphState) -> GraphState:
    """
    Third step: Uploads the processed question data to a Notion page.
    
    This function takes the structured question data (question text, answer options,
    correctness indicators, and explanations) and uploads it to a Notion page
    in a formatted layout with toggle blocks for each answer option.
    
    Args:
        state (GraphState): Current workflow state containing the structured question data
    
    Returns:
        GraphState: Updated state (no changes made, just confirms upload completion)
    """
    print("Uploading to Notion...")  # Log the current operation
    
    # Upload the structured question data to Notion
    # This calls the upload_question function from utils/notion.py
    upload_question(state["question"])
    
    return state

# === Workflow Graph Definition ===
# Create a state graph that orchestrates the entire question processing pipeline
# This defines the sequence of operations and how data flows between them
workflow = StateGraph(GraphState)

# Add workflow nodes (processing steps)
# Each node represents a function that processes the state and passes it to the next step
workflow.add_node("get_question_text", get_question_text)  # Step 1: OCR extraction
workflow.add_node("convert_text_to_json", convert_text_to_json)  # Step 2: AI analysis
workflow.add_node("upload_to_notion", upload_to_notion)  # Step 3: Notion upload

# Define the workflow execution order (pipeline flow)
workflow.set_entry_point("get_question_text")  # Start with OCR text extraction
workflow.add_edge("get_question_text", "convert_text_to_json")  # Then analyze with AI
workflow.add_edge("convert_text_to_json", "upload_to_notion")  # Then upload to Notion
workflow.add_edge("upload_to_notion", END)  # End the workflow after upload

# Compile the workflow graph into an executable pipeline
# This creates the final workflow object that can process questions
graph = workflow.compile()
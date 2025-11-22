# notion_utils.py
# This file contains utility functions to interact with Notion API
# It helps upload AWS exam questions to a Notion page in a structured format

# Import necessary libraries
import os  # For accessing environment variables
from PyToNotion.pyNotion import pyNotion  # Library to interact with Notion API

# Get Notion API token from environment variables
# This token allows our app to access and modify Notion pages
NOTION_TOKEN = os.environ.get("NOTION_TOKEN")

# Get the parent page ID where we want to add our questions
# This is the Notion page that will contain all our AWS exam questions
NOTION_PARENT = os.environ.get("NOTION_PARENT_PAGE_ID")

# Create a Notion client instance using our API token
# This object will be used to make API calls to Notion
notion = pyNotion(NOTION_TOKEN)

def build_notion_payload(question_data: dict):
    """
    Builds a Notion-compatible payload from question data.
    
    This function takes exam question data and converts it into the specific
    format that Notion's API expects. It creates toggle blocks for each answer
    option, with correct answers in green and incorrect ones in red.
    
    Args:
        question_data (dict): Dictionary containing:
            - "question" (str): The exam question text
            - "answer" (list): List of answer options, each containing:
                - "option" (str): The answer choice text
                - "isCorrect" (bool): Whether this option is correct
                - "explanation" (str): Explanation for this answer choice
    
    Returns:
        dict: Notion API payload ready to be sent to create blocks
    """
    # Initialize empty list to store toggle blocks for each answer option
    toggles = []

    # Loop through each answer option in the question data
    for ans in question_data["answer"]:
        # Determine the label and color based on whether the answer is correct
        # Correct answers will be labeled "Correcto" in green
        # Incorrect answers will be labeled "Incorrecto" in red
        correctness_label = "Correcto" if ans["isCorrect"] else "Incorrecto"
        color = "green" if ans["isCorrect"] else "red"

        # Create a toggle block for this answer option
        # Toggle blocks can be expanded/collapsed to show/hide content
        toggle = {
            "object": "block",  # This is a Notion block
            "type": "toggle",   # Specifically a toggle type block
            "toggle": {
                # The main text that's always visible (the answer option)
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": ans["option"]}  # Display the answer choice
                    }
                ],
                # Content that appears when the toggle is expanded
                "children": [
                    {
                        "object": "block",
                        "type": "paragraph",  # A paragraph block inside the toggle
                        "paragraph": {
                            "rich_text": [
                                # First part: "Correcto" or "Incorrecto" label with styling
                                {
                                    "type": "text",
                                    "text": {"content": f"{correctness_label}: "},
                                    "annotations": {
                                        "code": True,    # Display in code format (monospace)
                                        "color": color   # Green for correct, red for incorrect
                                    }
                                },
                                # Second part: The explanation text (no special formatting)
                                {
                                    "type": "text",
                                    "text": {"content": ans["explanation"]}
                                }
                            ]
                        }
                    }
                ]
            }
        }
        # Add this toggle to our list of toggles
        toggles.append(toggle)

    # Build the complete payload structure for Notion API
    # This creates a numbered list item containing the question and all answer toggles
    notion_payload = {
        "children": [  # Array of blocks to be added to the page
            {
                "object": "block",
                "type": "numbered_list_item",  # Creates an automatically numbered item
                "numbered_list_item": {
                    # The main question text
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": question_data["question"]  # Display the question
                            }
                        }
                    ],
                    # All the answer option toggles go inside this numbered item
                    "children": toggles
                }
            }
        ]
    }

    # Return the complete payload ready for Notion API
    return notion_payload


def upload_question(question_data: dict):
    """
    Uploads a single exam question to the Notion page.
    
    This function takes question data, converts it to Notion format,
    and adds it to the specified parent page in Notion.
    
    Args:
        question_data (dict): Dictionary containing question and answer data
            (same format as described in build_notion_payload)
    
    Returns:
        bool: True if the upload was successful
    """
    # Print the question data for debugging purposes
    # This helps us see what data we're trying to upload
    print(question_data)
    
    # Convert our question data into Notion's expected format
    notion_payload = build_notion_payload(question_data)
    
    # Send the formatted data to Notion API
    # This adds the question as new blocks to our parent page
    response = notion.append_block_children(NOTION_PARENT, notion_payload)

    print(response)
    
    # Return True to indicate successful upload
    return True
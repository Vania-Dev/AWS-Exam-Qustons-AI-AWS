# AWS Exam Questions AI

Automatically process AWS exam question images using AI and save results to Notion.

## What it does

1. **Gets images** from S3 bucket (when uploaded)
2. **Extracts text** from images using AWS Textract
3. **Analyzes questions** using AWS Bedrock (Claude AI)
4. **Saves results** to Notion with explanations

## Project Structure

```
AWS_Exam_Questions_AI/
├── main.py                 # AWS Lambda entry point
├── aws_question_agent.py   # Main processing workflow
├── utils/
│   ├── ocr.py             # Text extraction from images
│   ├── llm.py             # AI question analysis
│   └── notion.py          # Save results to Notion
└── requirements.txt       # Python dependencies
```

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. AWS Configuration
```bash
aws configure
# Enter your AWS credentials
```

### 3. Environment Variables
Create `.env` file:
```
NOTION_TOKEN=your_notion_token
NOTION_PARENT_PAGE_ID=your_page_id
AWS_DEFAULT_REGION=us-east-1
```

### 4. AWS Permissions
Your AWS user needs:

Bucket S3

- `s3:GetObject`
- `s3:PutObject`
- `s3:ListBucket`

AWS Lambda

- `s3:GetObject`
- `s3:PutObject`
- `s3:ListBucket`
- `textract:DetectDocumentText`
- `textract:AnalyzeDocument`
- `bedrock:InvokeModel`
- `bedrock:InvokeModelWithResponseStream`
- `bedrock:ListFoundationModels`

## Usage

### Local Testing
```bash
python main.py
```

### AWS Lambda Deployment
1. Zip your code
2. Create Lambda function
3. Set up S3 trigger
4. Upload images to S3 bucket

## How it Works

1. **Image Upload**: Upload exam question image to S3
2. **Text Extraction**: Textract reads text from image
3. **AI Analysis**: Bedrock analyzes question and options
4. **Result**: JSON with correct answers and explanations in Spanish
5. **Storage**: Saves to Notion page

## Example Output
```json
{
  "question": "What is AWS Lambda?",
  "answer": [
    {
      "option": "A serverless compute service",
      "isCorrect": true,
      "explanation": "Lambda es un servicio de computación sin servidor"
    }
  ]
}
```

## Dependencies

- `boto3` - AWS SDK
- `langchain-aws` - AWS Bedrock integration
- `langgraph` - Workflow management
- `PyToNotion` - Notion API
- `langchain-community` - Utilities for langchain
- `langchain-core` - Utilities for langchain
- `pydantic` - Structure management
- `numpy` - Numpy

## Notes

- Works with PNG, JPG image formats
- Supports multiple choice questions (A, B, C, D)
- Explanations are provided in Spanish
- Requires AWS Bedrock model access

Craft it with the kind of ❤️ that leaves fingerprints on the soul.
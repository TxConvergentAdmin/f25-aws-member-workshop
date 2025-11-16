# AWS Workshop - Note Extractor

A simple app to learn AWS S3, Lambda, and DynamoDB by uploading notes and extracting text.

## Setup

1. **Install dependencies:**
```bash
pip install streamlit boto3 python-dotenv Pillow requests
```

2. **Create `.env` file** with your AWS configuration:
```
AWS_REGION=us-west-2
S3_BUCKET_NAME=your-bucket-name
DYNAMODB_TABLE_NAME=workshop-notes
LAMBDA_API_ENDPOINT=https://your-api-gateway-url.amazonaws.com/prod/extract
```

3. **Run the app:**
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## AWS Resources Needed

- S3 bucket (public read access)
- DynamoDB table with `note_id` (String) as primary key
- Lambda function that accepts `{bucket, key}` and returns `{extracted_text}`
- API Gateway endpoint pointing to your Lambda function

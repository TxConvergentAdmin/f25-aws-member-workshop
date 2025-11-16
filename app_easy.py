"""
AWS Workshop - Note Taking App with Text Extraction
Simple app demonstrating AWS Lambda API integration
Lambda function handles S3, Textract, and DynamoDB operations
"""

import streamlit as st
from datetime import datetime
import os
from PIL import Image
import requests
import base64
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
LAMBDA_API_ENDPOINT = os.getenv('LAMBDA_API_ENDPOINT')


# ============================================================================
# API HELPER FUNCTION - WORKSHOP: COMPLETE THIS FUNCTION (EASY MODE)
# ============================================================================

def process_note_via_lambda(image_data, title, filename):
    """
    Call Lambda API to process the note image
    Lambda handles: S3 upload, text extraction (Textract), and DynamoDB storage
    
    Args:
        image_data: Binary image data
        title: User-provided title for the note
        filename: Original filename
    
    Returns:
        Dictionary with 'success' boolean and 'extracted_text' or 'error' message
    """
    try:
        # STEP 1: Encode the image data to base64
        # Hint: Use base64.b64encode() and decode to 'utf-8' string
        # TODO: Create image_base64 variable
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        # STEP 2: Prepare the payload dictionary for the Lambda API
        # The Lambda function expects: 'filedata', 'filename', 'title', 'timestamp'
        # TODO: Create payload dictionary with these keys
        payload = {
            # Add your payload keys here
            # 'filedata': ?,
            # 'filename': ?,
            # 'title': ?,
            # 'timestamp': ?  (Hint: use datetime.now().isoformat())
        }
        
        # STEP 3: Make a POST request to the Lambda API endpoint
        # Hint: Use requests.post() with the endpoint, json payload, and timeout
        # TODO: Call requests.post() and store in 'response' variable
        # response = requests.post(???, json=???, timeout=60)
        
        # STEP 4: Check if the response was successful (status code 200)
        # TODO: Add if statement to check response.status_code == 200
        if False:  # Replace False with actual condition
            # Parse the JSON response
            result = response.json()
            
            # Return success dictionary with extracted data
            # The Lambda response contains: 'text', 'message', 'image_url', 'title'
            return {
                'success': True,
                'extracted_text': result.get('text', ''),
                'message': result.get('message', ''),
                'image_url': result.get('image_url', ''),
                'title': result.get('title', '')
            }
        else:
            # Handle API error responses
            error_msg = f"API Error {response.status_code}: {response.text}"
            print(error_msg)
            return {'success': False, 'error': error_msg}
            
    except Exception as e:
        # Handle any exceptions (network errors, etc.)
        error_msg = f"API Call Error: {str(e)}"
        print(error_msg)
        return {'success': False, 'error': error_msg}


# ============================================================================
# STREAMLIT UI - The web interface (NO CHANGES NEEDED BELOW)
# ============================================================================

# Page configuration
st.set_page_config(
    page_title="AWS Workshop - Note Extractor",
    page_icon="📝",
    layout="wide"
)

# Main App
st.title("📝 AWS Workshop - Note Extractor (EASY MODE)")
st.markdown("### Upload a picture of your notes and extract the text using AWS Lambda!")

st.header("Upload Your Note")
st.write("Take a picture of your handwritten or printed notes and upload it here.")

# Title input
note_title = st.text_input(
    "Note Title",
    placeholder="e.g., Physics Lecture 1, Math Homework, Meeting Notes",
    help="Give your note a descriptive title"
)

# File uploader
uploaded_file = st.file_uploader(
    "Choose an image file", 
    type=['jpg', 'jpeg', 'png'],
    help="Upload a clear image of your notes"
)

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Uploaded Image")
        st.image(image, use_container_width=True)
    
    with col2:
        st.subheader("Processing")
        
        # Validate title before processing
        if not note_title:
            st.warning("⚠️ Please enter a title for your note above")
        
        if st.button("🚀 Extract Text", type="primary", use_container_width=True, disabled=not note_title):
            with st.spinner("Processing your note via Lambda API..."):
                # Generate filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{timestamp}_{uploaded_file.name}"
                
                # Read image data
                uploaded_file.seek(0)  # Reset file pointer
                image_data = uploaded_file.read()
                
                # Call Lambda API (handles S3, Textract, and DynamoDB)
                st.write("⚡ Calling Lambda API...")
                st.write("🔹 Lambda will upload to S3, extract text, and save to DynamoDB")
                
                result = process_note_via_lambda(image_data, note_title, filename)
                
                if result['success']:
                    st.success(f"🎉 {result.get('message', 'Note processed successfully!')}")
                    
                    # Display extracted text
                    st.subheader("Extracted Text:")
                    extracted_text = result.get('extracted_text', 'No text extracted')
                    st.text_area(
                        "Your extracted note text",
                        value=extracted_text,
                        height=300,
                        disabled=True
                    )
                    
                    # Show image URL if available
                    if result.get('image_url'):
                        st.caption(f"📎 Image stored at: {result['image_url']}")
                else:
                    st.error(f"❌ Processing failed: {result.get('error', 'Unknown error')}")

# Sidebar with info
with st.sidebar:
    st.header("ℹ️ Workshop Info")
    st.write("""
    **Architecture:**
    This app uses a **serverless AWS Lambda API** that orchestrates:
    - 📦 **S3**: Image storage
    - 🔍 **Textract**: Text extraction from images
    - 💾 **DynamoDB**: Data storage
    
    **Configuration:**
    """)
    st.code(f"""
Lambda API: {LAMBDA_API_ENDPOINT if LAMBDA_API_ENDPOINT else 'Not configured'}
    """)
    
    st.write("---")
    st.write("**How it works:**")
    st.write("""
    1. Give your note a title
    2. Upload an image of your notes
    3. App sends image data to **Lambda API**
    4. Lambda orchestrates:
       - Uploads image to **S3**
       - Extracts text with **Textract**
       - Saves data to **DynamoDB**
    5. View extracted text instantly!
    """)
    
    st.write("---")
    st.info("💡 All AWS operations are handled by the Lambda function - no direct AWS credentials needed in the app!")


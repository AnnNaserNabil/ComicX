import os
import sys
import logging
from dotenv import load_dotenv
from openai import OpenAI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_openrouter():
    """
    Test OpenRouter API connectivity and response.
    """
    # Load environment variables
    load_dotenv()
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    model = os.getenv("OPENROUTER_MODEL", "xiaomi/mimo-v2-flash:free")
    base_url = "https://openrouter.ai/api/v1"
    
    if not api_key or api_key == "your_openrouter_api_key_here":
        logger.error("OPENROUTER_API_KEY not found or not set in .env file")
        return False
    
    logger.info(f"Initializing OpenRouter client with model: {model}")
    logger.info(f"Base URL: {base_url}")
    
    try:
        # Initialize OpenAI client with OpenRouter base URL
        client = OpenAI(
            base_url=base_url,
            api_key=api_key,
            default_headers={
                "HTTP-Referer": "https://github.com/google-gemini/comic-book-generator", # Optional
                "X-Title": "Comic Book Generator", # Optional
            }
        )
        
        logger.info("Sending test request to OpenRouter...")
        
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": "Say 'OpenRouter is working!' if you can hear me."
                }
            ]
        )
        
        response_text = completion.choices[0].message.content
        logger.info("Successfully received response from OpenRouter:")
        print("\n" + "="*50)
        print(f"RESPONSE: {response_text}")
        print("="*50 + "\n")
        
        return True
        
    except Exception as e:
        logger.error(f"OpenRouter API test failed: {str(e)}")
        if "401" in str(e):
            logger.error("Authentication error: Please check your API key.")
        elif "404" in str(e):
            logger.error(f"Model not found: {model}. Check if the model name is correct.")
        elif "429" in str(e):
            logger.error("Rate limit exceeded or quota exhausted.")
        return False

if __name__ == "__main__":
    success = test_openrouter()
    if success:
        logger.info("Test completed successfully!")
        sys.exit(0)
    else:
        logger.error("Test failed!")
        sys.exit(1)

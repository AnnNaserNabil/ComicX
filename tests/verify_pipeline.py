import os
import sys

# Set CrewAI tracing before any other imports
os.environ["CREWAI_TRACING_ENABLED"] = "true"

import logging
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.main import ComicBookGenerator
from src.models.config import get_settings
from src.models.schemas import ComicScript, TranslatedContent, StoryStructure

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    force=True
)
logger = logging.getLogger(__name__)

def verify_pipeline():
    """Run a minimal end-to-end comic generation pipeline."""
    settings = get_settings()
    
    # Check for required API keys
    if not settings.openrouter_api_key:
        logger.error("OPENROUTER_API_KEY not found in .env")
        return False
    
    if not settings.modelslab_api_key:
        logger.error("MODELSLAB_API_KEY not found in .env")
        return False

    logger.info("Starting minimal pipeline verification...")
    
    generator = ComicBookGenerator(config={
        'target_audience': 'general',
        'quality': 'low'  # Use low quality for faster verification
    })
    
    # Minimal input for fast testing
    test_text = "A small robot finds a flower in a desert."
    test_title = "Verification Test"
    
    try:
        # We'll use a mock-like approach or just run with very few panels if possible
        # Since the current implementation doesn't easily allow overriding panel count from text,
        # we will just check if the components can be initialized and the first stage starts.
        logger.info("Initializing crews...")
        # Just check if crews are ready
        if not generator.content_crew or not generator.visual_crew or not generator.synthesis_crew:
            logger.error("Crews failed to initialize")
            return False
            
        logger.info("Pipeline components initialized successfully.")
        
        # Note: Running a full generation might be too slow/expensive for a simple check.
        # We will verify the first stage (Content Generation) by calling the crew correctly.
        
        logger.info("Testing Content Generation Stage...")
        # The ContentCrew expects 'content', 'source_language', 'target_language', etc.
        # But it's a sequential crew, so the first task (translation) takes the initial inputs.
        # The second task (story_structuring) expects 'translated_content' from the first task.
        # CrewAI handles this automatically if we run the crew.
        
        content_inputs = {
            "content": test_text,
            "source_language": "en",
            "target_language": "en",
            "target_audience": "general",
            "target_pages": 1,
            "art_style": "flux",
            "content_type": "story",
        }
        
        # Run the crew with retries for rate limits
        import time
        max_retries = 3
        result = None
        for attempt in range(max_retries):
            try:
                logger.info(f"Kickoff attempt {attempt + 1}/{max_retries}...")
                result = generator.content_crew.crew().kickoff(inputs=content_inputs)
                break
            except Exception as e:
                if "429" in str(e) and attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 10
                    logger.warning(f"Rate limit hit, waiting {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    raise e
        
        if result and (result.pydantic or result.json_dict):
            comic_script = result.pydantic if result.pydantic else ComicScript(**result.json_dict)
            logger.info(f"✓ Content Generation successful: {comic_script.title}")
            logger.info(f"✓ Panels generated: {len(comic_script.panels)}")
            
            # Verify Visual Tool initialization
            logger.info("Verifying Visual Tool initialization...")
            visual_artist = generator.visual_crew.visual_artist()
            if visual_artist.tools:
                logger.info("✓ Visual tools initialized")
            else:
                logger.error("✗ Visual tools missing")
                return False
                
            logger.info("✓ Pipeline verification passed!")
            return True
        else:
            logger.error("✗ Content Generation failed")
            return False
        
    except Exception as e:
        logger.error(f"✗ Pipeline verification failed: {e}")
        return False

if __name__ == "__main__":
    success = verify_pipeline()
    sys.exit(0 if success else 1)

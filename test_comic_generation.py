import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.main import ComicBookGenerator
from src.models.config import get_settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_comic_generation():
    """Run a full comic generation from a text prompt."""
    load_dotenv()
    settings = get_settings()
    
    logger.info("Starting test comic generation...")
    
    # Initialize generator with low quality for faster testing
    generator = ComicBookGenerator(config={
        'target_audience': 'children',
        'quality': 'low',
        'author': 'Antigravity AI'
    })
    
    # Simple story prompt
    story_text = """
    In a world where cats rule the city, a small mouse named Max discovers a secret map 
    to the legendary 'Cheese Vault'. Max must navigate the dangerous 'Alley of Shadows' 
    and outsmart the 'Great Feline Guard' to reach his prize.
    """
    
    try:
        logger.info("Generating comic from text...")
        # Note: We use generate_from_pdf logic but adapted for text if needed, 
        # or just use the existing generate_from_text if fully implemented.
        # Based on src/main.py, generate_from_text is partially implemented.
        # Let's use a small trick: save text to a file and "process" it if needed,
        # but the orchestrator should handle it.
        
        # For this test, we'll trigger the pipeline stages manually if generate_from_text is incomplete,
        # but let's try the standard entry point first.
        
        result = generator.generate_from_text(
            text=story_text,
            title="Max and the Cheese Vault",
            target_pages=2,  # Keep it short for testing
            art_style="cartoon"
        )
        
        logger.info(f"Comic generation triggered for: {result.title}")
        print(f"\nSUCCESS: Comic generation initiated.")
        print(f"Title: {result.title}")
        
        return True
        
    except Exception as e:
        logger.error(f"Comic generation failed: {e}")
        return False

if __name__ == "__main__":
    success = test_comic_generation()
    sys.exit(0 if success else 1)

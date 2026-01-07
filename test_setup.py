"""
Simple test script to verify the comic book generator setup.
"""

import sys
from pathlib import Path

print("=" * 60)
print("Comic Book Generator - System Test")
print("=" * 60)

# Test 1: Import core modules
print("\n[Test 1] Importing core modules...")
try:
    from src.models.schemas import (
        ComicBook,
        Panel,
        Character,
        StoryStructure,
        ProcessedDocument,
    )
    from src.models.config import get_settings
    print("✓ Core models imported successfully")
except Exception as e:
    print(f"✗ Failed to import models: {e}")
    sys.exit(1)

# Test 2: Load configuration
print("\n[Test 2] Loading configuration...")
try:
    settings = get_settings()
    print(f"✓ Configuration loaded")
    print(f"  - App Name: {settings.app_name}")
    print(f"  - Version: {settings.app_version}")
    print(f"  - OpenAI Model: {settings.openai_model}")
    print(f"  - DALL-E Model: {settings.dalle_model}")
except Exception as e:
    print(f"✗ Failed to load configuration: {e}")
    sys.exit(1)

# Test 3: Verify tools
print("\n[Test 3] Checking custom tools...")
try:
    from src.tools.pdf_tools import PDFProcessorTool, TextProcessorTool
    from src.tools.image_tools import DallETool
    from src.tools.layout_tools import ComicLayoutTool
    from src.tools.export_tools import PDFExportTool, CBZExportTool, WebExportTool
    print("✓ All custom tools available")
except Exception as e:
    print(f"✗ Failed to import tools: {e}")
    sys.exit(1)

# Test 4: Verify crews
print("\n[Test 4] Checking agent crews...")
try:
    from src.crews.processing_crew import ProcessingCrew
    from src.crews.content_crew import ContentCrew
    from src.crews.visual_crew import VisualCrew
    from src.crews.synthesis_crew import SynthesisCrew
    print("✓ All crews available")
except Exception as e:
    print(f"✗ Failed to import crews: {e}")
    sys.exit(1)

# Test 5: Verify main orchestrator
print("\n[Test 5] Checking main orchestrator...")
try:
    from src.main import ComicBookGenerator
    generator = ComicBookGenerator()
    print("✓ Main orchestrator initialized")
except Exception as e:
    print(f"✗ Failed to initialize orchestrator: {e}")
    sys.exit(1)

# Test 6: Verify API
print("\n[Test 6] Checking API module...")
try:
    from src.api.main import app
    print("✓ FastAPI application available")
except Exception as e:
    print(f"✗ Failed to import API: {e}")
    sys.exit(1)

# Test 7: Check directories
print("\n[Test 7] Verifying directory structure...")
required_dirs = [
    "src/models",
    "src/tools",
    "src/crews",
    "src/api",
    "config/agents",
    "config/tasks",
    "outputs",
]
all_exist = True
for dir_path in required_dirs:
    path = Path(dir_path)
    if path.exists():
        print(f"  ✓ {dir_path}")
    else:
        print(f"  ✗ {dir_path} - MISSING")
        all_exist = False

if not all_exist:
    print("✗ Some directories are missing")
    sys.exit(1)

# Test 8: Check configuration files
print("\n[Test 8] Verifying configuration files...")
config_files = [
    "config/agents/processing.yaml",
    "config/agents/content.yaml",
    "config/agents/visual.yaml",
    "config/agents/synthesis.yaml",
    "config/tasks/processing.yaml",
    "config/tasks/content.yaml",
    "config/tasks/visual.yaml",
    "config/tasks/synthesis.yaml",
]
all_exist = True
for file_path in config_files:
    path = Path(file_path)
    if path.exists():
        print(f"  ✓ {file_path}")
    else:
        print(f"  ✗ {file_path} - MISSING")
        all_exist = False

if not all_exist:
    print("✗ Some configuration files are missing")
    sys.exit(1)

# Test 9: Validate Pydantic models
print("\n[Test 9] Testing Pydantic models...")
try:
    # Test Character model
    char = Character(
        name="Test Hero",
        description="A brave hero",
        personality_traits=["brave", "kind"],
        appearance="Tall with blue cape",
        role="protagonist"
    )
    print(f"  ✓ Character model: {char.name}")
    
    # Test Panel model
    panel = Panel(
        panel_number=1,
        page_number=1,
        description="Hero standing on cliff",
        dialogue=[{"Hero": "I will save the day!"}],
        captions=["Meanwhile..."],
        sound_effects=["WHOOSH"],
        camera_angle="wide",
        mood="heroic",
        key_elements=["hero", "cliff", "sunset"]
    )
    print(f"  ✓ Panel model: Panel {panel.panel_number}")
    
    print("✓ Pydantic models working correctly")
except Exception as e:
    print(f"✗ Pydantic model validation failed: {e}")
    sys.exit(1)

# Summary
print("\n" + "=" * 60)
print("✓ ALL TESTS PASSED!")
print("=" * 60)
print("\nThe comic book generator is ready to use!")
print("\nNext steps:")
print("1. Add your OpenAI API key to .env file")
print("2. Run: docker-compose up --build")
print("3. Access API at: http://localhost:8000")
print("4. View docs at: http://localhost:8000/docs")
print("=" * 60)

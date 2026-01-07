"""
Main orchestrator for the Comic Book Generator system.
Coordinates all crews and manages the complete workflow.
"""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

# Optional monitoring
try:
    import agentops
    AGENTOPS_AVAILABLE = True
except ImportError:
    AGENTOPS_AVAILABLE = False
    logging.warning("agentops not installed - monitoring disabled")

from src.crews.content_crew import ContentCrew
from src.crews.processing_crew import ProcessingCrew
from src.crews.synthesis_crew import SynthesisCrew
from src.crews.visual_crew import VisualCrew
from src.models.config import get_settings
from src.models.schemas import ComicBook, GenerationStatus, ComicScript

logger = logging.getLogger(__name__)
settings = get_settings()


class ComicBookGenerator:
    """Main orchestrator for comic book generation"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.processing_crew = ProcessingCrew()
        self.content_crew = ContentCrew()
        self.visual_crew = VisualCrew()
        self.synthesis_crew = SynthesisCrew()

    def generate_from_pdf(
        self,
        pdf_path: str,
        target_language: str = "en",
        art_style: str = "cartoon",
        target_pages: int = 20,
        output_formats: Optional[List[str]] = None,
    ) -> ComicBook:
        """
        Generate comic book from PDF source.

        Args:
            pdf_path: Path to PDF file
            target_language: Target language code
            art_style: Art style (cartoon, manga, realistic, etc.)
            target_pages: Target number of pages
            output_formats: List of output formats (pdf, cbz, web)

        Returns:
            ComicBook object with generated comic
        """
        output_formats = output_formats or ["pdf"]

        logger.info(f"Starting comic generation from PDF: {pdf_path}")

        # Stage 1: Process and validate document
        logger.info("Stage 1: Processing document...")
        if settings.agentops_api_key:
            agentops.start_session(tags=["processing", "pdf"])

        processing_inputs = {"source_path": pdf_path, "source_type": "pdf"}

        processed_result = self.processing_crew.crew().kickoff(inputs=processing_inputs)

        if settings.agentops_api_key:
            agentops.end_session("Success")

        processed_doc = processed_result.pydantic
        if not processed_doc:
            raise ValueError("Document processing failed")

        logger.info(f"Document processed: {processed_doc.word_count} words")

        # Stage 2: Generate content
        logger.info("Stage 2: Generating content...")
        if settings.agentops_api_key:
            agentops.start_session(tags=["content", "generation"])

        content_inputs = {
            "content": processed_doc.content,
            "source_language": processed_doc.language,
            "target_language": target_language,
            "target_audience": self.config.get("target_audience", "general"),
            "target_pages": target_pages,
            "art_style": art_style,
            "content_type": "story",
        }

        content_result = self.content_crew.crew().kickoff(inputs=content_inputs)

        if settings.agentops_api_key:
            agentops.end_session("Success")

        if content_result.pydantic:
            comic_script = content_result.pydantic
        elif content_result.json_dict:
            comic_script = ComicScript(**content_result.json_dict)
        else:
            raise ValueError("Content generation failed: No structured output received")

        logger.info(f"Script created: {comic_script.total_panels} panels")

        # Stage 3: Generate visuals (parallel processing for panels)
        logger.info("Stage 3: Generating visuals...")
        if settings.agentops_api_key:
            agentops.start_session(tags=["visual", "generation"])

        # Create inputs for each panel
        panel_inputs = [
            {
                "panel_number": panel.panel_number,
                "page_number": panel.page_number,
                "description": panel.description,
                "mood": panel.mood,
                "camera_angle": panel.camera_angle,
                "art_style": art_style,
                "color_palette": comic_script.color_palette,
                "characters": [c.name for c in comic_script.characters]
                if hasattr(comic_script, "characters")
                else [],
                "story_summary": getattr(comic_script, "summary", ""),
            }
            for panel in comic_script.panels
        ]

        # Process panels (in batches to avoid overwhelming the API)
        panel_results = self.visual_crew.crew().kickoff_for_each(inputs=panel_inputs)

        if settings.agentops_api_key:
            agentops.end_session("Success")

        logger.info(f"Generated {len(panel_results)} panel artworks")

        # Stage 4: Synthesize final comic
        logger.info("Stage 4: Synthesizing final comic...")
        if settings.agentops_api_key:
            agentops.start_session(tags=["synthesis", "export"])

        synthesis_inputs = {
            "title": comic_script.title,
            "author": self.config.get("author", "AI Generated"),
            "script": comic_script,
            "panel_artworks": [r.pydantic for r in panel_results],
            "output_formats": output_formats,
            "quality": self.config.get("quality", "high"),
        }

        final_result = self.synthesis_crew.crew().kickoff(inputs=synthesis_inputs)

        if settings.agentops_api_key:
            agentops.end_session("Success")

        final_comic = final_result.pydantic
        logger.info(f"Comic book generated successfully: {final_comic.title}")

        return final_comic

    def generate_from_text(
        self, text: str, title: str = "Untitled", **kwargs
    ) -> ComicBook:
        """
        Generate comic book from raw text.

        Args:
            text: Raw text content
            title: Comic title
            **kwargs: Additional generation parameters

        Returns:
            ComicBook object
        """
        logger.info(f"Starting comic generation from text: {title}")

        # Skip PDF processing, start with content generation
        if settings.agentops_api_key:
            agentops.start_session(tags=["content", "text"])

        content_inputs = {
            "content": text,
            "source_language": kwargs.get("source_language", "en"),
            "target_language": kwargs.get("target_language", "en"),
            "target_audience": kwargs.get("target_audience", "general"),
            "target_pages": kwargs.get("target_pages", 20),
            "art_style": kwargs.get("art_style", "cartoon"),
            "content_type": "story",
        }

        content_result = self.content_crew.crew().kickoff(inputs=content_inputs)

        if settings.agentops_api_key:
            agentops.end_session("Success")

        if content_result.pydantic:
            comic_script = content_result.pydantic
        elif content_result.json_dict:
            comic_script = ComicScript(**content_result.json_dict)
        else:
            raise ValueError("Content generation failed: No structured output received")

        logger.info(f"Script created: {comic_script.total_panels} panels")

        # Stage 3: Generate visuals (parallel processing for panels)
        logger.info("Stage 3: Generating visuals...")
        if settings.agentops_api_key:
            agentops.start_session(tags=["visual", "generation"])

        # Create inputs for each panel
        panel_inputs = [
            {
                "panel_number": panel.panel_number,
                "page_number": panel.page_number,
                "description": panel.description,
                "mood": panel.mood,
                "camera_angle": panel.camera_angle,
                "art_style": kwargs.get("art_style", "cartoon"),
                "color_palette": comic_script.color_palette,
                "characters": [c.name for c in comic_script.characters]
                if hasattr(comic_script, "characters")
                else [],
                "story_summary": getattr(comic_script, "summary", ""),
            }
            for panel in comic_script.panels
        ]

        # Process panels (in batches to avoid overwhelming the API)
        panel_results = self.visual_crew.crew().kickoff_for_each(inputs=panel_inputs)

        if settings.agentops_api_key:
            agentops.end_session("Success")

        logger.info(f"Generated {len(panel_results)} panel artworks")

        # Stage 4: Synthesize final comic
        logger.info("Stage 4: Synthesizing final comic...")
        if settings.agentops_api_key:
            agentops.start_session(tags=["synthesis", "export"])

        synthesis_inputs = {
            "title": comic_script.title,
            "author": self.config.get("author", "AI Generated"),
            "script": comic_script,
            "panel_artworks": [r.pydantic for r in panel_results],
            "output_formats": kwargs.get("output_formats", ["pdf"]),
            "quality": self.config.get("quality", "high"),
        }

        final_result = self.synthesis_crew.crew().kickoff(inputs=synthesis_inputs)

        if settings.agentops_api_key:
            agentops.end_session("Success")

        final_comic = final_result.pydantic
        logger.info(f"Comic book generated successfully: {final_comic.title}")

        return final_comic

    def get_status(self, job_id: str) -> GenerationStatus:
        """
        Get generation status for a job.

        Args:
            job_id: Job ID

        Returns:
            GenerationStatus object
        """
        # TODO: Implement job tracking
        return GenerationStatus(
            job_id=job_id,
            status="unknown",
            progress=0.0,
            current_stage="",
            message="Job tracking not yet implemented",
        )


if __name__ == "__main__":
    # Example usage
    generator = ComicBookGenerator(
        config={"target_audience": "children", "quality": "high"}
    )

    result = generator.generate_from_pdf(
        pdf_path="example_story.pdf",
        target_language="en",
        art_style="cartoon",
        target_pages=10,
        output_formats=["pdf", "web"],
    )

    print(f"Comic generated: {result.title}")
    print(f"Total pages: {result.total_pages}")
    print(f"Output format: {result.format}")

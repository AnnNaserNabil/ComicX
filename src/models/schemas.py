"""
Data models and Pydantic schemas for the comic book generator.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, field_validator


# ============================================================================
# Processing Layer Models
# ============================================================================

class ProcessedDocument(BaseModel):
    """Processed document from PDF/text extraction"""
    source_type: str = Field(..., description="Type of source: pdf, text, raw")
    title: Optional[str] = Field(None, description="Document title")
    author: Optional[str] = Field(None, description="Document author")
    content: str = Field(..., description="Extracted text content")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Document metadata")
    extracted_images: List[str] = Field(default_factory=list, description="URLs or base64 images")
    structure: Dict[str, Any] = Field(default_factory=dict, description="Document structure")
    language: str = Field(default="en", description="Detected language")
    word_count: int = Field(..., description="Total word count")
    created_at: datetime = Field(default_factory=datetime.now)


class ValidationResult(BaseModel):
    """Content validation result"""
    is_valid: bool = Field(..., description="Whether content is valid")
    quality_score: float = Field(..., ge=0, le=100, description="Quality score 0-100")
    issues: List[str] = Field(default_factory=list, description="List of issues found")
    warnings: List[str] = Field(default_factory=list, description="List of warnings")
    suggestions: List[str] = Field(default_factory=list, description="Improvement suggestions")
    estimated_panels: int = Field(..., description="Estimated number of panels")
    estimated_pages: int = Field(..., description="Estimated number of pages")


# ============================================================================
# Content Generation Models
# ============================================================================

class TranslatedContent(BaseModel):
    """Translated and adapted content"""
    original_language: str = Field(..., description="Source language code")
    target_language: str = Field(..., description="Target language code")
    translated_text: str = Field(..., description="Translated content")
    adaptations: List[Dict[str, str]] = Field(
        default_factory=list,
        description="Cultural adaptations made"
    )
    preserved_terms: List[str] = Field(
        default_factory=list,
        description="Terms preserved from original"
    )
    translation_notes: List[str] = Field(
        default_factory=list,
        description="Notes about translation"
    )


class Character(BaseModel):
    """Character definition"""
    name: str = Field(..., description="Character name")
    description: str = Field(..., description="Character description")
    personality_traits: List[str] = Field(
        default_factory=list,
        description="Personality traits"
    )
    appearance: str = Field(..., description="Physical appearance description")
    role: str = Field(..., description="Role in story: protagonist, antagonist, supporting")


class StoryStructure(BaseModel):
    """Structured story with characters and arcs"""
    title: str = Field(..., description="Story title")
    genre: str = Field(..., description="Story genre")
    summary: str = Field(..., description="Story summary")
    themes: List[str] = Field(default_factory=list, description="Story themes")
    characters: List[Character] = Field(default_factory=list, description="Story characters")
    story_arcs: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Story arcs and plot points"
    )
    narrative_style: str = Field(..., description="Narrative style")
    target_audience: str = Field(..., description="Target audience")
    estimated_reading_time: int = Field(..., description="Estimated reading time in minutes")


class Panel(BaseModel):
    """Individual comic panel"""
    panel_number: int = Field(..., ge=1, description="Panel number")
    page_number: int = Field(..., ge=1, description="Page number")
    description: str = Field(..., description="Visual description for artist")
    dialogue: List[Dict[str, str]] = Field(
        default_factory=list,
        description="Dialogue: {character: text}"
    )
    captions: List[str] = Field(default_factory=list, description="Narrative captions")
    sound_effects: List[str] = Field(default_factory=list, description="Sound effects")
    camera_angle: str = Field(
        default="medium",
        description="Camera angle: close-up, medium, wide, etc."
    )
    mood: str = Field(..., description="Panel mood/atmosphere")
    key_elements: List[str] = Field(
        default_factory=list,
        description="Key visual elements"
    )


class PanelText(BaseModel):
    """Text elements for a comic panel"""
    panel_number: int = Field(..., description="Panel number")
    caption: Optional[str] = Field(None, description="Narrative caption")
    dialogue_lines: List[Dict[str, str]] = Field(
        default_factory=list,
        description="Dialogue: {character: text}"
    )
    sound_effects: List[str] = Field(default_factory=list, description="Sound effects")
    thought_bubbles: List[Dict[str, str]] = Field(
        default_factory=list,
        description="Thought bubbles: {character: thought}"
    )


class ComicScript(BaseModel):
    """Complete comic book script"""
    title: str = Field(..., description="Comic title")
    total_pages: int = Field(..., ge=1, description="Total number of pages")
    total_panels: int = Field(..., ge=1, description="Total number of panels")
    panels: List[Panel] = Field(..., description="All panels in order")
    style_guide: Dict[str, Any] = Field(
        default_factory=dict,
        description="Visual style guidelines"
    )
    color_palette: List[str] = Field(
        default_factory=list,
        description="Color palette hex codes"
    )
    notes: List[str] = Field(default_factory=list, description="Additional notes")


# ============================================================================
# Visual Generation Models
# ============================================================================

class PanelArtwork(BaseModel):
    """Generated artwork for a panel"""
    panel_number: int = Field(..., description="Panel number")
    page_number: int = Field(..., description="Page number")
    prompt: str = Field(..., description="Generation prompt used")
    image_url: str = Field(..., description="URL to generated image")
    image_data: Optional[str] = Field(None, description="Base64 image data if needed")
    generation_params: Dict[str, Any] = Field(
        default_factory=dict,
        description="Generation parameters"
    )
    style_tags: List[str] = Field(default_factory=list, description="Style tags")
    quality_score: float = Field(default=0.0, ge=0, le=100, description="Quality score")


class StyleAnalysis(BaseModel):
    """Style consistency analysis"""
    consistency_score: float = Field(..., ge=0, le=100, description="Overall consistency")
    character_consistency: Dict[str, float] = Field(
        default_factory=dict,
        description="Per-character consistency scores"
    )
    color_consistency: float = Field(..., ge=0, le=100, description="Color consistency")
    style_consistency: float = Field(..., ge=0, le=100, description="Art style consistency")
    inconsistencies: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Detected inconsistencies"
    )
    recommendations: List[str] = Field(
        default_factory=list,
        description="Recommendations for improvement"
    )


class ReferenceSheet(BaseModel):
    """Character/setting reference sheet"""
    character_name: str = Field(..., description="Character or setting name")
    reference_images: List[str] = Field(
        default_factory=list,
        description="Reference image URLs"
    )
    color_codes: List[str] = Field(default_factory=list, description="Color hex codes")
    key_features: List[str] = Field(default_factory=list, description="Key visual features")
    notes: str = Field(default="", description="Additional notes")


class PageLayout(BaseModel):
    """Comic page layout"""
    page_number: int = Field(..., ge=1, description="Page number")
    panels: List[Dict[str, Any]] = Field(..., description="Panel positions and sizes")
    speech_bubbles: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Speech bubble positions"
    )
    captions: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Caption positions"
    )
    sound_effects: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Sound effect positions"
    )
    layout_template: str = Field(..., description="Layout template used")
    rendered_page: str = Field(..., description="URL to rendered page")


# ============================================================================
# Synthesis & Output Models
# ============================================================================

class ComicBook(BaseModel):
    """Complete comic book"""
    title: str = Field(..., description="Comic title")
    author: str = Field(default="AI Generated", description="Author name")
    pages: List[str] = Field(..., description="URLs or paths to page images")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Comic metadata")
    total_pages: int = Field(..., ge=1, description="Total pages")
    file_size: int = Field(default=0, description="File size in bytes")
    format: str = Field(..., description="Output format: pdf, cbz, web")
    created_at: datetime = Field(default_factory=datetime.now)
    version: str = Field(default="1.0.0", description="Comic version")


class VideoClip(BaseModel):
    """Individual video clip"""
    clip_number: int = Field(..., description="Clip number")
    video_url: Optional[str] = Field(None, description="URL to video clip")
    request_id: Optional[str] = Field(None, description="Processing request ID")
    prompt: str = Field(..., description="Generation prompt")
    duration: float = Field(..., description="Duration in seconds")
    status: str = Field(default="pending", description="Status: pending, processing, completed, failed")


class VideoSequence(BaseModel):
    """Sequence of video clips for animated comic"""
    title: str = Field(..., description="Sequence title")
    clips: List[VideoClip] = Field(default_factory=list, description="Video clips")
    total_clips: int = Field(..., description="Total number of clips")
    total_duration: float = Field(default=0.0, description="Total duration in seconds")
    format: str = Field(default="mp4", description="Video format")
    created_at: datetime = Field(default_factory=datetime.now)


class QualityReport(BaseModel):
    """Quality assurance report"""
    overall_score: float = Field(..., ge=0, le=100, description="Overall quality score")
    completeness_check: bool = Field(..., description="All pages present")
    readability_score: float = Field(..., ge=0, le=100, description="Text readability")
    image_quality_score: float = Field(..., ge=0, le=100, description="Image quality")
    issues_found: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Issues found"
    )
    warnings: List[str] = Field(default_factory=list, description="Warnings")
    passed: bool = Field(..., description="Whether QA passed")
    recommendations: List[str] = Field(
        default_factory=list,
        description="Recommendations"
    )


# ============================================================================
# API Models
# ============================================================================

class GenerationRequest(BaseModel):
    """API request for comic generation"""
    source_type: str = Field(..., description="Source type: pdf, text, raw")
    content: Optional[str] = Field(None, description="Text content if source_type is text/raw")
    target_language: str = Field(default="en", description="Target language")
    art_style: str = Field(default="cartoon", description="Art style")
    target_pages: int = Field(default=20, ge=1, le=100, description="Target page count")
    target_audience: str = Field(default="general", description="Target audience")
    color_mode: str = Field(default="full-color", description="Color mode")
    output_formats: List[str] = Field(
        default_factory=lambda: ["pdf"],
        description="Output formats"
    )


class GenerationStatus(BaseModel):
    """Generation status response"""
    job_id: str = Field(..., description="Job ID")
    status: str = Field(..., description="Status: pending, processing, completed, failed")
    progress: float = Field(default=0.0, ge=0, le=100, description="Progress percentage")
    current_stage: str = Field(default="", description="Current processing stage")
    message: str = Field(default="", description="Status message")
    result: Optional[ComicBook] = Field(None, description="Result if completed")
    error: Optional[str] = Field(None, description="Error message if failed")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class HealthCheck(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    timestamp: datetime = Field(default_factory=datetime.now)
    services: Dict[str, str] = Field(
        default_factory=dict,
        description="Service statuses"
    )

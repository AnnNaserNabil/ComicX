"""
Multi-LLM utility for selecting appropriate language models for different tasks.
"""

import logging
from typing import Any, Dict, Optional

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

from src.models.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class LLMFactory:
    """Factory for creating LLM instances based on configuration"""
    
    @staticmethod
    def get_llm(
        task_type: str = "general",
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> Any:
        """
        Get appropriate LLM for the task type.
        
        Args:
            task_type: Type of task (story_generation, script_writing, captioning, dialogue, translation, general)
            temperature: Override default temperature
            max_tokens: Override default max tokens
            **kwargs: Additional LLM parameters
            
        Returns:
            LLM instance
        """
        # Determine which LLM to use based on task type
        llm_choice = settings.general_llm  # default to general setting
        
        if task_type == "story_generation":
            llm_choice = settings.story_generation_llm
        elif task_type == "script_writing":
            llm_choice = settings.script_writing_llm
        elif task_type == "captioning":
            llm_choice = settings.captioning_llm
        elif task_type == "dialogue":
            llm_choice = settings.dialogue_llm
        elif task_type == "translation":
            llm_choice = settings.translation_llm
        
        # Create appropriate LLM instance
        if llm_choice == "openai" and settings.openai_api_key:
            return LLMFactory._create_openai_llm(temperature, max_tokens, **kwargs)
        elif llm_choice == "openrouter" and settings.openrouter_api_key:
            return LLMFactory._create_openrouter_llm(temperature, max_tokens, **kwargs)
        else:
            # Default to Gemini (primary LLM)
            return LLMFactory._create_gemini_llm(temperature, max_tokens, **kwargs)
    
    @staticmethod
    def _create_openrouter_llm(
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> ChatOpenAI:
        """Create OpenRouter LLM instance using ChatOpenAI"""
        if not settings.openrouter_api_key:
            logger.warning("OpenRouter API key not configured, falling back to Gemini")
            return LLMFactory._create_gemini_llm(temperature, max_tokens, **kwargs)
        
        model = settings.openrouter_model
        if not model.startswith("openrouter/"):
            model = f"openrouter/{model}"
            
        return ChatOpenAI(
            model=model,
            api_key=settings.openrouter_api_key,
            base_url=settings.openrouter_base_url,
            temperature=temperature or settings.gemini_temperature,
            max_tokens=max_tokens or settings.gemini_max_tokens,
            **kwargs
        )
    
    @staticmethod
    def _create_gemini_llm(
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> ChatGoogleGenerativeAI:
        """Create Google Gemini LLM instance"""
        return ChatGoogleGenerativeAI(
            model=settings.gemini_model,
            google_api_key=settings.google_api_key,
            temperature=temperature or settings.gemini_temperature,
            max_output_tokens=max_tokens or settings.gemini_max_tokens,
            **kwargs
        )
    
    @staticmethod
    def _create_openai_llm(
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> ChatOpenAI:
        """Create OpenAI LLM instance (if API key is available)"""
        if not settings.openai_api_key:
            logger.warning("OpenAI API key not configured, falling back to Gemini")
            return LLMFactory._create_gemini_llm(temperature, max_tokens, **kwargs)
        
        return ChatOpenAI(
            model=settings.openai_model,
            api_key=settings.openai_api_key,
            temperature=temperature or settings.openai_temperature,
            max_tokens=max_tokens or settings.openai_max_tokens,
            **kwargs
        )
    
    @staticmethod
    def get_story_llm(**kwargs) -> Any:
        """Get LLM optimized for story generation (creative, long-form)"""
        return LLMFactory.get_llm(
            task_type="story_generation",
            temperature=0.9,  # High creativity
            **kwargs
        )
    
    @staticmethod
    def get_script_llm(**kwargs) -> Any:
        """Get LLM optimized for script writing (structured, detailed)"""
        return LLMFactory.get_llm(
            task_type="script_writing",
            temperature=0.7,  # Balanced
            **kwargs
        )
    
    @staticmethod
    def get_caption_llm(**kwargs) -> Any:
        """Get LLM optimized for captioning (concise, descriptive)"""
        return LLMFactory.get_llm(
            task_type="captioning",
            temperature=0.6,  # More focused
            **kwargs
        )
    
    @staticmethod
    def get_dialogue_llm(**kwargs) -> Any:
        """Get LLM optimized for dialogue (natural, character-appropriate)"""
        return LLMFactory.get_llm(
            task_type="dialogue",
            temperature=0.8,  # Creative but consistent
            **kwargs
        )
    
    @staticmethod
    def get_translation_llm(**kwargs) -> Any:
        """Get LLM optimized for translation (accurate, context-aware)"""
        return LLMFactory.get_llm(
            task_type="translation",
            temperature=0.5,  # More precise
            **kwargs
        )


class ChunkedStoryGenerator:
    """Generate stories in chunks for better quality and control"""
    
    def __init__(self, llm: Optional[Any] = None):
        self.llm = llm or LLMFactory.get_story_llm()
    
    def generate_story_outline(self, prompt: str, num_chapters: int = 5) -> Dict[str, Any]:
        """
        Generate story outline with chapters.
        
        Args:
            prompt: Story prompt or theme
            num_chapters: Number of chapters to create
            
        Returns:
            Story outline with chapter summaries
        """
        outline_prompt = f"""Create a detailed story outline for a comic book based on this prompt:

{prompt}

Generate an outline with {num_chapters} chapters. For each chapter, provide:
1. Chapter title
2. Brief summary (2-3 sentences)
3. Key events
4. Characters involved
5. Mood/tone

Format as JSON with this structure:
{{
    "title": "Story Title",
    "genre": "Genre",
    "themes": ["theme1", "theme2"],
    "chapters": [
        {{
            "number": 1,
            "title": "Chapter Title",
            "summary": "Chapter summary",
            "key_events": ["event1", "event2"],
            "characters": ["char1", "char2"],
            "mood": "mood description"
        }}
    ]
}}"""
        
        response = self.llm.invoke(outline_prompt)
        # Parse response (simplified - add proper JSON parsing)
        return {"outline": response.content}
    
    def generate_chapter_content(
        self,
        chapter_info: Dict[str, Any],
        previous_context: str = ""
    ) -> str:
        """
        Generate detailed content for a single chapter.
        
        Args:
            chapter_info: Chapter information from outline
            previous_context: Summary of previous chapters for continuity
            
        Returns:
            Detailed chapter content
        """
        context_section = f"\n\nPrevious chapters context:\n{previous_context}" if previous_context else ""
        
        chapter_prompt = f"""Write detailed content for this chapter of a comic book story:

Chapter {chapter_info.get('number')}: {chapter_info.get('title')}
Summary: {chapter_info.get('summary')}
Key Events: {', '.join(chapter_info.get('key_events', []))}
Characters: {', '.join(chapter_info.get('characters', []))}
Mood: {chapter_info.get('mood')}{context_section}

Write engaging narrative content that:
- Develops the characters
- Advances the plot
- Includes vivid descriptions for visual adaptation
- Maintains the specified mood
- Flows naturally from previous chapters

Length: 500-800 words"""
        
        response = self.llm.invoke(chapter_prompt)
        return response.content
    
    def generate_full_story(self, prompt: str, num_chapters: int = 5) -> Dict[str, Any]:
        """
        Generate complete story in chunks.
        
        Args:
            prompt: Story prompt
            num_chapters: Number of chapters
            
        Returns:
            Complete story with all chapters
        """
        logger.info(f"Generating story outline for: {prompt[:50]}...")
        outline = self.generate_story_outline(prompt, num_chapters)
        
        chapters = []
        previous_context = ""
        
        # Generate each chapter
        for i in range(num_chapters):
            chapter_info = {
                'number': i + 1,
                'title': f"Chapter {i + 1}",
                'summary': f"Chapter {i + 1} of the story",
                'key_events': [],
                'characters': [],
                'mood': 'engaging'
            }
            
            logger.info(f"Generating chapter {i + 1}/{num_chapters}...")
            chapter_content = self.generate_chapter_content(chapter_info, previous_context)
            
            chapters.append({
                'number': i + 1,
                'content': chapter_content
            })
            
            # Update context for next chapter
            previous_context += f"\nChapter {i + 1}: {chapter_content[:200]}..."
        
        return {
            'outline': outline,
            'chapters': chapters,
            'full_text': '\n\n'.join([c['content'] for c in chapters])
        }


class CaptionGenerator:
    """Generate captions for comic panels"""
    
    def __init__(self, llm: Optional[Any] = None):
        self.llm = llm or LLMFactory.get_caption_llm()
    
    def generate_panel_caption(
        self,
        panel_description: str,
        context: str = "",
        max_words: int = 20
    ) -> str:
        """
        Generate concise caption for a panel.
        
        Args:
            panel_description: Description of what's in the panel
            context: Story context
            max_words: Maximum words for caption
            
        Returns:
            Caption text
        """
        prompt = f"""Generate a concise, impactful caption for this comic panel:

Panel: {panel_description}
Context: {context}

Requirements:
- Maximum {max_words} words
- Engaging and descriptive
- Suitable for comic book narration
- Sets the scene or mood

Caption:"""
        
        response = self.llm.invoke(prompt)
        return response.content.strip()
    
    def generate_multiple_captions(
        self,
        panels: list,
        story_context: str = ""
    ) -> list:
        """Generate captions for multiple panels"""
        captions = []
        
        for i, panel in enumerate(panels):
            caption = self.generate_panel_caption(
                panel_description=panel.get('description', ''),
                context=story_context,
                max_words=20
            )
            captions.append({
                'panel_number': i + 1,
                'caption': caption
            })
        
        return captions


class DialogueGenerator:
    """Generate dialogue for comic characters"""
    
    def __init__(self, llm: Optional[Any] = None):
        self.llm = llm or LLMFactory.get_dialogue_llm()
    
    def generate_dialogue(
        self,
        characters: list,
        scene_description: str,
        context: str = "",
        num_exchanges: int = 3
    ) -> list:
        """
        Generate dialogue between characters.
        
        Args:
            characters: List of character names/descriptions
            scene_description: What's happening in the scene
            context: Story context
            num_exchanges: Number of dialogue exchanges
            
        Returns:
            List of dialogue exchanges
        """
        char_list = ', '.join(characters)
        
        prompt = f"""Generate natural dialogue for this comic book scene:

Characters: {char_list}
Scene: {scene_description}
Context: {context}

Generate {num_exchanges} exchanges of dialogue that:
- Sounds natural and character-appropriate
- Advances the scene
- Reveals character personality
- Is concise (comic book style)

Format as:
CHARACTER NAME: "Dialogue text"

Dialogue:"""
        
        response = self.llm.invoke(prompt)
        
        # Parse dialogue (simplified)
        dialogue_lines = []
        for line in response.content.split('\n'):
            if ':' in line and '"' in line:
                char, text = line.split(':', 1)
                dialogue_lines.append({
                    'character': char.strip(),
                    'text': text.strip().strip('"')
                })
        
        return dialogue_lines

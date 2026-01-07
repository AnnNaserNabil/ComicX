"""
Image and video generation tools using ModelsLab API.
"""

import base64
import io
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from crewai.tools import BaseTool
from modelslab_py.core.client import Client
from modelslab_py.core.apis.community import Community
from modelslab_py.core.apis.realtime import Realtime
from modelslab_py.core.apis.video import Video
from modelslab_py.schemas.community import Text2Image as CommunityText2Image
from modelslab_py.schemas.realtime import RealtimeText2ImageSchema
from modelslab_py.schemas.video import Text2Video
from PIL import Image
from pydantic import BaseModel, Field

from src.models.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class ImageGenerationResult(BaseModel):
    """Result from image generation"""
    image_url: str
    prompt: str
    model: str
    width: int
    height: int


class ModelsLabImageTool(BaseTool):
    """Tool for generating images using ModelsLab API"""
    
    name: str = "ModelsLab Image Generator"
    description: str = (
        "Generate images using ModelsLab's powerful AI models. "
        "Supports various styles including photorealistic, cartoon, anime, and more."
    )
    
    model: str = Field(default="flux")
    width: int = Field(default=1024)
    height: int = Field(default=1024)
    samples: int = Field(default=1)
    num_inference_steps: int = Field(default=30)
    guidance_scale: float = Field(default=7.5)
    use_community: bool = Field(default=True)
    
    # Internal state (excluded from schema)
    client: Any = Field(None, exclude=True)
    api: Any = Field(None, exclude=True)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = Client(api_key=settings.modelslab_api_key)
        
        if self.use_community:
            self.api = Community(client=self.client, enterprise=settings.modelslab_enterprise)
        else:
            self.api = Realtime(client=self.client, enterprise=settings.modelslab_enterprise)
    
    def _run(
        self,
        prompt: str,
        negative_prompt: Optional[str] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        seed: Optional[int] = None,
        style: Optional[str] = None
    ) -> ImageGenerationResult:
        """
        Generate image using ModelsLab.
        
        Args:
            prompt: Text description of image to generate
            negative_prompt: What to avoid in the image
            width: Image width (optional)
            height: Image height (optional)
            seed: Random seed for reproducibility (optional)
            style: Art style hint (optional)
            
        Returns:
            ImageGenerationResult with URL and metadata
        """
        try:
            # Enhance prompt with style if provided
            enhanced_prompt = prompt
            if style:
                enhanced_prompt = f"{prompt}, {style} style"
            
            # Use community models for better quality
            if self.use_community:
                schema = CommunityText2Image(
                    model_id=self.model,
                    prompt=enhanced_prompt,
                    negative_prompt=negative_prompt or "blurry, low quality, distorted, deformed, ugly",
                    width=width or self.width,
                    height=height or self.height,
                    samples=self.samples,
                    num_inference_steps=self.num_inference_steps,
                    guidance_scale=self.guidance_scale,
                    seed=seed
                )
                
                logger.info(f"Generating image with ModelsLab Community API: {prompt[:50]}...")
                response = self.api.text_to_image(schema)
            else:
                # Use realtime API for faster generation
                schema = RealtimeText2ImageSchema(
                    prompt=enhanced_prompt,
                    negative_prompt=negative_prompt or "blurry, low quality, distorted",
                    width=width or self.width,
                    height=height or self.height,
                    samples=self.samples,
                    num_inference_steps=self.num_inference_steps,
                    guidance_scale=self.guidance_scale,
                    seed=seed
                )
                
                logger.info(f"Generating image with ModelsLab Realtime API: {prompt[:50]}...")
                response = self.api.text_to_image(schema)
            
            # Handle response
            if response.get("status") == "success":
                image_url = response["output"][0]
                
                return ImageGenerationResult(
                    image_url=image_url,
                    prompt=enhanced_prompt,
                    model=self.model,
                    width=width or self.width,
                    height=height or self.height
                )
            elif response.get("status") == "processing":
                # For async processing, return the request ID
                logger.warning(f"Image generation is processing. Request ID: {response.get('id')}")
                return ImageGenerationResult(
                    image_url=f"processing:{response.get('id')}",
                    prompt=enhanced_prompt,
                    model=self.model,
                    width=width or self.width,
                    height=height or self.height
                )
            else:
                error_msg = response.get("message", "Unknown error")
                logger.error(f"Image generation failed: {error_msg}")
                raise Exception(f"ModelsLab API error: {error_msg}")
                
        except Exception as e:
            logger.error(f"Error generating image with ModelsLab: {e}")
            raise


class VideoGenerationResult(BaseModel):
    """Result from video generation"""
    video_url: Optional[str] = None
    request_id: Optional[str] = None
    status: str
    prompt: str
    model: str
    eta: Optional[int] = None


class ModelsLabVideoTool(BaseTool):
    """Tool for generating videos using ModelsLab API"""
    
    name: str = "ModelsLab Video Generator"
    description: str = (
        "Generate videos from text prompts or animate images using ModelsLab's AI models. "
        "Creates short video clips with smooth motion and cinematic quality."
    )
    
    model: str = Field(default="cogvideox")
    width: int = Field(default=512)
    height: int = Field(default=512)
    num_frames: int = Field(default=25)
    num_inference_steps: int = Field(default=20)
    guidance_scale: float = Field(default=7.0)
    
    # Internal state (excluded from schema)
    client: Any = Field(None, exclude=True)
    api: Any = Field(None, exclude=True)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = Client(api_key=settings.modelslab_api_key)
        self.api = Video(client=self.client, enterprise=settings.modelslab_enterprise)
    
    def _run(
        self,
        prompt: str,
        negative_prompt: Optional[str] = None,
        init_image: Optional[str] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        num_frames: Optional[int] = None
    ) -> VideoGenerationResult:
        """
        Generate video using ModelsLab.
        
        Args:
            prompt: Text description of video to generate
            negative_prompt: What to avoid in the video
            init_image: Optional starting image for image-to-video
            width: Video width (optional)
            height: Video height (optional)
            num_frames: Number of frames (optional)
            
        Returns:
            VideoGenerationResult with URL or request ID
        """
        try:
            schema = Text2Video(
                model_id=self.model,
                prompt=prompt,
                negative_prompt=negative_prompt or "low quality, blurry, static, choppy",
                width=width or self.width,
                height=height or self.height,
                num_frames=num_frames or self.num_frames,
                num_inference_steps=self.num_inference_steps,
                guidance_scale=self.guidance_scale
            )
            
            logger.info(f"Generating video with ModelsLab: {prompt[:50]}...")
            response = self.api.text_to_video(schema)
            
            # Video generation is typically async
            if response.get("status") == "success":
                return VideoGenerationResult(
                    video_url=response["output"][0],
                    status="success",
                    prompt=prompt,
                    model=self.model
                )
            elif response.get("status") == "processing":
                return VideoGenerationResult(
                    request_id=response.get("id"),
                    status="processing",
                    prompt=prompt,
                    model=self.model,
                    eta=response.get("eta")
                )
            else:
                error_msg = response.get("message", "Unknown error")
                logger.error(f"Video generation failed: {error_msg}")
                raise Exception(f"ModelsLab API error: {error_msg}")
                
        except Exception as e:
            logger.error(f"Error generating video with ModelsLab: {e}")
            raise


class ImageProcessorTool(BaseTool):
    """Tool for image processing and manipulation"""
    
    name: str = "Image Processor"
    description: str = (
        "Process and manipulate images: resize, crop, convert formats, "
        "and perform basic image operations."
    )
    
    def _run(
        self,
        image_path: str,
        operation: str,
        **kwargs
    ) -> str:
        """
        Process image with specified operation.
        
        Args:
            image_path: Path to image file
            operation: Operation to perform (resize, crop, convert, etc.)
            **kwargs: Operation-specific parameters
            
        Returns:
            Path to processed image
        """
        try:
            img_path = Path(image_path)
            if not img_path.exists():
                raise FileNotFoundError(f"Image not found: {image_path}")
            
            # Load image
            img = Image.open(img_path)
            
            # Perform operation
            if operation == "resize":
                img = self._resize(img, **kwargs)
            elif operation == "crop":
                img = self._crop(img, **kwargs)
            elif operation == "convert":
                img = self._convert(img, **kwargs)
            elif operation == "optimize":
                img = self._optimize(img, **kwargs)
            else:
                raise ValueError(f"Unknown operation: {operation}")
            
            # Save processed image
            output_path = kwargs.get('output_path', img_path.with_stem(f"{img_path.stem}_processed"))
            img.save(output_path)
            
            logger.info(f"Processed image saved to {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"Error processing image: {e}")
            raise
    
    def _resize(self, img: Image.Image, width: int, height: int, **kwargs) -> Image.Image:
        """Resize image"""
        return img.resize((width, height), Image.Resampling.LANCZOS)
    
    def _crop(self, img: Image.Image, left: int, top: int, right: int, bottom: int, **kwargs) -> Image.Image:
        """Crop image"""
        return img.crop((left, top, right, bottom))
    
    def _convert(self, img: Image.Image, mode: str, **kwargs) -> Image.Image:
        """Convert image mode"""
        return img.convert(mode)
    
    def _optimize(self, img: Image.Image, **kwargs) -> Image.Image:
        """Optimize image"""
        # Convert to RGB if needed
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = background
        
        return img

"""
Comic panel layout and typography tools.
"""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from crewai.tools import BaseTool
from PIL import Image, ImageDraw, ImageFont
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class LayoutConfig(BaseModel):
    """Layout configuration"""
    page_width: int = 1200
    page_height: int = 1600
    margin: int = 50
    gutter: int = 20
    background_color: str = "white"


class PanelPosition(BaseModel):
    """Panel position and size"""
    x: int
    y: int
    width: int
    height: int


class TextElement(BaseModel):
    """Text element (speech bubble, caption, etc.)"""
    text: str
    x: int
    y: int
    width: int
    height: int
    element_type: str  # speech_bubble, caption, sound_effect
    font_size: int = 16
    font_color: str = "black"


class ComicLayoutTool(BaseTool):
    """Tool for creating comic page layouts"""
    
    name: str = "Comic Layout Designer"
    description: str = (
        "Create professional comic book page layouts with panels, "
        "speech bubbles, captions, and sound effects."
    )
    
    def _run(
        self,
        panels: List[Dict[str, Any]],
        layout_style: str = "grid",
        config: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Create comic page layout.
        
        Args:
            panels: List of panel data with images and positions
            layout_style: Layout style (grid, dynamic, traditional)
            config: Layout configuration
            
        Returns:
            Path to rendered page image
        """
        try:
            # Parse configuration
            layout_config = LayoutConfig(**(config or {}))
            
            # Create blank page
            page = Image.new(
                'RGB',
                (layout_config.page_width, layout_config.page_height),
                layout_config.background_color
            )
            
            # Calculate panel positions
            panel_positions = self._calculate_positions(
                len(panels),
                layout_style,
                layout_config
            )
            
            # Place panels on page
            for panel_data, position in zip(panels, panel_positions):
                self._place_panel(page, panel_data, position)
            
            # Add text elements
            for panel_data in panels:
                if 'text_elements' in panel_data:
                    for text_elem in panel_data['text_elements']:
                        self._add_text_element(page, text_elem)
            
            # Save page
            output_path = Path(f"/tmp/page_{id(page)}.png")
            page.save(output_path, quality=95)
            
            logger.info(f"Created page layout: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"Error creating layout: {e}")
            raise
    
    def _calculate_positions(
        self,
        num_panels: int,
        layout_style: str,
        config: LayoutConfig
    ) -> List[PanelPosition]:
        """Calculate panel positions based on layout style"""
        
        positions = []
        
        if layout_style == "grid":
            positions = self._grid_layout(num_panels, config)
        elif layout_style == "dynamic":
            positions = self._dynamic_layout(num_panels, config)
        elif layout_style == "traditional":
            positions = self._traditional_layout(num_panels, config)
        else:
            # Default to grid
            positions = self._grid_layout(num_panels, config)
        
        return positions
    
    def _grid_layout(self, num_panels: int, config: LayoutConfig) -> List[PanelPosition]:
        """Create grid-based layout"""
        positions = []
        
        # Calculate grid dimensions
        cols = 2 if num_panels > 1 else 1
        rows = (num_panels + cols - 1) // cols
        
        # Calculate panel dimensions
        available_width = config.page_width - (2 * config.margin) - ((cols - 1) * config.gutter)
        available_height = config.page_height - (2 * config.margin) - ((rows - 1) * config.gutter)
        
        panel_width = available_width // cols
        panel_height = available_height // rows
        
        # Create positions
        for i in range(num_panels):
            row = i // cols
            col = i % cols
            
            x = config.margin + col * (panel_width + config.gutter)
            y = config.margin + row * (panel_height + config.gutter)
            
            positions.append(PanelPosition(
                x=x, y=y,
                width=panel_width,
                height=panel_height
            ))
        
        return positions
    
    def _dynamic_layout(self, num_panels: int, config: LayoutConfig) -> List[PanelPosition]:
        """Create dynamic layout with varying panel sizes"""
        # Simplified dynamic layout
        # TODO: Implement more sophisticated dynamic layouts
        return self._grid_layout(num_panels, config)
    
    def _traditional_layout(self, num_panels: int, config: LayoutConfig) -> List[PanelPosition]:
        """Create traditional comic book layout"""
        # Simplified traditional layout
        # TODO: Implement traditional comic layouts (3-4 panels per page)
        return self._grid_layout(num_panels, config)
    
    def _place_panel(
        self,
        page: Image.Image,
        panel_data: Dict[str, Any],
        position: PanelPosition
    ) -> None:
        """Place panel image on page"""
        try:
            # Load panel image
            panel_image_path = panel_data.get('image_path')
            if not panel_image_path:
                return
            
            panel_img = Image.open(panel_image_path)
            
            # Resize to fit position
            panel_img = panel_img.resize(
                (position.width, position.height),
                Image.Resampling.LANCZOS
            )
            
            # Paste on page
            page.paste(panel_img, (position.x, position.y))
            
            # Draw border
            draw = ImageDraw.Draw(page)
            draw.rectangle(
                [position.x, position.y, position.x + position.width, position.y + position.height],
                outline="black",
                width=2
            )
            
        except Exception as e:
            logger.warning(f"Could not place panel: {e}")
    
    def _add_text_element(self, page: Image.Image, text_elem: Dict[str, Any]) -> None:
        """Add text element to page"""
        try:
            draw = ImageDraw.Draw(page)
            
            elem_type = text_elem.get('element_type', 'caption')
            text = text_elem.get('text', '')
            x = text_elem.get('x', 0)
            y = text_elem.get('y', 0)
            font_size = text_elem.get('font_size', 16)
            
            # Load font (use default if custom font not available)
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
            except:
                font = ImageFont.load_default()
            
            # Draw based on element type
            if elem_type == 'speech_bubble':
                self._draw_speech_bubble(draw, text, x, y, font)
            elif elem_type == 'caption':
                self._draw_caption(draw, text, x, y, font)
            elif elem_type == 'sound_effect':
                self._draw_sound_effect(draw, text, x, y, font)
            
        except Exception as e:
            logger.warning(f"Could not add text element: {e}")
    
    def _draw_speech_bubble(
        self,
        draw: ImageDraw.ImageDraw,
        text: str,
        x: int,
        y: int,
        font: ImageFont.FreeTypeFont
    ) -> None:
        """Draw speech bubble"""
        # Get text size
        bbox = draw.textbbox((x, y), text, font=font)
        padding = 10
        
        # Draw bubble background
        draw.ellipse(
            [bbox[0] - padding, bbox[1] - padding, bbox[2] + padding, bbox[3] + padding],
            fill="white",
            outline="black",
            width=2
        )
        
        # Draw text
        draw.text((x, y), text, fill="black", font=font)
    
    def _draw_caption(
        self,
        draw: ImageDraw.ImageDraw,
        text: str,
        x: int,
        y: int,
        font: ImageFont.FreeTypeFont
    ) -> None:
        """Draw caption box"""
        bbox = draw.textbbox((x, y), text, font=font)
        padding = 5
        
        # Draw box
        draw.rectangle(
            [bbox[0] - padding, bbox[1] - padding, bbox[2] + padding, bbox[3] + padding],
            fill="white",
            outline="black",
            width=1
        )
        
        # Draw text
        draw.text((x, y), text, fill="black", font=font)
    
    def _draw_sound_effect(
        self,
        draw: ImageDraw.ImageDraw,
        text: str,
        x: int,
        y: int,
        font: ImageFont.FreeTypeFont
    ) -> None:
        """Draw sound effect text"""
        # Draw bold outlined text for sound effects
        # Draw outline
        for offset_x in [-2, 0, 2]:
            for offset_y in [-2, 0, 2]:
                draw.text((x + offset_x, y + offset_y), text, fill="black", font=font)
        
        # Draw main text
        draw.text((x, y), text, fill="yellow", font=font)


class TypographyTool(BaseTool):
    """Tool for comic book typography"""
    
    name: str = "Typography Designer"
    description: str = (
        "Design and apply typography for comic books including "
        "dialogue, captions, and sound effects."
    )
    
    def _run(
        self,
        text: str,
        text_type: str,
        style: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Design typography for text element.
        
        Args:
            text: Text content
            text_type: Type of text (dialogue, caption, sound_effect)
            style: Style parameters
            
        Returns:
            Typography configuration
        """
        style = style or {}
        
        # Default styles for different text types
        defaults = {
            'dialogue': {
                'font_family': 'DejaVu Sans',
                'font_size': 16,
                'font_weight': 'normal',
                'color': 'black',
                'background': 'white',
                'border': True
            },
            'caption': {
                'font_family': 'DejaVu Sans',
                'font_size': 14,
                'font_weight': 'normal',
                'color': 'black',
                'background': 'lightyellow',
                'border': True
            },
            'sound_effect': {
                'font_family': 'DejaVu Sans Bold',
                'font_size': 24,
                'font_weight': 'bold',
                'color': 'red',
                'background': None,
                'border': False,
                'outline': True
            }
        }
        
        # Merge with provided style
        config = defaults.get(text_type, defaults['dialogue']).copy()
        config.update(style)
        config['text'] = text
        config['text_type'] = text_type
        
        return config

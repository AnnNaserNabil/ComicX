"""
PDF processing tools for extracting text, images, and metadata.
"""

import io
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

import pdfplumber
import PyPDF2
from crewai.tools import BaseTool
from PIL import Image
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class PDFExtractionResult(BaseModel):
    """Result from PDF extraction"""
    text: str
    images: List[str]
    metadata: Dict[str, Any]
    page_count: int
    word_count: int


class PDFProcessorTool(BaseTool):
    """Tool for processing PDF documents"""
    
    name: str = "PDF Processor"
    description: str = (
        "Extract text, images, and metadata from PDF documents. "
        "Returns structured data including content, images, and document information."
    )
    
    def _run(self, pdf_path: str) -> PDFExtractionResult:
        """
        Extract content from PDF file.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            PDFExtractionResult with extracted content
        """
        try:
            pdf_file = Path(pdf_path)
            if not pdf_file.exists():
                raise FileNotFoundError(f"PDF file not found: {pdf_path}")
            
            # Extract text using pdfplumber
            text_content = self._extract_text(pdf_file)
            
            # Extract images
            images = self._extract_images(pdf_file)
            
            # Extract metadata using PyPDF2
            metadata = self._extract_metadata(pdf_file)
            
            # Calculate word count
            word_count = len(text_content.split())
            
            return PDFExtractionResult(
                text=text_content,
                images=images,
                metadata=metadata,
                page_count=metadata.get("page_count", 0),
                word_count=word_count
            )
            
        except Exception as e:
            logger.error(f"Error processing PDF: {e}")
            raise
    
    def _extract_text(self, pdf_path: Path) -> str:
        """Extract text from PDF using pdfplumber"""
        text_parts = []
        
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    text_parts.append(text)
        
        return "\n\n".join(text_parts)
    
    def _extract_images(self, pdf_path: Path) -> List[str]:
        """Extract images from PDF"""
        images = []
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    if hasattr(page, 'images'):
                        for img_idx, img in enumerate(page.images):
                            # Store image reference
                            images.append(f"page_{page_num}_img_{img_idx}")
        except Exception as e:
            logger.warning(f"Could not extract images: {e}")
        
        return images
    
    def _extract_metadata(self, pdf_path: Path) -> Dict[str, Any]:
        """Extract metadata from PDF"""
        metadata = {}
        
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                # Get basic metadata
                if pdf_reader.metadata:
                    metadata.update({
                        'title': pdf_reader.metadata.get('/Title', ''),
                        'author': pdf_reader.metadata.get('/Author', ''),
                        'subject': pdf_reader.metadata.get('/Subject', ''),
                        'creator': pdf_reader.metadata.get('/Creator', ''),
                        'producer': pdf_reader.metadata.get('/Producer', ''),
                    })
                
                # Get page count
                metadata['page_count'] = len(pdf_reader.pages)
                
        except Exception as e:
            logger.warning(f"Could not extract metadata: {e}")
        
        return metadata


class TextProcessorTool(BaseTool):
    """Tool for processing plain text files"""
    
    name: str = "Text Processor"
    description: str = (
        "Process plain text files and extract content. "
        "Handles encoding detection and text normalization."
    )
    
    def _run(self, text_path: Optional[str] = None, text_content: Optional[str] = None) -> str:
        """
        Process text file or content.
        
        Args:
            text_path: Path to text file (optional)
            text_content: Raw text content (optional)
            
        Returns:
            Processed text content
        """
        if text_path:
            return self._process_file(text_path)
        elif text_content:
            return self._normalize_text(text_content)
        else:
            raise ValueError("Either text_path or text_content must be provided")
    
    def _process_file(self, text_path: str) -> str:
        """Process text file"""
        file_path = Path(text_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Text file not found: {text_path}")
        
        # Try different encodings
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                return self._normalize_text(content)
            except UnicodeDecodeError:
                continue
        
        raise ValueError(f"Could not decode file with any supported encoding: {text_path}")
    
    def _normalize_text(self, text: str) -> str:
        """Normalize text content"""
        # Remove excessive whitespace
        lines = [line.strip() for line in text.split('\n')]
        lines = [line for line in lines if line]
        
        # Join with proper spacing
        normalized = '\n\n'.join(lines)
        
        return normalized

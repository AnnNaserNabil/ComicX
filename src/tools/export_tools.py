"""
Export tools for generating various output formats.
"""

import io
import logging
import zipfile
from pathlib import Path
from typing import Any, Dict, List, Optional

from crewai.tools import BaseTool
from PIL import Image
from pydantic import BaseModel
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

logger = logging.getLogger(__name__)


class ExportResult(BaseModel):
    """Export operation result"""
    format: str
    output_path: str
    file_size: int
    page_count: int


class PDFExportTool(BaseTool):
    """Tool for exporting comics to PDF format"""
    
    name: str = "PDF Exporter"
    description: str = (
        "Export comic book pages to PDF format with proper sizing and quality."
    )
    
    def _run(
        self,
        pages: List[str],
        output_path: str,
        title: str = "Comic Book",
        author: str = "AI Generated",
        page_size: tuple = letter
    ) -> ExportResult:
        """
        Export pages to PDF.
        
        Args:
            pages: List of image paths
            output_path: Output PDF path
            title: PDF title
            author: PDF author
            page_size: Page size (default: letter)
            
        Returns:
            ExportResult with file information
        """
        try:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Create PDF
            c = canvas.Canvas(str(output_file), pagesize=page_size)
            
            # Set metadata
            c.setTitle(title)
            c.setAuthor(author)
            c.setSubject("AI Generated Comic Book")
            
            # Add pages
            for page_path in pages:
                try:
                    # Load image
                    img = Image.open(page_path)
                    
                    # Calculate dimensions to fit page
                    page_width, page_height = page_size
                    img_width, img_height = img.size
                    
                    # Calculate scaling
                    scale = min(page_width / img_width, page_height / img_height)
                    new_width = img_width * scale
                    new_height = img_height * scale
                    
                    # Center image on page
                    x = (page_width - new_width) / 2
                    y = (page_height - new_height) / 2
                    
                    # Draw image
                    c.drawImage(
                        page_path,
                        x, y,
                        width=new_width,
                        height=new_height,
                        preserveAspectRatio=True
                    )
                    
                    c.showPage()
                    
                except Exception as e:
                    logger.warning(f"Could not add page {page_path}: {e}")
            
            # Save PDF
            c.save()
            
            # Get file size
            file_size = output_file.stat().st_size
            
            logger.info(f"Exported PDF: {output_file} ({file_size} bytes)")
            
            return ExportResult(
                format="pdf",
                output_path=str(output_file),
                file_size=file_size,
                page_count=len(pages)
            )
            
        except Exception as e:
            logger.error(f"Error exporting PDF: {e}")
            raise


class CBZExportTool(BaseTool):
    """Tool for exporting comics to CBZ (Comic Book ZIP) format"""
    
    name: str = "CBZ Exporter"
    description: str = (
        "Export comic book pages to CBZ format (ZIP archive of images)."
    )
    
    def _run(
        self,
        pages: List[str],
        output_path: str,
        title: str = "Comic Book"
    ) -> ExportResult:
        """
        Export pages to CBZ.
        
        Args:
            pages: List of image paths
            output_path: Output CBZ path
            title: Comic title
            
        Returns:
            ExportResult with file information
        """
        try:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Ensure .cbz extension
            if output_file.suffix.lower() != '.cbz':
                output_file = output_file.with_suffix('.cbz')
            
            # Create CBZ (ZIP file)
            with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as cbz:
                for idx, page_path in enumerate(pages, 1):
                    try:
                        # Add page with numbered filename
                        page_file = Path(page_path)
                        archive_name = f"page_{idx:03d}{page_file.suffix}"
                        cbz.write(page_path, archive_name)
                        
                    except Exception as e:
                        logger.warning(f"Could not add page {page_path}: {e}")
                
                # Add metadata file
                metadata = f"Title: {title}\nPages: {len(pages)}\n"
                cbz.writestr("ComicInfo.txt", metadata)
            
            # Get file size
            file_size = output_file.stat().st_size
            
            logger.info(f"Exported CBZ: {output_file} ({file_size} bytes)")
            
            return ExportResult(
                format="cbz",
                output_path=str(output_file),
                file_size=file_size,
                page_count=len(pages)
            )
            
        except Exception as e:
            logger.error(f"Error exporting CBZ: {e}")
            raise


class WebExportTool(BaseTool):
    """Tool for exporting comics to web-friendly format"""
    
    name: str = "Web Exporter"
    description: str = (
        "Export comic book pages to web-friendly format with HTML viewer."
    )
    
    def _run(
        self,
        pages: List[str],
        output_dir: str,
        title: str = "Comic Book",
        optimize: bool = True
    ) -> ExportResult:
        """
        Export pages for web viewing.
        
        Args:
            pages: List of image paths
            output_dir: Output directory
            title: Comic title
            optimize: Whether to optimize images for web
            
        Returns:
            ExportResult with file information
        """
        try:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            # Create images directory
            images_dir = output_path / "images"
            images_dir.mkdir(exist_ok=True)
            
            # Process and copy images
            total_size = 0
            web_pages = []
            
            for idx, page_path in enumerate(pages, 1):
                try:
                    img = Image.open(page_path)
                    
                    # Optimize for web if requested
                    if optimize:
                        # Convert to RGB if needed
                        if img.mode in ('RGBA', 'LA', 'P'):
                            background = Image.new('RGB', img.size, (255, 255, 255))
                            if img.mode == 'P':
                                img = img.convert('RGBA')
                            background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                            img = background
                        
                        # Resize if too large
                        max_width = 1200
                        if img.width > max_width:
                            ratio = max_width / img.width
                            new_height = int(img.height * ratio)
                            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
                    
                    # Save optimized image
                    web_page_path = images_dir / f"page_{idx:03d}.jpg"
                    img.save(web_page_path, "JPEG", quality=85, optimize=True)
                    
                    web_pages.append(f"images/page_{idx:03d}.jpg")
                    total_size += web_page_path.stat().st_size
                    
                except Exception as e:
                    logger.warning(f"Could not process page {page_path}: {e}")
            
            # Create HTML viewer
            html_content = self._generate_html(title, web_pages)
            html_path = output_path / "index.html"
            html_path.write_text(html_content)
            
            logger.info(f"Exported web comic: {output_path}")
            
            return ExportResult(
                format="web",
                output_path=str(html_path),
                file_size=total_size,
                page_count=len(web_pages)
            )
            
        except Exception as e:
            logger.error(f"Error exporting web comic: {e}")
            raise
    
    def _generate_html(self, title: str, pages: List[str]) -> str:
        """Generate HTML viewer"""
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: Arial, sans-serif;
            background: #1a1a1a;
            color: white;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        h1 {{
            text-align: center;
            margin-bottom: 30px;
            color: #fff;
        }}
        .page {{
            margin-bottom: 20px;
            text-align: center;
        }}
        .page img {{
            max-width: 100%;
            height: auto;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }}
        .page-number {{
            margin-top: 10px;
            color: #888;
        }}
        .navigation {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: rgba(0,0,0,0.8);
            padding: 10px 20px;
            border-radius: 5px;
        }}
        button {{
            background: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            margin: 0 5px;
            cursor: pointer;
            border-radius: 3px;
        }}
        button:hover {{
            background: #45a049;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        <div id="comic-viewer">
"""
        
        for idx, page in enumerate(pages, 1):
            html += f"""
            <div class="page" id="page-{idx}">
                <img src="{page}" alt="Page {idx}">
                <div class="page-number">Page {idx} of {len(pages)}</div>
            </div>
"""
        
        html += """
        </div>
    </div>
    <div class="navigation">
        <button onclick="scrollToTop()">↑ Top</button>
        <button onclick="scrollToBottom()">↓ Bottom</button>
    </div>
    <script>
        function scrollToTop() {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
        function scrollToBottom() {
            window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
        }
    </script>
</body>
</html>
"""
        
        return html


class ExportManager:
    """Manage multiple export formats"""
    
    def __init__(self):
        self.pdf_exporter = PDFExportTool()
        self.cbz_exporter = CBZExportTool()
        self.web_exporter = WebExportTool()
    
    def export_all(
        self,
        pages: List[str],
        output_dir: Path,
        title: str,
        formats: List[str]
    ) -> Dict[str, ExportResult]:
        """Export to multiple formats"""
        results = {}
        
        for format_name in formats:
            try:
                if format_name == "pdf":
                    result = self.pdf_exporter._run(
                        pages,
                        str(output_dir / f"{title}.pdf"),
                        title=title
                    )
                    results["pdf"] = result
                    
                elif format_name == "cbz":
                    result = self.cbz_exporter._run(
                        pages,
                        str(output_dir / f"{title}.cbz"),
                        title=title
                    )
                    results["cbz"] = result
                    
                elif format_name == "web":
                    result = self.web_exporter._run(
                        pages,
                        str(output_dir / "web"),
                        title=title
                    )
                    results["web"] = result
                    
            except Exception as e:
                logger.error(f"Error exporting to {format_name}: {e}")
        
        return results

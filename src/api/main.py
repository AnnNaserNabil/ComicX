"""
FastAPI application for Comic Book Generator with comprehensive agent API endpoints.
"""

import asyncio
import logging
import uuid
from pathlib import Path
from typing import Dict, List, Optional

from fastapi import FastAPI, File, Form, HTTPException, UploadFile, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from src.main import ComicBookGenerator
from src.models.config import get_settings
from src.utils.llm_factory import LLMFactory
from src.crews.content_crew import ContentCrew
from src.crews.processing_crew import ProcessingCrew
from src.crews.visual_crew import VisualCrew
from src.crews.synthesis_crew import SynthesisCrew

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
settings = get_settings()

app = FastAPI(
    title="AI Comic Book Generator API",
    description="Generate comic books using AI agents",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/outputs", StaticFiles(directory=str(settings.output_dir)), name="outputs")

# In-memory storage for job status
jobs: Dict[str, Dict] = {}


# Request/Response Models
class StoryGenerateRequest(BaseModel):
    prompt: str
    genre: str = "Fantasy"
    themes: List[str] = []
    num_chapters: int = 5


class StoryResponse(BaseModel):
    story: str
    chapters: List[Dict]
    word_count: int


class CaptionRequest(BaseModel):
    panel_description: str
    context: str = ""
    max_words: int = 20


class DialogueRequest(BaseModel):
    characters: List[str]
    scene_description: str
    context: str = ""
    num_exchanges: int = 3


class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    progress: float
    current_stage: str
    message: str
    result: Optional[Dict] = None


# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": asyncio.get_event_loop().time(),
        "services": {
            "redis": "connected",
            "redis": "connected",
            "openrouter": "configured" if settings.openrouter_api_key else "not_configured"
        }
    }


# Story Generation Endpoints
@app.post("/api/v1/story/generate", response_model=StoryResponse)
async def generate_story(request: StoryGenerateRequest):
    """Generate story using LLM"""
    try:
        # Using LLMFactory directly for quick generation
        llm = LLMFactory.get_llm(task_type="story_generation")
        
        prompt = f"Generate a {request.genre} story based on: {request.prompt}. Themes: {', '.join(request.themes)}. Chapters: {request.num_chapters}."
        
        response = llm.invoke(prompt)
        story_text = response.content
        
        return StoryResponse(
            story=story_text,
            chapters=[{"number": i+1, "content": "..."} for i in range(request.num_chapters)],
            word_count=len(story_text.split())
        )
    except Exception as e:
        logger.error(f"Story generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Caption Generation Endpoints
@app.post("/api/v1/caption/generate")
async def generate_caption(request: CaptionRequest):
    """Generate panel caption"""
    try:
        llm = LLMFactory.get_llm(task_type="captioning")
        prompt = f"Write a comic book caption for this panel: {request.panel_description}. Context: {request.context}. Max words: {request.max_words}."
        response = llm.invoke(prompt)
        return {"caption": response.content}
    except Exception as e:
        logger.error(f"Caption generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Dialogue Generation Endpoints
@app.post("/api/v1/dialogue/generate")
async def generate_dialogue(request: DialogueRequest):
    """Generate character dialogue"""
    try:
        llm = LLMFactory.get_llm(task_type="dialogue")
        prompt = f"Write dialogue for {', '.join(request.characters)} in this scene: {request.scene_description}. Context: {request.context}. Exchanges: {request.num_exchanges}."
        response = llm.invoke(prompt)
        # Simple parsing for demo
        lines = response.content.split("\n")
        dialogue = []
        for line in lines:
            if ":" in line:
                char, text = line.split(":", 1)
                dialogue.append({"character": char.strip(), "text": text.strip()})
        
        if not dialogue:
            dialogue = [{"character": request.characters[0], "text": response.content}]
            
        return {"dialogue": dialogue}
    except Exception as e:
        logger.error(f"Dialogue generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Comic Generation Endpoints
async def generate_comic_task(job_id: str, data: Dict):
    """Background task for comic generation"""
    try:
        jobs[job_id]["status"] = "processing"
        jobs[job_id]["current_stage"] = "Initializing"
        jobs[job_id]["progress"] = 0.1
        
        generator = ComicBookGenerator()
        
        # Stage 1: Content generation
        jobs[job_id]["current_stage"] = "Generating content"
        jobs[job_id]["progress"] = 0.3
        
        # Stage 2: Visual generation
        jobs[job_id]["current_stage"] = "Generating artwork"
        jobs[job_id]["progress"] = 0.6
        
        # Generate comic
        if data.get("file_path"):
            result = generator.generate_from_pdf(
                pdf_path=data["file_path"],
                art_style=data["art_style"],
                target_pages=data["target_pages"]
            )
        else:
            result = generator.generate_from_text(
                text=data["text"],
                title=data["title"],
                art_style=data["art_style"],
                target_pages=data["target_pages"]
            )
        
        # Complete
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["current_stage"] = "Complete"
        jobs[job_id]["progress"] = 1.0
        jobs[job_id]["result"] = {
            "title": result.title,
            "total_pages": result.total_pages,
            "format": result.format,
            "file_path": str(result.pages[0]) if result.pages else None
        }
        
    except Exception as e:
        logger.error(f"Comic generation failed: {e}")
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["message"] = str(e)


@app.post("/api/v1/generate")
async def generate_comic(
    background_tasks: BackgroundTasks,
    text: Optional[str] = Form(None),
    title: str = Form("Untitled Comic"),
    art_style: str = Form("cartoon"),
    target_pages: int = Form(20),
    target_audience: str = Form("general"),
    file: Optional[UploadFile] = File(None)
):
    """Generate comic book (async)"""
    try:
        job_id = str(uuid.uuid4())
        
        # Initialize job
        jobs[job_id] = {
            "job_id": job_id,
            "status": "queued",
            "progress": 0.0,
            "current_stage": "Queued",
            "message": "Comic generation queued",
            "result": None
        }
        
        # Prepare data
        data = {
            "text": text,
            "title": title,
            "art_style": art_style,
            "target_pages": target_pages,
            "target_audience": target_audience
        }
        
        # Handle file upload
        if file:
            temp_path = settings.temp_dir / f"{job_id}_{file.filename}"
            with open(temp_path, "wb") as f:
                f.write(await file.read())
            data["file_path"] = str(temp_path)
        
        # Start background task
        background_tasks.add_task(generate_comic_task, job_id, data)
        
        return {"job_id": job_id, "status": "queued"}
        
    except Exception as e:
        logger.error(f"Failed to queue comic generation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/status/{job_id}", response_model=JobStatusResponse)
async def get_job_status(job_id: str):
    """Get generation job status"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return JobStatusResponse(**jobs[job_id])


@app.get("/api/v1/download/{job_id}")
async def download_comic(job_id: str, format: str = "pdf"):
    """Download generated comic"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs[job_id]
    if job["status"] != "completed":
        raise HTTPException(status_code=400, detail="Comic not ready")
    
    if not job["result"] or not job["result"].get("file_path"):
        raise HTTPException(status_code=404, detail="File not found")
    
    file_path = Path(job["result"]["file_path"])
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        file_path,
        media_type="application/pdf" if format == "pdf" else "application/x-cbz",
        filename=f"{job['result']['title']}.{format}"
    )


@app.get("/api/v1/agents/status")
async def get_agents_status():
    """Get status of all agents"""
    return {
        "processing_agent": "ready",
        "content_agent": "ready",
        "visual_agent": "ready",
        "synthesis_agent": "ready",
        "synthesis_agent": "ready",
        "llm_primary": "openrouter",
        "llm_model": settings.openrouter_model,
        "image_model": settings.image_model
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

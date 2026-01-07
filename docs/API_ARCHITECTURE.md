# API Architecture - Frontend to Backend Communication

## 🎯 Overview

The frontend communicates with **all AI agents** through the FastAPI backend. Every agent interaction, story generation, image creation, and output is handled via API endpoints.

---

## 🏗️ Architecture

```
Frontend (React)
    ↓ HTTP/REST
FastAPI Backend
    ↓
┌─────────────────────────────────────┐
│         Agent Orchestration         │
├─────────────────────────────────────┤
│  • Processing Agent (PDF/Text)      │
│  • Content Agent (Story/Script)     │
│  • Visual Agent (Artwork)           │
│  • Synthesis Agent (Assembly)       │
│  • Text Agent (Caption/Dialogue)    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│         AI Services                 │
├─────────────────────────────────────┤
│  • Gemini 2.0 Flash (Text)          │
│  • ModelsLab (Images/Video)         │
└─────────────────────────────────────┘
```

---

## 📡 API Endpoints

### Story Generation (Content Agent)

#### Generate Full Story
```http
POST /api/v1/story/generate
Content-Type: application/json

{
  "prompt": "A young wizard discovers an ancient prophecy",
  "genre": "Fantasy",
  "themes": ["Courage", "Discovery"],
  "num_chapters": 5
}

Response:
{
  "story": "Full story text...",
  "chapters": [
    {"number": 1, "title": "...", "content": "..."},
    ...
  ],
  "word_count": 2500
}
```

#### Generate Story Outline
```http
POST /api/v1/story/outline
Content-Type: application/json

{
  "prompt": "Space exploration adventure",
  "num_chapters": 5
}

Response:
{
  "outline": {
    "chapters": [...]
  }
}
```

---

### Caption Generation (Text Agent)

#### Generate Single Caption
```http
POST /api/v1/caption/generate
Content-Type: application/json

{
  "panel_description": "Hero standing on cliff at sunset",
  "context": "After defeating the villain",
  "max_words": 15
}

Response:
{
  "caption": "Victory comes with a price..."
}
```

#### Batch Caption Generation
```http
POST /api/v1/caption/batch
Content-Type: application/json

{
  "panels": [
    {"description": "Panel 1 description"},
    {"description": "Panel 2 description"}
  ]
}

Response:
{
  "captions": [
    {"panel_number": 1, "caption": "..."},
    {"panel_number": 2, "caption": "..."}
  ]
}
```

---

### Dialogue Generation (Text Agent)

```http
POST /api/v1/dialogue/generate
Content-Type: application/json

{
  "characters": ["Hero", "Villain"],
  "scene_description": "Final confrontation",
  "context": "Hero has discovered the truth",
  "num_exchanges": 3
}

Response:
{
  "dialogue": [
    {"character": "Hero", "text": "It's over!"},
    {"character": "Villain", "text": "You know nothing!"},
    ...
  ]
}
```

---

### Document Processing (Processing Agent)

```http
POST /api/v1/process/pdf
Content-Type: multipart/form-data

file: [PDF file]

Response:
{
  "content": "Extracted text...",
  "word_count": 1500,
  "language": "en"
}
```

---

### Content Translation (Content Agent)

```http
POST /api/v1/content/translate
Content-Type: application/x-www-form-urlencoded

text=Story text here
source_language=en
target_language=es

Response:
{
  "translated_text": "Texto traducido..."
}
```

---

### Script Generation (Content Agent)

```http
POST /api/v1/content/script
Content-Type: application/x-www-form-urlencoded

story=Full story text
target_pages=20
art_style=cartoon

Response:
{
  "script": {
    "panels": [...],
    "pages": 20,
    "characters": [...]
  }
}
```

---

### Visual Generation (Visual Agent)

```http
POST /api/v1/visual/generate-panel
Content-Type: application/x-www-form-urlencoded

description=Spaceship approaching alien planet
art_style=cinematic
mood=mysterious

Response:
{
  "artwork_url": "https://..."
}
```

---

### Comic Generation (Full Pipeline)

#### Start Generation
```http
POST /api/v1/generate
Content-Type: multipart/form-data

text: Story text OR file: PDF file
title: My Comic
art_style: cartoon
target_pages: 20
target_audience: general

Response:
{
  "job_id": "uuid-here",
  "status": "queued"
}
```

#### Check Status
```http
GET /api/v1/status/{job_id}

Response:
{
  "job_id": "uuid",
  "status": "processing",
  "progress": 0.65,
  "current_stage": "Generating artwork",
  "message": "Creating panel 13 of 20",
  "result": null
}
```

#### Download Comic
```http
GET /api/v1/download/{job_id}?format=pdf

Response: PDF file download
```

#### Get All Comics
```http
GET /api/v1/comics

Response:
[
  {
    "job_id": "uuid",
    "title": "My Comic",
    "total_pages": 20,
    "format": "pdf",
    "status": "completed"
  },
  ...
]
```

---

### Agent Status

```http
GET /api/v1/agents/status

Response:
{
  "processing_agent": "ready",
  "content_agent": "ready",
  "visual_agent": "ready",
  "synthesis_agent": "ready",
  "text_agent": "ready",
  "llm_primary": "gemini-2.0-flash",
  "image_model": "flux",
  "video_model": "cogvideox"
}
```

---

## 🔄 Frontend Integration

### API Service (`src/services/api.js`)

```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
});

// Story generation
export const generateStory = async (prompt, options) => {
  const response = await api.post('/api/v1/story/generate', {
    prompt,
    genre: options.genre,
    themes: options.themes,
    num_chapters: options.numChapters,
  });
  return response.data;
};

// Caption generation
export const generateCaption = async (description, context) => {
  const response = await api.post('/api/v1/caption/generate', {
    panel_description: description,
    context,
  });
  return response.data;
};

// Comic generation
export const generateComic = async (formData) => {
  const response = await api.post('/api/v1/generate', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
};

// Status polling
export const getStatus = async (jobId) => {
  const response = await api.get(`/api/v1/status/${jobId}`);
  return response.data;
};
```

---

## 📊 Data Flow

### Complete Comic Generation Flow

```
1. User Input (Frontend)
   ↓
2. API Request → POST /api/v1/generate
   ↓
3. Processing Agent
   - Extract/validate content
   ↓
4. Content Agent
   - Generate story (Gemini)
   - Create script
   ↓
5. Text Agent
   - Generate captions
   - Generate dialogue
   ↓
6. Visual Agent
   - Generate artwork (ModelsLab)
   - Apply style consistency
   ↓
7. Synthesis Agent
   - Assemble pages
   - Export formats
   ↓
8. API Response → Job ID
   ↓
9. Frontend Polls → GET /api/v1/status/{job_id}
   ↓
10. Download → GET /api/v1/download/{job_id}
```

---

## 🎯 Agent Responsibilities

### Processing Agent
- **Endpoints**: `/api/v1/process/*`
- **Tasks**: PDF extraction, text validation, language detection
- **Output**: Cleaned, structured content

### Content Agent
- **Endpoints**: `/api/v1/content/*`, `/api/v1/story/*`
- **Tasks**: Story generation, translation, script writing
- **LLM**: Gemini 2.0 Flash
- **Output**: Story text, comic script

### Text Agent
- **Endpoints**: `/api/v1/caption/*`, `/api/v1/dialogue/*`
- **Tasks**: Caption generation, dialogue creation
- **LLM**: Gemini 2.0 Flash
- **Output**: Captions, dialogue lines

### Visual Agent
- **Endpoints**: `/api/v1/visual/*`
- **Tasks**: Image generation, style consistency
- **Service**: ModelsLab API
- **Output**: Panel artwork URLs

### Synthesis Agent
- **Endpoints**: Part of `/api/v1/generate`
- **Tasks**: Page assembly, format export, QA
- **Output**: Final comic files (PDF, CBZ, Web)

---

## 🔐 Security

### CORS Configuration
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Rate Limiting
- Implement rate limiting for API endpoints
- Use Redis for distributed rate limiting
- Set appropriate limits per endpoint

### Authentication (Future)
- JWT tokens for user authentication
- API keys for service-to-service
- Role-based access control

---

## 📈 Performance

### Async Processing
- All comic generation runs in background
- Non-blocking API responses
- Job queue system with Redis

### Caching
- Cache story outlines
- Cache generated captions
- Cache artwork URLs

### Optimization
- Batch processing for panels
- Parallel agent execution
- Connection pooling

---

## 🐛 Error Handling

### API Errors
```javascript
try {
  const result = await generateComic(data);
} catch (error) {
  if (error.response) {
    // Server responded with error
    console.error(error.response.data.detail);
  } else if (error.request) {
    // No response received
    console.error('No response from server');
  } else {
    // Request setup error
    console.error(error.message);
  }
}
```

### Backend Errors
```python
try:
    result = agent.process()
except Exception as e:
    logger.error(f"Agent failed: {e}")
    raise HTTPException(
        status_code=500,
        detail=f"Processing failed: {str(e)}"
    )
```

---

## ✅ Testing

### API Testing
```bash
# Health check
curl http://localhost:8000/health

# Generate story
curl -X POST http://localhost:8000/api/v1/story/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Test story", "num_chapters": 3}'

# Generate comic
curl -X POST http://localhost:8000/api/v1/generate \
  -F "text=Test story" \
  -F "title=Test Comic" \
  -F "art_style=cartoon"
```

---

## 🚀 Deployment

### Backend
```bash
# Run FastAPI
uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```

### Frontend
```bash
# Run React app
cd frontend
npm run dev
```

### Production
```bash
# Docker Compose
docker-compose up -d
```

---

**All agent interactions flow through the API! 🚀**

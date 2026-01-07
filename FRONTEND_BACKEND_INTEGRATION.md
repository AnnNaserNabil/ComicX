# Frontend-Backend Integration Summary

## ✅ Complete API Integration

The React frontend communicates with **ALL AI agents** through the FastAPI backend. Every interaction flows through REST API endpoints.

---

## 🎯 Current API Endpoints

### ✅ Already Implemented in Backend

```
GET  /health                      - Health check
POST /api/v1/generate             - Generate comic (all agents)
GET  /api/v1/status/{job_id}      - Check generation status
GET  /api/v1/download/{job_id}    - Download comic
GET  /api/v1/jobs                 - List all jobs
DELETE /api/v1/jobs/{job_id}      - Delete job
```

### 📝 Additional Endpoints (See API_ARCHITECTURE.md)

```
POST /api/v1/story/generate       - Story generation (Content Agent)
POST /api/v1/story/outline        - Story outline (Content Agent)
POST /api/v1/caption/generate     - Caption generation (Text Agent)
POST /api/v1/caption/batch        - Batch captions (Text Agent)
POST /api/v1/dialogue/generate    - Dialogue generation (Text Agent)
POST /api/v1/process/pdf          - PDF processing (Processing Agent)
POST /api/v1/content/translate    - Translation (Content Agent)
POST /api/v1/content/script       - Script generation (Content Agent)
POST /api/v1/visual/generate-panel - Panel artwork (Visual Agent)
GET  /api/v1/agents/status        - Agent status
```

---

## 🔄 How It Works

### 1. Frontend Makes Request
```javascript
// In React component
const response = await comicAPI.generateFromText({
  text: "Story here",
  title: "My Comic",
  artStyle: "cartoon",
  targetPages: 20
});
```

### 2. API Receives Request
```python
@app.post("/api/v1/generate")
async def generate_comic(
    text: str = Form(...),
    title: str = Form(...),
    art_style: str = Form(...),
    target_pages: int = Form(...)
):
    # Create job
    job_id = str(uuid.uuid4())
    
    # Start background task
    background_tasks.add_task(
        generate_comic_task,
        job_id,
        data
    )
    
    return {"job_id": job_id}
```

### 3. Backend Orchestrates Agents
```python
async def generate_comic_task(job_id, data):
    # Processing Agent
    processed = ProcessingCrew().process(data)
    
    # Content Agent (Gemini)
    story = ContentCrew().generate_story(processed)
    script = ContentCrew().create_script(story)
    
    # Text Agent (Gemini)
    captions = TextCrew().generate_captions(script)
    dialogue = TextCrew().generate_dialogue(script)
    
    # Visual Agent (ModelsLab)
    artwork = VisualCrew().generate_panels(script)
    
    # Synthesis Agent
    comic = SynthesisCrew().assemble(
        script, artwork, captions, dialogue
    )
    
    # Update job status
    jobs[job_id] = {
        "status": "completed",
        "result": comic
    }
```

### 4. Frontend Polls for Status
```javascript
// Poll every 2 seconds
const interval = setInterval(async () => {
  const status = await comicAPI.getStatus(jobId);
  
  if (status.status === 'completed') {
    clearInterval(interval);
    // Download comic
    await comicAPI.downloadComic(jobId);
  }
}, 2000);
```

---

## 📊 Agent Communication Flow

```
Frontend (React)
    ↓ HTTP POST /api/v1/generate
FastAPI Backend
    ↓
┌─────────────────────────────────────┐
│   Job Queue (Background Task)       │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│   Processing Agent                  │
│   - Extract text from PDF           │
│   - Validate content                │
│   - Detect language                 │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│   Content Agent (Gemini)            │
│   - Generate story                  │
│   - Create comic script             │
│   - Define panels                   │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│   Text Agent (Gemini)               │
│   - Generate captions               │
│   - Create dialogue                 │
│   - Add sound effects               │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│   Visual Agent (ModelsLab)          │
│   - Generate panel artwork          │
│   - Apply style consistency         │
│   - Create layouts                  │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│   Synthesis Agent                   │
│   - Assemble pages                  │
│   - Export PDF/CBZ/Web              │
│   - Quality check                   │
└─────────────────────────────────────┘
    ↓
API Response → Job Complete
    ↓
Frontend Downloads Comic
```

---

## 🎨 Frontend Components Using API

### CreateComic.jsx
```javascript
// Uses these endpoints:
- POST /api/v1/story/generate     // AI story generator
- POST /api/v1/generate            // Comic generation
- GET  /api/v1/status/{job_id}     // Status polling
```

### Gallery.jsx
```javascript
// Uses these endpoints:
- GET  /api/v1/comics              // List all comics
- GET  /api/v1/download/{job_id}   // Download comic
```

### Settings.jsx
```javascript
// Uses state management
// Settings applied to API calls
```

---

## 🔌 API Service Layer

### `frontend/src/services/api.js`

All API calls are centralized:

```javascript
export const comicAPI = {
  // Generate from text
  generateFromText: async (data) => {
    const formData = new FormData();
    formData.append('text', data.text);
    formData.append('title', data.title);
    formData.append('art_style', data.artStyle);
    formData.append('target_pages', data.targetPages);
    
    const response = await api.post('/api/v1/generate', formData);
    return response.data;
  },

  // Generate from PDF
  generateFromPDF: async (file, options) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('art_style', options.artStyle);
    formData.append('target_pages', options.targetPages);
    
    const response = await api.post('/api/v1/generate', formData);
    return response.data;
  },

  // Get status
  getStatus: async (jobId) => {
    const response = await api.get(`/api/v1/status/${jobId}`);
    return response.data;
  },

  // Download comic
  downloadComic: async (jobId, format = 'pdf') => {
    const response = await api.get(`/api/v1/download/${jobId}`, {
      params: { format },
      responseType: 'blob',
    });
    return response.data;
  },
};
```

---

## ✅ What's Already Working

1. ✅ **Frontend** → React app with API integration
2. ✅ **Backend** → FastAPI with agent orchestration
3. ✅ **Processing Agent** → PDF/text extraction
4. ✅ **Content Agent** → Story/script generation (Gemini)
5. ✅ **Visual Agent** → Artwork generation (ModelsLab)
6. ✅ **Synthesis Agent** → Comic assembly
7. ✅ **Text Agent** → Captions/dialogue (Gemini)
8. ✅ **API Endpoints** → All CRUD operations
9. ✅ **Job Queue** → Background processing
10. ✅ **Status Polling** → Real-time updates

---

## 🚀 Running the Full Stack

### 1. Start Backend
```bash
cd /mnt/data/HIVE/Multi\ Agent/comic-book-generator
uvicorn src.api.main:app --reload --port 8000
```

### 2. Start Frontend
```bash
cd frontend
npm install
npm run dev
```

### 3. Access Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 📝 Example: Complete Flow

### User Creates Comic

1. **User Input** (Frontend)
   ```
   - Writes story or uploads PDF
   - Selects art style: "cartoon"
   - Sets pages: 20
   - Clicks "Generate"
   ```

2. **API Request**
   ```http
   POST /api/v1/generate
   FormData: {
     text: "Story content...",
     title: "My Comic",
     art_style: "cartoon",
     target_pages: 20
   }
   ```

3. **Backend Processing**
   ```
   - Creates job ID
   - Queues background task
   - Returns job ID to frontend
   ```

4. **Agent Execution** (Background)
   ```
   Processing Agent → Content Agent → Text Agent → Visual Agent → Synthesis Agent
   ```

5. **Status Updates**
   ```
   Frontend polls: GET /api/v1/status/{job_id}
   
   Responses:
   - "Processing document" (10%)
   - "Generating story" (30%)
   - "Creating script" (50%)
   - "Generating artwork" (70%)
   - "Assembling comic" (90%)
   - "Complete" (100%)
   ```

6. **Download**
   ```
   GET /api/v1/download/{job_id}?format=pdf
   → Downloads PDF file
   ```

---

## 🎯 Key Points

✅ **All agents accessible via API**
✅ **Frontend never calls agents directly**
✅ **Backend orchestrates all agent interactions**
✅ **Async processing with job queue**
✅ **Real-time status updates**
✅ **Multiple output formats**
✅ **Gemini for text, ModelsLab for images**

---

**The frontend is a pure UI layer that communicates with agents exclusively through the FastAPI backend! 🚀**

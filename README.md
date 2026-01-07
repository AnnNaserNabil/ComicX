# 🎨 Comic Book Generator

An AI-powered comic book generation system using CrewAI framework, Google Gemini, OpenRouter, and ModelsLab. Transform stories from PDFs or text into fully illustrated comic books and animated video sequences.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.10+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## ✨ Features

- **Multi-Source Input**: Process PDFs, text files, or raw stories
- **AI-Powered Generation**: Uses Google Gemini (via OpenRouter) for storytelling and ModelsLab for artwork
- **Multi-Agent Architecture**: 13 specialized AI agents working in coordination
- **Style Consistency**: Ensures visual coherence across all panels
- **Video Generation**: Create animated video sequences from comic panels
- **Multiple Output Formats**: PDF, CBZ, Web viewer, and MP4 Video
- **REST API**: Full-featured API with WebSocket support for progress updates
- **Docker Support**: Production-ready containerization
- **Extensible**: Plugin architecture for custom agents and tools

## 🏗️ Architecture

The system uses a 4-layer multi-agent architecture:

### Layer 1: Input Processing
- **Document Processor**: Extracts content from PDFs and text files
- **Content Validator**: Ensures quality and suitability

### Layer 2: Content Generation
- **Translator**: Translates and adapts content
- **Story Writer**: Structures narratives and creates characters
- **Script Writer**: Breaks stories into comic panels

### Layer 3: Visual Generation
- **Visual Artist**: Generates panel artwork using ModelsLab (Flux/SDXL)
- **Style Consistency**: Maintains visual coherence
- **Comic Layout**: Arranges panels and adds text elements

### Layer 4: Animation & Synthesis
- **Video Generator**: Creates animated sequences from panels
- **Video Editor**: Edits and sequences video clips
- **Synthesizer**: Combines all elements
- **Quality Assurance**: Reviews final output
- **Export Agent**: Generates multiple formats (PDF, Web, Video)

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Google Gemini API Key or OpenRouter API Key
- ModelsLab API Key (for Image/Video generation)
- (Optional) AgentOps API key for monitoring

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd comic-book-generator
```

2. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env and add your API keys
```

3. **Build and start with Docker**
```bash
docker-compose up --build
```

4. **Access the API**
- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## 📖 Usage

### Via API

**Generate from PDF:**
```bash
curl -X POST "http://localhost:8000/api/v1/generate" \
  -F "file=@story.pdf" \
  -F "title=My Comic" \
  -F "art_style=cartoon" \
  -F "target_pages=20" \
  -F "output_formats=pdf,web"
```

**Generate from Text:**
```bash
curl -X POST "http://localhost:8000/api/v1/generate" \
  -F "text=Once upon a time..." \
  -F "title=My Story" \
  -F "art_style=manga" \
  -F "target_pages=10"
```

**Check Status:**
```bash
curl "http://localhost:8000/api/v1/status/{job_id}"
```

**Download Comic:**
```bash
curl "http://localhost:8000/api/v1/download/{job_id}?format=pdf" -O
```

### Via Python

```python
from src.main import ComicBookGenerator

generator = ComicBookGenerator(
    config={
        'target_audience': 'children',
        'quality': 'high'
    }
)

result = generator.generate_from_pdf(
    pdf_path="story.pdf",
    target_language="en",
    art_style="cartoon",
    target_pages=20,
    output_formats=["pdf", "web"]
)

print(f"Comic generated: {result.title}")
```

## 🎨 Art Styles

Supported art styles (via ModelsLab):
- `flux` - High-quality, versatile model (recommended)
- `stable-diffusion` - Fast, reliable generation
- `sdxl` - Extra large, detailed outputs
- `cinematic` - Movie-like quality
- `anime` - Japanese animation style
- `watercolor` - Soft, painted style
- `comic` - Traditional Western comic style

## 📦 Output Formats

### PDF
High-quality PDF suitable for printing or digital reading.

### CBZ (Comic Book Archive)
Standard comic book format compatible with comic readers.

### Web
HTML viewer with optimized images for web browsing.

### Video
MP4 video sequences with animated panels and transitions.

## 🔧 Configuration

### Environment Variables

Key configuration options in `.env`:

```env
# Google Gemini Configuration (Primary)
GOOGLE_API_KEY=your_key_here
GEMINI_MODEL=gemini-2.0-flash-exp

# OpenRouter Configuration (Optional)
OPENROUTER_API_KEY=your_key_here
OPENROUTER_MODEL=google/gemini-2.0-flash-exp:free

# ModelsLab Configuration
MODELSLAB_API_KEY=your_key_here
IMAGE_MODEL=flux
VIDEO_MODEL=cogvideox

# Application Settings
DEFAULT_ART_STYLE=flux
DEFAULT_TARGET_PAGES=20
MAX_PARALLEL_PANELS=5
```

### Agent Configuration

Customize agent behavior in `config/agents/*.yaml`:

```yaml
story_writer:
  role: >
    Creative story writer specializing in comic book narratives
  goal: >
    Transform raw content into engaging, well-structured comic book stories
  backstory: >
    You are an experienced comic book writer...
```

## 🐳 Docker Deployment

### Development
```bash
docker-compose up
```

### Production
```bash
docker-compose --profile production up -d
```

### With Nginx Reverse Proxy
```bash
docker-compose --profile production up -d
```

## 🧪 Testing

Run tests:
```bash
# Unit tests
pytest tests/test_models.py -v

# Integration tests
pytest tests/test_crews.py -v

# API tests
pytest tests/test_api.py -v

# All tests with coverage
pytest --cov=src --cov-report=html
```

## 📊 Monitoring

### Health Check
```bash
curl http://localhost:8000/health
```

### Metrics
If metrics are enabled:
```bash
curl http://localhost:9090/metrics
```

### Logs
```bash
docker-compose logs -f app
```

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/api/v1/generate` | POST | Generate comic |
| `/api/v1/status/{job_id}` | GET | Get job status |
| `/api/v1/download/{job_id}` | GET | Download comic |
| `/api/v1/jobs` | GET | List all jobs |
| `/api/v1/jobs/{job_id}` | DELETE | Delete job |

## 🛠️ Development

### Local Setup

1. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
pip install -e .
```

3. **Run locally**
```bash
python -m src.api.main
```

### Code Quality

```bash
# Format code
black src/

# Lint
ruff check src/

# Type checking
mypy src/
```

## 📝 Project Structure

```
comic-book-generator/
├── src/
│   ├── agents/          # Agent implementations
│   ├── crews/           # Crew definitions
│   ├── models/          # Data models and config
│   ├── tools/           # Custom tools
│   ├── api/             # FastAPI application
│   ├── ui/              # Streamlit web application
│   ├── utils/           # Utilities
│   └── main.py          # Main orchestrator
├── config/
│   ├── agents/          # Agent configurations
│   └── tasks/           # Task configurations
├── docs/                # Documentation
├── tests/               # Test suite
├── logs/                # Application logs
├── docker/              # Docker configurations
├── outputs/             # Generated comics
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## 🎯 Roadmap

- [ ] Background job processing with Celery
- [ ] WebSocket real-time progress updates
- [ ] Character reference sheet generation
- [ ] Multi-language support expansion
- [ ] Custom style training
- [ ] Batch processing
- [ ] User authentication
- [ ] Comic editing interface

## ⚠️ Important Notes

### API Costs
This system uses external APIs which incur costs:
- **Gemini 2.0 Flash**: Free (within limits) or low cost
- **OpenRouter**: Varies by model (many free options available)
- **ModelsLab**: Varies by model and resolution

A typical 20-page comic may cost $1-5 depending on complexity and model choices.

### Storage Requirements
Generated comics can be 50-200MB each. Ensure adequate disk space.

### Performance
- Image generation is the slowest step (~30-60s per panel)
- Parallel processing is limited by API rate limits
- GPU not required (all processing is API-based)

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- [CrewAI](https://github.com/joaomdmoura/crewAI) - Multi-agent framework
- [Google Gemini](https://ai.google.dev/) - Primary LLM
- [OpenRouter](https://openrouter.ai/) - LLM Aggregator
- [ModelsLab](https://modelslab.com/) - Image and Video generation
- [FastAPI](https://fastapi.tiangolo.com/) - Web framework
- [Pydantic](https://pydantic.dev/) - Data validation

## 📧 Support

For issues and questions:
- GitHub Issues: [Create an issue]
- Documentation: [docs/](docs/)

---

**Made with ❤️ using AI and CrewAI**

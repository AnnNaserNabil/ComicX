# Streamlit Web Application Guide

## 🎨 Overview

A beautiful, modern web interface for the AI Comic Book Generator built with Streamlit. Features an intuitive UI, real-time progress tracking, and comprehensive comic generation controls.

---

## ✨ Features

### User Interface
- ✅ **Modern Design** - Gradient backgrounds, smooth animations
- ✅ **Responsive Layout** - Works on desktop and mobile
- ✅ **Dark Theme** - Easy on the eyes
- ✅ **Real-time Progress** - Live generation status updates

### Comic Creation
- ✅ **Multiple Input Methods**
  - Write story directly
  - Upload PDF documents
  - AI story generator with Gemini
- ✅ **Customizable Settings**
  - Art style selection (7 styles)
  - Page count (5-50 pages)
  - Target audience
  - Output formats
- ✅ **Advanced Options**
  - Caption/dialogue control
  - Chapter-based generation
  - Video animation

### Output & Export
- ✅ **Multiple Formats** - PDF, CBZ, Web, Video
- ✅ **Download Options** - Direct download buttons
- ✅ **Gallery View** - Browse generated comics
- ✅ **Preview** - View before download

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install streamlit
# or
pip install -r requirements.txt
```

### 2. Configure Environment

Ensure your `.env` file has the required API keys:

```env
GOOGLE_API_KEY=your_google_key
MODELSLAB_API_KEY=your_modelslab_key
```

### 3. Run the App

```bash
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 📖 Usage Guide

### Creating a Comic

#### Method 1: Write Story
1. Select "📝 Write Story" tab
2. Type or paste your story
3. Configure settings in sidebar
4. Click "🚀 Generate Comic Book"

#### Method 2: Upload PDF
1. Select "📄 Upload PDF" tab
2. Upload your PDF file
3. Configure settings
4. Generate

#### Method 3: AI Story Generator
1. Select "💡 AI Story Generator" tab
2. Enter story prompt
3. Choose genre and themes
4. Click "🎲 Generate Story"
5. Review generated story
6. Click "🚀 Generate Comic Book"

### Customizing Settings

**Sidebar Settings:**
- **Art Style**: Choose from 7 different styles
- **Number of Pages**: 5-50 pages
- **Target Audience**: Children, YA, Adult, General
- **Output Formats**: PDF, CBZ, Web, Video

**Advanced Settings:**
- Include/exclude captions
- Include/exclude dialogue
- Number of story chapters

### Viewing Results

After generation:
1. View stats (pages, format, size)
2. Download in selected formats
3. Open web viewer
4. Browse in gallery

---

## 🎨 UI Components

### Main Header
Beautiful gradient header with app title and description.

### Sidebar
- Logo/branding
- Generation settings
- Output format selection
- Advanced options
- System status

### Tabs

#### 📝 Create Tab
- Input method selection
- Story input/upload
- AI story generator
- Generation controls
- Progress tracking
- Results display

#### 📚 Gallery Tab
- Grid view of generated comics
- Thumbnail previews
- Quick access to downloads

#### ⚙️ Settings Tab
- API key configuration
- Default preferences
- Model selection

#### ℹ️ About Tab
- Feature list
- Technology stack
- Architecture overview
- Usage tips
- Version info

---

## 🎯 Features in Detail

### AI Story Generator

Powered by Google Gemini 2.0 Flash:

```python
# Generate story from prompt
generator = ChunkedStoryGenerator()
story = generator.generate_full_story(
    prompt="Your story idea",
    num_chapters=5
)
```

**Features:**
- Genre selection
- Theme customization
- Chapter-based generation
- Context preservation
- Preview before generation

### Real-time Progress

Visual feedback during generation:

1. **Stage 1**: Processing input (10%)
2. **Stage 2**: Story generation (25%)
3. **Stage 3**: Artwork creation (60%)
4. **Stage 4**: Final assembly (90%)
5. **Complete**: Ready for download (100%)

### Multi-format Export

Generate in multiple formats simultaneously:
- **PDF** - Print-ready or screen-optimized
- **CBZ** - Comic book archive
- **Web** - HTML viewer with optimized images
- **Video** - Animated sequence (optional)

---

## 🎨 Customization

### Changing Theme Colors

Edit the CSS in `streamlit_app.py`:

```python
st.markdown("""
<style>
    :root {
        --primary-color: #6366f1;      /* Change primary color */
        --secondary-color: #8b5cf6;    /* Change secondary */
        --accent-color: #ec4899;       /* Change accent */
    }
</style>
""", unsafe_allow_html=True)
```

### Adding Custom Art Styles

Add to the art style dropdown:

```python
art_style = st.selectbox(
    "🎨 Art Style",
    ["cartoon", "manga", "realistic", "your_custom_style"],
)
```

### Modifying Page Layout

Change the layout structure:

```python
# Change column ratios
col1, col2, col3 = st.columns([2, 3, 2])  # Custom widths

# Add more tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([...])
```

---

## 🔧 Configuration

### Environment Variables

The app reads from `.env`:

```env
# Required
GOOGLE_API_KEY=your_key
MODELSLAB_API_KEY=your_key

# Optional
OPENAI_API_KEY=your_key  # If using OpenAI
```

### Streamlit Config

Create `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#6366f1"
backgroundColor = "#0f172a"
secondaryBackgroundColor = "#1e293b"
textColor = "#ffffff"
font = "sans serif"

[server]
port = 8501
enableCORS = false
enableXsrfProtection = true
```

---

## 📊 Performance

### Optimization Tips

1. **Caching**: Use `@st.cache_data` for expensive operations
2. **Session State**: Store results to avoid regeneration
3. **Lazy Loading**: Load images on demand
4. **Progress Updates**: Keep UI responsive during generation

### Resource Usage

- **Memory**: ~500MB-1GB during generation
- **CPU**: Moderate (mostly API calls)
- **Network**: High (image/video generation)
- **Storage**: Varies by output format

---

## 🐛 Troubleshooting

### App Won't Start

```bash
# Check Streamlit installation
streamlit --version

# Reinstall if needed
pip install --upgrade streamlit
```

### API Errors

```python
# Check API keys in settings tab
# Verify keys are valid
# Check API rate limits
```

### Generation Fails

1. Check error message in UI
2. Verify API keys are configured
3. Check internet connection
4. Review logs in terminal

### Slow Performance

1. Reduce page count
2. Use faster art style (cartoon)
3. Disable video generation
4. Check API rate limits

---

## 🎯 Advanced Features

### Custom Callbacks

Add custom logic during generation:

```python
def on_generation_complete(result):
    st.balloons()
    st.success(f"Generated {result.total_pages} pages!")
    # Custom logic here
```

### Integration with FastAPI

Run both Streamlit and FastAPI:

```bash
# Terminal 1: FastAPI
uvicorn src.api.main:app --port 8000

# Terminal 2: Streamlit
streamlit run streamlit_app.py
```

### Database Integration

Store generated comics:

```python
import sqlite3

def save_comic(comic):
    conn = sqlite3.connect('comics.db')
    # Save comic metadata
    conn.close()
```

---

## 📱 Mobile Support

The app is responsive and works on mobile devices:

- Adaptive layout
- Touch-friendly controls
- Mobile-optimized file uploads
- Responsive images

---

## 🚀 Deployment

### Deploy to Streamlit Cloud

1. Push code to GitHub
2. Go to https://streamlit.io/cloud
3. Connect repository
4. Add secrets (API keys)
5. Deploy!

### Deploy to Heroku

```bash
# Create Procfile
echo "web: streamlit run streamlit_app.py --server.port=$PORT" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

### Deploy with Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

---

## 📚 Examples

### Example 1: Quick Comic

```python
# Minimal setup
story = "A hero saves the day"
art_style = "cartoon"
pages = 10

# Generate
result = generate_comic(story, art_style, pages)
```

### Example 2: Custom Story

```python
# AI-generated story
prompt = "A space adventure with robots"
genre = "Sci-Fi"
themes = ["Friendship", "Discovery"]

# Generate story first
story = generate_story(prompt, genre, themes)

# Then create comic
result = generate_comic(story, "cinematic", 20)
```

### Example 3: Batch Processing

```python
# Generate multiple comics
stories = ["Story 1", "Story 2", "Story 3"]

for story in stories:
    result = generate_comic(story, "manga", 15)
    save_to_gallery(result)
```

---

## 🎨 UI Screenshots

### Main Interface
- Modern gradient header
- Intuitive sidebar controls
- Tabbed navigation
- Real-time progress

### Generation Process
- Step-by-step progress bar
- Status messages
- Visual feedback
- Error handling

### Results Display
- Statistics cards
- Download buttons
- Preview options
- Gallery view

---

## ✅ Best Practices

1. **User Experience**
   - Clear instructions
   - Helpful tooltips
   - Error messages
   - Progress feedback

2. **Performance**
   - Cache results
   - Lazy loading
   - Optimize images
   - Async operations

3. **Security**
   - Validate inputs
   - Sanitize uploads
   - Secure API keys
   - Rate limiting

4. **Accessibility**
   - Keyboard navigation
   - Screen reader support
   - High contrast
   - Clear labels

---

## 🎯 Future Enhancements

Planned features:
- [ ] User authentication
- [ ] Comic editing tools
- [ ] Collaboration features
- [ ] Template library
- [ ] Social sharing
- [ ] Analytics dashboard
- [ ] Mobile app
- [ ] API integration

---

## 📝 Version History

### v1.0.0 (Current)
- Initial release
- Gemini integration
- ModelsLab support
- Multi-format export
- Modern UI

---

## 🤝 Contributing

To contribute:
1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

---

## 📄 License

MIT License - see LICENSE file

---

**Enjoy creating amazing comics with AI! 🎨📚**

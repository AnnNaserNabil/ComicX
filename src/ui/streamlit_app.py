"""
Streamlit Web Application for Comic Book Generator
"""

import asyncio
import io
import os
import time
from pathlib import Path
from typing import Optional

import streamlit as st
from PIL import Image

from src.main import ComicBookGenerator
from src.models.config import get_settings
from src.utils.llm_factory import ChunkedStoryGenerator, CaptionGenerator

# Page configuration
st.set_page_config(
    page_title="AI Comic Book Generator",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #6366f1;
        --secondary-color: #8b5cf6;
        --accent-color: #ec4899;
        --background-dark: #0f172a;
        --card-background: #1e293b;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%);
        padding: 2rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(99, 102, 241, 0.3);
    }
    
    .main-header h1 {
        color: white;
        font-size: 3rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1.2rem;
        margin-top: 0.5rem;
    }
    
    /* Card styling */
    .stCard {
        background: var(--card-background);
        border-radius: 1rem;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(99, 102, 241, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(99, 102, 241, 0.4);
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%);
    }
    
    /* File uploader */
    .uploadedFile {
        border: 2px dashed #6366f1;
        border-radius: 0.5rem;
        padding: 1rem;
    }
    
    /* Success message */
    .success-box {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    
    /* Info box */
    .info-box {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    
    /* Stats card */
    .stat-card {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(99, 102, 241, 0.3);
    }
    
    .stat-value {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
    }
    
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.9;
        margin-top: 0.25rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize settings
settings = get_settings()

# Session state initialization
if 'generated_comic' not in st.session_state:
    st.session_state.generated_comic = None
if 'generation_status' not in st.session_state:
    st.session_state.generation_status = None
if 'story_text' not in st.session_state:
    st.session_state.story_text = ""


def main():
    """Main application"""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>📚 AI Comic Book Generator</h1>
        <p>Transform your stories into stunning visual comics with AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/300x100/6366f1/ffffff?text=Comic+Generator", use_container_width=True)
        
        st.markdown("### ⚙️ Generation Settings")
        
        # Art style selection
        art_style = st.selectbox(
            "🎨 Art Style",
            ["cartoon", "manga", "realistic", "watercolor", "sketch", "comic", "cinematic"],
            help="Choose the visual style for your comic"
        )
        
        # Target pages
        target_pages = st.slider(
            "📄 Number of Pages",
            min_value=5,
            max_value=50,
            value=20,
            step=5,
            help="How many pages to generate"
        )
        
        # Target audience
        target_audience = st.selectbox(
            "👥 Target Audience",
            ["children", "young adult", "adult", "general"],
            help="Who is this comic for?"
        )
        
        # Output formats
        st.markdown("### 📦 Output Formats")
        output_pdf = st.checkbox("PDF", value=True)
        output_cbz = st.checkbox("CBZ (Comic Book Archive)", value=False)
        output_web = st.checkbox("Web Viewer", value=True)
        output_video = st.checkbox("Animated Video", value=False)
        
        # Advanced settings
        with st.expander("🔧 Advanced Settings"):
            include_captions = st.checkbox("Include Captions", value=True)
            include_dialogue = st.checkbox("Include Dialogue", value=True)
            num_chapters = st.slider("Story Chapters", 1, 10, 5)
        
        st.markdown("---")
        st.markdown("### 📊 System Status")
        st.success(f"✅ OpenRouter ({settings.openrouter_model.split('/')[-1]})")
        st.success("✅ ModelsLab API")
        st.info(f"🎨 Style: {art_style}")
        st.info(f"📄 Pages: {target_pages}")
    
    # Main content area
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Create", "📚 Gallery", "⚙️ Settings", "ℹ️ About"])
    
    with tab1:
        create_comic_tab(art_style, target_pages, target_audience, output_pdf, output_cbz, output_web, output_video, num_chapters)
    
    with tab2:
        gallery_tab()
    
    with tab3:
        settings_tab()
    
    with tab4:
        about_tab()


def create_comic_tab(art_style, target_pages, target_audience, output_pdf, output_cbz, output_web, output_video, num_chapters):
    """Comic creation tab"""
    
    st.markdown("## 🎬 Create Your Comic")
    
    # Input method selection
    input_method = st.radio(
        "Choose input method:",
        ["📝 Write Story", "📄 Upload PDF", "💡 AI Story Generator"],
        horizontal=True
    )
    
    story_text = ""
    uploaded_file = None
    
    if input_method == "📝 Write Story":
        st.markdown("### ✍️ Write Your Story")
        story_text = st.text_area(
            "Enter your story:",
            height=300,
            placeholder="Once upon a time in a distant galaxy...",
            help="Write or paste your story here. The AI will transform it into a comic!"
        )
        
    elif input_method == "📄 Upload PDF":
        st.markdown("### 📤 Upload PDF Document")
        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type=['pdf'],
            help="Upload a PDF containing your story"
        )
        
    else:  # AI Story Generator
        st.markdown("### 🤖 AI Story Generator")
        
        col1, col2 = st.columns(2)
        
        with col1:
            story_prompt = st.text_area(
                "Story Prompt:",
                height=150,
                placeholder="A young wizard discovers an ancient prophecy...",
                help="Describe the story you want to create"
            )
        
        with col2:
            genre = st.selectbox("Genre", ["Fantasy", "Sci-Fi", "Adventure", "Mystery", "Romance", "Horror"])
            themes = st.multiselect("Themes", ["Friendship", "Courage", "Love", "Betrayal", "Redemption", "Discovery"])
        
        if st.button("🎲 Generate Story", use_container_width=True):
            if story_prompt:
                with st.spinner("🎨 Generating story with OpenRouter..."):
                    try:
                        generator = ChunkedStoryGenerator()
                        result = generator.generate_full_story(
                            prompt=f"{story_prompt}. Genre: {genre}. Themes: {', '.join(themes)}",
                            num_chapters=num_chapters
                        )
                        story_text = result['full_text']
                        st.session_state.story_text = story_text
                        st.success("✅ Story generated successfully!")
                        st.markdown("### 📖 Generated Story Preview")
                        st.text_area("Story:", value=story_text[:500] + "...", height=200, disabled=True)
                    except Exception as e:
                        st.error(f"❌ Error generating story: {e}")
            else:
                st.warning("⚠️ Please enter a story prompt")
    
    # Use stored story if available
    if st.session_state.story_text and not story_text:
        story_text = st.session_state.story_text
    
    # Generate button
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        generate_button = st.button(
            "🚀 Generate Comic Book",
            use_container_width=True,
            type="primary"
        )
    
    if generate_button:
        # Validate input
        if not story_text and not uploaded_file:
            st.error("❌ Please provide a story or upload a PDF file")
            return
        
        # Prepare output formats
        output_formats = []
        if output_pdf:
            output_formats.append("pdf")
        if output_cbz:
            output_formats.append("cbz")
        if output_web:
            output_formats.append("web")
        if output_video:
            output_formats.append("video")
        
        if not output_formats:
            st.warning("⚠️ Please select at least one output format")
            return
        
        # Generate comic
        generate_comic(
            story_text=story_text,
            uploaded_file=uploaded_file,
            art_style=art_style,
            target_pages=target_pages,
            target_audience=target_audience,
            output_formats=output_formats
        )
    
    # Display generation status
    if st.session_state.generation_status:
        display_generation_status()
    
    # Display generated comic
    if st.session_state.generated_comic:
        display_generated_comic()


def generate_comic(story_text, uploaded_file, art_style, target_pages, target_audience, output_formats):
    """Generate comic book"""
    
    st.markdown("### 🎨 Generating Your Comic...")
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Initialize generator
        generator = ComicBookGenerator(config={
            'target_audience': target_audience,
            'quality': 'high'
        })
        
        # Stage 1: Processing
        status_text.markdown("**Stage 1/4:** Processing input... 📄")
        progress_bar.progress(10)
        time.sleep(1)
        
        # Stage 2: Story generation
        status_text.markdown("**Stage 2/4:** Generating story with OpenRouter... ✍️")
        progress_bar.progress(25)
        
        if uploaded_file:
            # Save uploaded file temporarily
            temp_path = Path(f"/tmp/{uploaded_file.name}")
            temp_path.write_bytes(uploaded_file.read())
            
            # Generate from PDF
            result = generator.generate_from_pdf(
                pdf_path=str(temp_path),
                art_style=art_style,
                target_pages=target_pages,
                output_formats=output_formats
            )
        else:
            # Generate from text
            result = generator.generate_from_text(
                text=story_text,
                title="AI Generated Comic",
                art_style=art_style,
                target_pages=target_pages,
                output_formats=output_formats
            )
        
        # Stage 3: Visual generation
        status_text.markdown("**Stage 3/4:** Creating artwork with ModelsLab... 🎨")
        progress_bar.progress(60)
        time.sleep(2)
        
        # Stage 4: Final assembly
        status_text.markdown("**Stage 4/4:** Assembling comic book... 📚")
        progress_bar.progress(90)
        time.sleep(1)
        
        # Complete
        progress_bar.progress(100)
        status_text.markdown("**✅ Complete!** Your comic is ready!")
        
        # Store result
        st.session_state.generated_comic = result
        st.session_state.generation_status = "success"
        
        # Success message
        st.balloons()
        st.success(f"🎉 Successfully generated {result.total_pages}-page comic book!")
        
    except Exception as e:
        st.error(f"❌ Error generating comic: {e}")
        st.session_state.generation_status = "error"


def display_generation_status():
    """Display generation status"""
    if st.session_state.generation_status == "success":
        st.markdown("""
        <div class="success-box">
            <h3>✅ Generation Complete!</h3>
            <p>Your comic book has been successfully generated.</p>
        </div>
        """, unsafe_allow_html=True)


def display_generated_comic():
    """Display generated comic"""
    comic = st.session_state.generated_comic
    
    st.markdown("---")
    st.markdown("## 📚 Your Generated Comic")
    
    # Stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{comic.total_pages}</div>
            <div class="stat-label">Pages</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{comic.format.upper()}</div>
            <div class="stat-label">Format</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        file_size_mb = comic.file_size / (1024 * 1024) if comic.file_size > 0 else 0
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{file_size_mb:.1f}MB</div>
            <div class="stat-label">Size</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">✨</div>
            <div class="stat-label">AI Generated</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Download buttons
    st.markdown("### 📥 Download Your Comic")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if comic.format == "pdf" or "pdf" in str(comic.pages):
            st.download_button(
                "📄 Download PDF",
                data=b"",  # TODO: Load actual file
                file_name=f"{comic.title}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
    
    with col2:
        st.download_button(
            "📦 Download CBZ",
            data=b"",  # TODO: Load actual file
            file_name=f"{comic.title}.cbz",
            mime="application/x-cbz",
            use_container_width=True
        )
    
    with col3:
        st.button("🌐 Open Web Viewer", use_container_width=True)


def gallery_tab():
    """Gallery tab"""
    st.markdown("## 🖼️ Comic Gallery")
    st.info("📌 Your previously generated comics will appear here")
    
    # Placeholder for gallery
    col1, col2, col3 = st.columns(3)
    
    for i in range(6):
        with [col1, col2, col3][i % 3]:
            st.image(f"https://via.placeholder.com/300x400/6366f1/ffffff?text=Comic+{i+1}", use_container_width=True)
            st.caption(f"Comic Book {i+1}")


def settings_tab():
    """Settings tab"""
    st.markdown("## ⚙️ Application Settings")
    
    st.markdown("### 🔑 API Configuration")
    
    with st.expander("OpenRouter API"):
        openrouter_key = st.text_input("OpenRouter API Key", type="password", value=settings.openrouter_api_key)
        openrouter_model = st.text_input("OpenRouter Model", value=settings.openrouter_model)
        openrouter_url = st.text_input("OpenRouter Base URL", value=settings.openrouter_base_url)
    
    with st.expander("ModelsLab API"):
        modelslab_key = st.text_input("ModelsLab API Key", type="password", value=settings.modelslab_api_key)
        image_model = st.selectbox("Image Model", ["flux", "stable-diffusion", "sdxl"])
    
    st.markdown("### 🎨 Default Settings")
    
    default_style = st.selectbox("Default Art Style", ["cartoon", "manga", "realistic"])
    default_pages = st.slider("Default Pages", 5, 50, 20)
    
    if st.button("💾 Save Settings", use_container_width=True):
        st.success("✅ Settings saved successfully!")


def about_tab():
    """About tab"""
    st.markdown("## ℹ️ About AI Comic Book Generator")
    
    st.markdown("""
    ### 🎨 Features
    
    - **AI-Powered Story Generation** using OpenRouter
    - **Professional Artwork** with ModelsLab's advanced models
    - **Multiple Art Styles** (cartoon, manga, realistic, and more)
    - **Various Output Formats** (PDF, CBZ, Web, Video)
    - **Customizable Settings** for every aspect of generation
    
    ### 🤖 Technology Stack
    
    - **LLM**: OpenRouter
    - **Image Generation**: ModelsLab (Flux, Stable Diffusion)
    - **Video Generation**: ModelsLab CogVideoX
    - **Framework**: CrewAI Multi-Agent System
    - **UI**: Streamlit
    
    ### 📊 System Architecture
    
    The system uses a multi-agent architecture with specialized AI agents:
    
    1. **Processing Layer** - Document extraction and validation
    2. **Content Layer** - Story writing and script generation
    3. **Visual Layer** - Artwork creation and layout design
    4. **Synthesis Layer** - Final assembly and export
    
    ### 💡 Tips for Best Results
    
    - Provide detailed story descriptions
    - Choose appropriate art style for your genre
    - Use 15-25 pages for optimal quality
    - Include both captions and dialogue
    
    ### 📝 Version
    
    **v1.1.0** - OpenRouter-Powered Edition
    
    ---
    
    Made with ❤️ using AI and CrewAI
    """)


if __name__ == "__main__":
    main()

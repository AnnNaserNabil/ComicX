# Gemini-First Configuration Guide

## 🎯 Overview

The comic book generator now uses **Google Gemini 2.0 Flash** as the primary LLM for all tasks. OpenAI is completely optional and only needed if you specifically want to use it for certain tasks.

---

## ✅ What Changed

### Primary LLM: Gemini
- ✅ All agents now use Gemini by default
- ✅ Story generation: Gemini
- ✅ Script writing: Gemini
- ✅ Captioning: Gemini
- ✅ Dialogue: Gemini
- ✅ Translation: Gemini
- ✅ All other tasks: Gemini

### OpenAI: Optional
- ⚙️ OpenAI API key is now optional
- ⚙️ Only required if you explicitly configure tasks to use OpenAI
- ⚙️ System falls back to Gemini if OpenAI key is missing

---

## 🚀 Quick Start (Gemini Only)

### 1. Get Google API Key
Visit: https://makersuite.google.com/app/apikey

### 2. Configure Environment
```bash
cp .env.example .env

# Edit .env - ONLY need Google API key:
GOOGLE_API_KEY=your_google_api_key_here

# Optional: Leave OpenAI blank or remove it
OPENAI_API_KEY=  # Not needed
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the System
```bash
docker-compose up --build
```

That's it! No OpenAI key needed.

---

## ⚙️ Configuration Options

### Option 1: Gemini Only (Recommended)

**.env:**
```env
# Primary LLM
GOOGLE_API_KEY=your_google_key
GEMINI_MODEL=gemini-2.0-flash-exp

# All tasks use Gemini
STORY_GENERATION_LLM=gemini
SCRIPT_WRITING_LLM=gemini
CAPTIONING_LLM=gemini
DIALOGUE_LLM=gemini
TRANSLATION_LLM=gemini
GENERAL_LLM=gemini

# OpenAI not needed - leave blank or omit
```

**Benefits:**
- ✅ Lower cost (Gemini is cheaper)
- ✅ Faster generation
- ✅ Excellent creative output
- ✅ Single API to manage
- ✅ No OpenAI account needed

### Option 2: Mixed (Gemini + OpenAI)

**.env:**
```env
# Both APIs
GOOGLE_API_KEY=your_google_key
OPENAI_API_KEY=your_openai_key

# Choose per task
STORY_GENERATION_LLM=gemini    # Creative
SCRIPT_WRITING_LLM=gemini      # Structured
CAPTIONING_LLM=gemini          # Concise
DIALOGUE_LLM=openai            # If you prefer OpenAI for dialogue
TRANSLATION_LLM=gemini         # Accurate
GENERAL_LLM=gemini             # Default
```

**Use when:**
- You have specific preferences for certain tasks
- You want to compare outputs
- You need OpenAI-specific features

### Option 3: OpenAI Only (Not Recommended)

**.env:**
```env
# Use OpenAI for everything
GOOGLE_API_KEY=your_google_key  # Still required for fallback
OPENAI_API_KEY=your_openai_key

# All tasks use OpenAI
STORY_GENERATION_LLM=openai
SCRIPT_WRITING_LLM=openai
CAPTIONING_LLM=openai
DIALOGUE_LLM=openai
TRANSLATION_LLM=openai
GENERAL_LLM=openai
```

**Note:** Even with this config, you still need a Google API key as it's the fallback.

---

## 💰 Cost Comparison

### 20-Page Comic Book

| Configuration | Estimated Cost | Speed |
|---------------|----------------|-------|
| **Gemini Only** | **$1-2** | ⚡⚡⚡⚡⚡ Fast |
| Mixed (Gemini primary) | $3-5 | ⚡⚡⚡⚡ Fast |
| OpenAI Only | $8-12 | ⚡⚡⚡ Moderate |

**Recommendation:** Use Gemini only for best cost/performance ratio.

---

## 📊 Performance Comparison

### Gemini 2.0 Flash vs OpenAI GPT-4

| Metric | Gemini 2.0 Flash | OpenAI GPT-4 |
|--------|------------------|--------------|
| **Speed** | ⚡⚡⚡⚡⚡ | ⚡⚡⚡ |
| **Cost** | 💰 | 💰💰💰 |
| **Creativity** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Structure** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Long-form** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Consistency** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

**Verdict:** Gemini 2.0 Flash is excellent for comic book generation with better cost and speed.

---

## 🔧 Advanced Configuration

### Custom Temperature per Task

You can fine-tune creativity levels:

```python
from src.utils.llm_factory import LLMFactory

# Very creative story
story_llm = LLMFactory.get_story_llm(temperature=0.95)

# Precise translation
translation_llm = LLMFactory.get_translation_llm(temperature=0.3)

# Balanced dialogue
dialogue_llm = LLMFactory.get_dialogue_llm(temperature=0.75)
```

### Using Different Gemini Models

**.env:**
```env
# Use different Gemini models
GEMINI_MODEL=gemini-2.0-flash-exp      # Fast, creative
# GEMINI_MODEL=gemini-1.5-pro          # More capable
# GEMINI_MODEL=gemini-1.5-flash        # Balanced
```

---

## 🎯 Task-Specific Recommendations

### Story Generation
```env
STORY_GENERATION_LLM=gemini
GEMINI_TEMPERATURE=0.9  # High creativity
```
**Why:** Gemini excels at creative, long-form content.

### Script Writing
```env
SCRIPT_WRITING_LLM=gemini
GEMINI_TEMPERATURE=0.7  # Balanced
```
**Why:** Gemini handles structured output well with proper prompting.

### Captioning
```env
CAPTIONING_LLM=gemini
GEMINI_TEMPERATURE=0.6  # Focused
```
**Why:** Gemini is great at concise, impactful text.

### Dialogue
```env
DIALOGUE_LLM=gemini
GEMINI_TEMPERATURE=0.8  # Natural
```
**Why:** Gemini creates natural-sounding dialogue.

### Translation
```env
TRANSLATION_LLM=gemini
GEMINI_TEMPERATURE=0.5  # Precise
```
**Why:** Gemini supports many languages natively.

---

## 🐛 Troubleshooting

### "Google API key not configured"
```bash
# Check your .env file
cat .env | grep GOOGLE_API_KEY

# Should show:
GOOGLE_API_KEY=your_actual_key_here
```

### "OpenAI API key not configured" Warning
This is normal if you're using Gemini only. The system will automatically use Gemini.

To remove the warning, ensure all tasks use Gemini:
```env
STORY_GENERATION_LLM=gemini
SCRIPT_WRITING_LLM=gemini
CAPTIONING_LLM=gemini
DIALOGUE_LLM=gemini
TRANSLATION_LLM=gemini
GENERAL_LLM=gemini
```

### Rate Limits
Gemini free tier: 15 requests/minute

If you hit rate limits:
1. Upgrade to paid tier
2. Add delays between requests
3. Use batch processing

---

## 📝 Example Usage

### Generate Comic with Gemini Only

```python
from src.main import ComicBookGenerator

# No OpenAI key needed!
generator = ComicBookGenerator(config={
    'target_audience': 'young adult',
    'quality': 'high'
})

result = generator.generate_from_text(
    text="A space adventure about first contact with aliens",
    title="First Contact",
    art_style="cinematic",
    target_pages=20
)

print(f"Generated: {result.title}")
print(f"All text generated with: Gemini 2.0 Flash")
print(f"Images generated with: ModelsLab")
```

### API Request

```bash
# Only need Google API key in .env
curl -X POST "http://localhost:8000/api/v1/generate" \
  -F "text=A hero's journey in a fantasy world" \
  -F "title=The Quest" \
  -F "art_style=fantasy" \
  -F "target_pages=15"

# All text generation uses Gemini
# All image generation uses ModelsLab
```

---

## ✅ Migration Checklist

If you were using OpenAI before:

- [ ] Get Google API key from https://makersuite.google.com/app/apikey
- [ ] Add `GOOGLE_API_KEY` to `.env`
- [ ] Update all `*_LLM` settings to `gemini`
- [ ] (Optional) Remove `OPENAI_API_KEY` from `.env`
- [ ] Test generation with `python test_setup.py`
- [ ] Verify costs are lower
- [ ] Enjoy faster generation!

---

## 🎉 Benefits Summary

### Using Gemini as Primary LLM:

✅ **Cost Savings**: 60-80% cheaper than OpenAI
✅ **Faster**: 2-3x faster response times
✅ **Simpler**: Only one API key to manage
✅ **Creative**: Excellent for storytelling
✅ **Multilingual**: Native support for many languages
✅ **Free Tier**: Generous free usage limits
✅ **Modern**: Latest Gemini 2.0 Flash model

### System Features:

✅ **Automatic Fallback**: Falls back to Gemini if OpenAI unavailable
✅ **Task Optimization**: Different temperatures per task type
✅ **Flexible**: Can still use OpenAI for specific tasks if needed
✅ **Consistent**: Same quality across all tasks
✅ **Reliable**: Robust error handling

---

## 📚 Additional Resources

- **Gemini API Docs**: https://ai.google.dev/docs
- **Get API Key**: https://makersuite.google.com/app/apikey
- **Pricing**: https://ai.google.dev/pricing
- **Rate Limits**: https://ai.google.dev/docs/rate_limits

---

## 🎯 Recommended Setup

For best results, use this configuration:

**.env:**
```env
# Primary LLM - Gemini 2.0 Flash
GOOGLE_API_KEY=your_google_api_key_here
GEMINI_MODEL=gemini-2.0-flash-exp
GEMINI_TEMPERATURE=0.8
GEMINI_MAX_TOKENS=8000

# All tasks use Gemini
STORY_GENERATION_LLM=gemini
SCRIPT_WRITING_LLM=gemini
CAPTIONING_LLM=gemini
DIALOGUE_LLM=gemini
TRANSLATION_LLM=gemini
GENERAL_LLM=gemini

# Image/Video Generation - ModelsLab
MODELSLAB_API_KEY=your_modelslab_key
IMAGE_MODEL=flux
VIDEO_MODEL=cogvideox

# OpenAI - Optional (leave blank if not using)
OPENAI_API_KEY=
```

This gives you:
- ⚡ Maximum speed
- 💰 Minimum cost
- 🎨 Excellent quality
- 🔧 Simplest setup

---

**You're all set to generate amazing comics with Gemini! 🚀**

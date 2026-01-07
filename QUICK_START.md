# Quick Start Guide - Streamlit App

## 🚀 Launch the App

```bash
# Navigate to project directory
cd "/mnt/data/HIVE/Multi Agent/comic-book-generator"

# Run the Streamlit app
streamlit run streamlit_app.py
```

The app will open at: **http://localhost:8501**

---

## 📋 Pre-Launch Checklist

### 1. Install Dependencies
```bash
pip install streamlit
# or install all requirements
pip install -r requirements.txt
```

### 2. Configure API Keys

Create `.env` file from template:
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```env
# Required
GOOGLE_API_KEY=your_google_api_key_here
MODELSLAB_API_KEY=your_modelslab_api_key_here

# Optional
OPENAI_API_KEY=your_openai_key  # Only if using OpenAI
```

### 3. Verify Installation
```bash
python test_streamlit.py
```

---

## 🎯 Testing Workflow

### Test 1: Write Story Method

1. Launch app: `streamlit run streamlit_app.py`
2. Select "📝 Write Story" tab
3. Enter a short story (e.g., "A brave knight saves a village from a dragon")
4. Configure settings:
   - Art Style: Cartoon
   - Pages: 5
   - Target Audience: Children
   - Output: PDF + Web
5. Click "🚀 Generate Comic Book"
6. Watch progress bar
7. Download results

**Expected Result:** Comic generated with 5 pages in cartoon style

### Test 2: AI Story Generator

1. Select "💡 AI Story Generator" tab
2. Enter prompt: "A space explorer discovers a new planet"
3. Choose:
   - Genre: Sci-Fi
   - Themes: Discovery, Courage
4. Click "🎲 Generate Story"
5. Review generated story
6. Configure settings (Cinematic, 10 pages)
7. Click "🚀 Generate Comic Book"

**Expected Result:** AI-generated story converted to comic

### Test 3: Upload PDF

1. Select "📄 Upload PDF" tab
2. Upload a PDF file (e.g., `/mnt/data/HIVE/Multi Agent/15.7_Laclaustra.pdf`)
3. Configure settings (Realistic, 15 pages)
4. Generate comic

**Expected Result:** PDF content converted to comic

### Test 4: Settings Configuration

1. Go to "⚙️ Settings" tab
2. Update API keys
3. Change default settings
4. Save settings

**Expected Result:** Settings saved successfully

### Test 5: Gallery View

1. Go to "📚 Gallery" tab
2. View previously generated comics
3. Click on thumbnails

**Expected Result:** Gallery displays generated comics

### Test 6: About Information

1. Go to "ℹ️ About" tab
2. Review features
3. Check technology stack
4. Read tips

**Expected Result:** Complete information displayed

---

## 🧪 Manual Testing Checklist

### UI Components
- [ ] Header displays correctly
- [ ] Sidebar shows all settings
- [ ] Tabs switch properly
- [ ] Buttons are clickable
- [ ] Progress bar animates
- [ ] Colors and gradients render
- [ ] Responsive on different screen sizes

### Functionality
- [ ] Story input accepts text
- [ ] PDF upload works
- [ ] AI story generator creates stories
- [ ] Art style selection changes
- [ ] Page slider adjusts
- [ ] Output format checkboxes work
- [ ] Generate button triggers generation
- [ ] Progress updates in real-time
- [ ] Results display correctly
- [ ] Download buttons work

### Error Handling
- [ ] Empty input shows warning
- [ ] Invalid PDF shows error
- [ ] Missing API key shows message
- [ ] Generation errors display properly
- [ ] Timeout handled gracefully

### Performance
- [ ] App loads quickly
- [ ] UI remains responsive
- [ ] Progress updates smoothly
- [ ] No memory leaks
- [ ] Handles large files

---

## 🐛 Common Issues & Solutions

### Issue: "streamlit: command not found"
**Solution:**
```bash
pip install streamlit
# or
pip install -r requirements.txt
```

### Issue: "Google API key not configured"
**Solution:**
Add your Google API key to `.env`:
```env
GOOGLE_API_KEY=your_actual_key_here
```

### Issue: "ModelsLab API error"
**Solution:**
1. Check API key in `.env`
2. Verify API key is valid
3. Check rate limits

### Issue: App won't start
**Solution:**
```bash
# Check Python version (need 3.10+)
python --version

# Reinstall dependencies
pip install -r requirements.txt --upgrade

# Clear cache
rm -rf ~/.streamlit/cache
```

### Issue: Generation fails
**Solution:**
1. Check API keys are valid
2. Verify internet connection
3. Check API rate limits
4. Review error message in UI
5. Check terminal logs

---

## 📊 Performance Benchmarks

### Expected Generation Times

| Pages | Art Style | Estimated Time |
|-------|-----------|----------------|
| 5     | Cartoon   | 2-3 minutes    |
| 10    | Manga     | 4-6 minutes    |
| 15    | Realistic | 8-12 minutes   |
| 20    | Cinematic | 12-18 minutes  |

### Resource Usage

- **Memory**: 500MB-1GB during generation
- **CPU**: Moderate (mostly API calls)
- **Network**: High (image generation)
- **Storage**: 50-200MB per comic

---

## ✅ Success Criteria

A successful test should:

1. ✅ App launches without errors
2. ✅ All tabs are accessible
3. ✅ Settings can be configured
4. ✅ Story input works (all 3 methods)
5. ✅ Generation completes successfully
6. ✅ Progress bar updates correctly
7. ✅ Results display properly
8. ✅ Downloads work
9. ✅ No console errors
10. ✅ UI is responsive

---

## 🎯 Test Scenarios

### Scenario 1: Quick Test (5 minutes)
```
1. Write simple story (2 sentences)
2. Cartoon style, 5 pages
3. PDF output only
4. Generate and download
```

### Scenario 2: Full Test (15 minutes)
```
1. Use AI story generator
2. Cinematic style, 10 pages
3. All output formats
4. Test all tabs
5. Verify all features
```

### Scenario 3: Stress Test (30 minutes)
```
1. Upload large PDF
2. Realistic style, 20 pages
3. Video output enabled
4. Monitor performance
5. Check memory usage
```

---

## 📝 Test Report Template

```markdown
## Test Report

**Date:** [Date]
**Tester:** [Name]
**Version:** 1.0.0

### Tests Performed
- [ ] UI Components
- [ ] Story Input
- [ ] PDF Upload
- [ ] AI Generator
- [ ] Settings
- [ ] Generation
- [ ] Downloads

### Results
- Passed: X/Y
- Failed: Y/Y
- Skipped: Z/Y

### Issues Found
1. [Issue description]
2. [Issue description]

### Notes
[Additional observations]
```

---

## 🚀 Next Steps After Testing

1. **If all tests pass:**
   - Deploy to production
   - Share with users
   - Monitor usage

2. **If issues found:**
   - Document issues
   - Fix critical bugs
   - Retest
   - Deploy

3. **Improvements:**
   - Gather user feedback
   - Add requested features
   - Optimize performance
   - Update documentation

---

**Ready to test? Run:** `streamlit run streamlit_app.py` 🚀

# API Testing Guide

## 🧪 Comprehensive API Test Suite

Test all API endpoints and third-party integrations (Gemini & ModelsLab).

---

## 🚀 Quick Start

### 1. Ensure Backend is Running

```bash
# Terminal 1: Start FastAPI
cd /mnt/data/HIVE/Multi\ Agent/comic-book-generator
uvicorn src.api.main:app --reload --port 8000
```

### 2. Run Tests

```bash
# Terminal 2: Run test suite
python test_api.py
```

---

## 📋 Test Coverage

### ✅ Self-Hosted API Tests

1. **Health Check** (`GET /health`)
   - Verifies API is running
   - Checks configuration status
   - Validates service availability

2. **Story Generation** (`POST /api/v1/story/generate`)
   - Tests Gemini integration
   - Validates story output
   - Checks chapter generation

3. **Caption Generation** (`POST /api/v1/caption/generate`)
   - Tests caption creation
   - Validates word limits
   - Checks context awareness

4. **Dialogue Generation** (`POST /api/v1/dialogue/generate`)
   - Tests character dialogue
   - Validates exchanges
   - Checks natural language

5. **Comic Generation** (`POST /api/v1/generate`)
   - Tests full pipeline
   - Validates job creation
   - Checks async processing

6. **Job Status** (`GET /api/v1/status/{job_id}`)
   - Tests status tracking
   - Validates progress updates
   - Checks completion status

7. **Agents Status** (`GET /api/v1/agents/status`)
   - Tests agent availability
   - Validates LLM configuration
   - Checks model settings

### ✅ Third-Party API Tests

8. **Google Gemini API**
   - Direct API call test
   - Text generation validation
   - Response quality check

9. **ModelsLab API**
   - Image generation test
   - API accessibility check
   - Queue status validation

---

## 📊 Test Output

### Example Output

```
================================================================================
COMIC BOOK GENERATOR - API TEST SUITE
================================================================================

API Base URL: http://localhost:8000
Google API Key: ✓ Configured
ModelsLab API Key: ✓ Configured
================================================================================

================================================================================
TEST 1: Health Check
================================================================================
Status: healthy
Version: 1.0.0
Gemini: True
ModelsLab: True

[✓ PASS] Health Check
    API is healthy

================================================================================
TEST 2: Google Gemini API
================================================================================
Response: Once upon a time, a small robot named Bolt discovered...

[✓ PASS] Gemini API
    Successfully generated text

================================================================================
TEST 3: ModelsLab API
================================================================================
Status: processing
Message: Request queued

[✓ PASS] ModelsLab API
    Request queued successfully

... (more tests)

================================================================================
TEST SUMMARY
================================================================================

Total Tests: 9
Passed: 9 ✓
Failed: 0 ✗
Success Rate: 100.0%

================================================================================
```

---

## 🔧 Configuration

### Environment Variables

Ensure these are set in `.env`:

```env
# API Configuration
API_BASE_URL=http://localhost:8000

# Google Gemini
GOOGLE_API_KEY=your_google_key

# ModelsLab
MODELSLAB_API_KEY=your_modelslab_key
```

---

## 🐛 Troubleshooting

### Test Failures

#### Health Check Fails
```
Problem: Connection refused
Solution: Ensure FastAPI is running on port 8000
```

#### Gemini API Fails
```
Problem: API key not configured
Solution: Add GOOGLE_API_KEY to .env file
```

#### ModelsLab API Fails
```
Problem: Invalid API key
Solution: Verify MODELSLAB_API_KEY is correct
```

#### Comic Generation Fails
```
Problem: Agents not initialized
Solution: Check all dependencies are installed
```

---

## 📝 Manual Testing

### Using cURL

#### Health Check
```bash
curl http://localhost:8000/health
```

#### Story Generation
```bash
curl -X POST http://localhost:8000/api/v1/story/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A space adventure",
    "genre": "Sci-Fi",
    "themes": ["Discovery"],
    "num_chapters": 3
  }'
```

#### Caption Generation
```bash
curl -X POST http://localhost:8000/api/v1/caption/generate \
  -H "Content-Type: application/json" \
  -d '{
    "panel_description": "Spaceship in space",
    "context": "Beginning of journey",
    "max_words": 15
  }'
```

#### Comic Generation
```bash
curl -X POST http://localhost:8000/api/v1/generate \
  -F "text=A short story about robots" \
  -F "title=Robot Story" \
  -F "art_style=cartoon" \
  -F "target_pages=5"
```

#### Job Status
```bash
curl http://localhost:8000/api/v1/status/{job_id}
```

---

## 🎯 Testing Checklist

Before deployment, ensure:

- [ ] All tests pass (100% success rate)
- [ ] Health check returns "healthy"
- [ ] Gemini API responds correctly
- [ ] ModelsLab API is accessible
- [ ] Story generation works
- [ ] Caption generation works
- [ ] Dialogue generation works
- [ ] Comic generation queues jobs
- [ ] Job status updates correctly
- [ ] All agents show "ready" status

---

## 📈 Performance Testing

### Load Testing

```bash
# Install Apache Bench
sudo apt-get install apache2-utils

# Test health endpoint
ab -n 1000 -c 10 http://localhost:8000/health

# Test story generation
ab -n 100 -c 5 -p story_payload.json \
  -T application/json \
  http://localhost:8000/api/v1/story/generate
```

### Response Time Benchmarks

| Endpoint | Expected Time | Acceptable |
|----------|---------------|------------|
| Health Check | <100ms | <500ms |
| Story Generation | 5-15s | <30s |
| Caption Generation | 2-5s | <10s |
| Dialogue Generation | 2-5s | <10s |
| Comic Generation (queue) | <1s | <2s |
| Job Status | <100ms | <500ms |

---

## 🔐 Security Testing

### API Key Validation

```bash
# Test without API key
curl -X POST http://localhost:8000/api/v1/story/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "test"}'

# Should return 401 or 500 with proper error
```

### Rate Limiting

```bash
# Send multiple rapid requests
for i in {1..100}; do
  curl http://localhost:8000/health &
done
wait

# Should handle gracefully
```

---

## 📊 Monitoring

### Check Logs

```bash
# View API logs
tail -f logs/api.log

# View agent logs
tail -f logs/agents.log
```

### Metrics to Monitor

- Request count
- Response times
- Error rates
- API key usage
- Queue length
- Agent status

---

## ✅ CI/CD Integration

### GitHub Actions

```yaml
name: API Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run API tests
        run: python test_api.py
        env:
          GOOGLE_API_KEY: ${{ secrets.GOOGLE_API_KEY }}
          MODELSLAB_API_KEY: ${{ secrets.MODELSLAB_API_KEY }}
```

---

## 🎯 Next Steps

After all tests pass:

1. ✅ Deploy to staging
2. ✅ Run integration tests
3. ✅ Perform load testing
4. ✅ Monitor for 24 hours
5. ✅ Deploy to production

---

**Run tests before every deployment! 🚀**

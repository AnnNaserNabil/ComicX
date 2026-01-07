"""
Comprehensive API Test Suite
Tests all endpoints and third-party API integrations
"""

import asyncio
import json
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "xiaomi/mimo-v2-flash:free")
MODELSLAB_API_KEY = os.getenv("MODELSLAB_API_KEY")

print("=" * 80)
print("COMIC BOOK GENERATOR - API TEST SUITE")
print("=" * 80)
print(f"\nAPI Base URL: {API_BASE_URL}")
print(f"Google API Key: {'✓ Configured' if GOOGLE_API_KEY else '✗ Missing'}")
print(f"OpenRouter API Key: {'✓ Configured' if OPENROUTER_API_KEY else '✗ Missing'}")
print(f"ModelsLab API Key: {'✓ Configured' if MODELSLAB_API_KEY else '✗ Missing'}")
print("=" * 80)


class APITester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []

    def log_test(self, name, passed, message=""):
        status = "✓ PASS" if passed else "✗ FAIL"
        self.test_results.append({"name": name, "passed": passed, "message": message})
        print(f"\n[{status}] {name}")
        if message:
            print(f"    {message}")

    def test_health_check(self):
        """Test 1: Health Check Endpoint"""
        print("\n" + "=" * 80)
        print("TEST 1: Health Check")
        print("=" * 80)
        
        try:
            response = self.session.get(f"{self.base_url}/health")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Status: {data.get('status')}")
                print(f"Version: {data.get('version')}")
                print(f"Gemini: {data.get('gemini_configured')}")
                print(f"ModelsLab: {data.get('modelslab_configured')}")
                
                self.log_test(
                    "Health Check",
                    data.get('status') == 'healthy',
                    f"API is {data.get('status')}"
                )
            else:
                self.log_test("Health Check", False, f"Status code: {response.status_code}")
                
        except Exception as e:
            self.log_test("Health Check", False, f"Error: {e}")

    def test_openrouter_api(self):
        """Test 2: OpenRouter API Integration"""
        print("\n" + "=" * 80)
        print("TEST 2: OpenRouter API")
        print("=" * 80)
        
        if not OPENROUTER_API_KEY:
            self.log_test("OpenRouter API", False, "API key not configured")
            return
        
        try:
            # Test OpenRouter API call using OpenAI client
            from openai import OpenAI
            
            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=OPENROUTER_API_KEY,
                default_headers={
                    "HTTP-Referer": "https://github.com/google-gemini/comic-book-generator",
                    "X-Title": "Comic Book Generator",
                }
            )
            
            response = client.chat.completions.create(
                model=OPENROUTER_MODEL,
                messages=[
                    {"role": "user", "content": "Write a one-sentence story about a robot."}
                ]
            )
            
            if response and response.choices[0].message.content:
                content = response.choices[0].message.content
                print(f"Response: {content[:100]}...")
                self.log_test("OpenRouter API", True, "Successfully generated text")
            else:
                self.log_test("OpenRouter API", False, "No response from OpenRouter")
                
        except Exception as e:
            self.log_test("OpenRouter API", False, f"Error: {e}")

    def test_modelslab_api(self):
        """Test 3: ModelsLab API Integration"""
        print("\n" + "=" * 80)
        print("TEST 3: ModelsLab API")
        print("=" * 80)
        
        if not MODELSLAB_API_KEY:
            self.log_test("ModelsLab API", False, "API key not configured")
            return
        
        try:
            # Test ModelsLab API using the library
            from modelslab_py.core.client import Client
            from modelslab_py.core.apis.community import Community
            from modelslab_py.schemas.community import Text2Image
            
            client = Client(api_key=MODELSLAB_API_KEY)
            api = Community(client=client)
            
            schema = Text2Image(
                model_id="flux",
                prompt="test image, simple cartoon robot",
                negative_prompt="blurry, low quality",
                width=512,
                height=512,
                samples=1,
                num_inference_steps=20
            )
            
            response = api.text_to_image(schema)
            
            if response.get("status") in ["success", "processing"]:
                print(f"Status: {response.get('status')}")
                self.log_test("ModelsLab API", True, f"API is accessible (Status: {response.get('status')})")
            else:
                error_msg = response.get("message", "Unknown error")
                self.log_test("ModelsLab API", False, f"Error: {error_msg}")
                
        except Exception as e:
            self.log_test("ModelsLab API", False, f"Error: {e}")

    def test_story_generation_endpoint(self):
        """Test 4: Story Generation Endpoint"""
        print("\n" + "=" * 80)
        print("TEST 4: Story Generation Endpoint")
        print("=" * 80)
        
        try:
            payload = {
                "prompt": "A brave knight on a quest",
                "genre": "Fantasy",
                "themes": ["Courage", "Adventure"],
                "num_chapters": 3
            }
            
            response = self.session.post(
                f"{self.base_url}/api/v1/story/generate",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"Story length: {len(data.get('story', ''))} characters")
                print(f"Chapters: {len(data.get('chapters', []))}")
                print(f"Word count: {data.get('word_count', 0)}")
                
                self.log_test(
                    "Story Generation",
                    len(data.get('story', '')) > 0,
                    f"Generated {data.get('word_count', 0)} words"
                )
            else:
                self.log_test("Story Generation", False, f"Status code: {response.status_code}")
                
        except Exception as e:
            self.log_test("Story Generation", False, f"Error: {e}")

    def test_caption_generation_endpoint(self):
        """Test 5: Caption Generation Endpoint"""
        print("\n" + "=" * 80)
        print("TEST 5: Caption Generation Endpoint")
        print("=" * 80)
        
        try:
            payload = {
                "panel_description": "A spaceship flying through stars",
                "context": "Beginning of the journey",
                "max_words": 15
            }
            
            response = self.session.post(
                f"{self.base_url}/api/v1/caption/generate",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                caption = data.get('caption', '')
                print(f"Caption: {caption}")
                
                self.log_test(
                    "Caption Generation",
                    len(caption) > 0,
                    f"Generated: {caption}"
                )
            else:
                self.log_test("Caption Generation", False, f"Status code: {response.status_code}")
                
        except Exception as e:
            self.log_test("Caption Generation", False, f"Error: {e}")

    def test_dialogue_generation_endpoint(self):
        """Test 6: Dialogue Generation Endpoint"""
        print("\n" + "=" * 80)
        print("TEST 6: Dialogue Generation Endpoint")
        print("=" * 80)
        
        try:
            payload = {
                "characters": ["Hero", "Villain"],
                "scene_description": "Final confrontation",
                "context": "Hero has discovered the truth",
                "num_exchanges": 2
            }
            
            response = self.session.post(
                f"{self.base_url}/api/v1/dialogue/generate",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                dialogue = data.get('dialogue', [])
                print(f"Exchanges: {len(dialogue)}")
                for line in dialogue[:2]:
                    print(f"  {line.get('character')}: {line.get('text')}")
                
                self.log_test(
                    "Dialogue Generation",
                    len(dialogue) > 0,
                    f"Generated {len(dialogue)} exchanges"
                )
            else:
                self.log_test("Dialogue Generation", False, f"Status code: {response.status_code}")
                
        except Exception as e:
            self.log_test("Dialogue Generation", False, f"Error: {e}")

    def test_comic_generation_endpoint(self):
        """Test 7: Comic Generation Endpoint"""
        print("\n" + "=" * 80)
        print("TEST 7: Comic Generation Endpoint (Text)")
        print("=" * 80)
        
        try:
            payload = {
                "text": "A short story about a robot learning to feel emotions.",
                "title": "Test Comic",
                "art_style": "cartoon",
                "target_pages": 5,
                "target_audience": "general"
            }
            
            response = self.session.post(
                f"{self.base_url}/api/v1/generate",
                data=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                job_id = data.get('job_id')
                print(f"Job ID: {job_id}")
                print(f"Status: {data.get('status')}")
                
                self.log_test(
                    "Comic Generation",
                    job_id is not None,
                    f"Job queued: {job_id}"
                )
                
                # Test status endpoint
                if job_id:
                    self.test_job_status(job_id)
                    
            else:
                self.log_test("Comic Generation", False, f"Status code: {response.status_code}")
                
        except Exception as e:
            self.log_test("Comic Generation", False, f"Error: {e}")

    def test_job_status(self, job_id):
        """Test 8: Job Status Endpoint"""
        print("\n" + "=" * 80)
        print("TEST 8: Job Status Endpoint")
        print("=" * 80)
        
        try:
            response = self.session.get(
                f"{self.base_url}/api/v1/status/{job_id}",
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"Job ID: {data.get('job_id')}")
                print(f"Status: {data.get('status')}")
                print(f"Progress: {data.get('progress', 0):.1%}")
                print(f"Stage: {data.get('current_stage')}")
                
                self.log_test(
                    "Job Status",
                    True,
                    f"Status: {data.get('status')}"
                )
            else:
                self.log_test("Job Status", False, f"Status code: {response.status_code}")
                
        except Exception as e:
            self.log_test("Job Status", False, f"Error: {e}")

    def test_agents_status_endpoint(self):
        """Test 9: Agents Status Endpoint"""
        print("\n" + "=" * 80)
        print("TEST 9: Agents Status Endpoint")
        print("=" * 80)
        
        try:
            response = self.session.get(
                f"{self.base_url}/api/v1/agents/status",
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"Processing Agent: {data.get('processing_agent')}")
                print(f"Content Agent: {data.get('content_agent')}")
                print(f"Visual Agent: {data.get('visual_agent')}")
                print(f"Synthesis Agent: {data.get('synthesis_agent')}")
                print(f"Text Agent: {data.get('text_agent')}")
                print(f"Primary LLM: {data.get('llm_primary')}")
                print(f"Image Model: {data.get('image_model')}")
                
                self.log_test(
                    "Agents Status",
                    all(v == "ready" for k, v in data.items() if k.endswith('_agent')),
                    "All agents ready"
                )
            else:
                self.log_test("Agents Status", False, f"Status code: {response.status_code}")
                
        except Exception as e:
            self.log_test("Agents Status", False, f"Error: {e}")

    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        
        total = len(self.test_results)
        passed = sum(1 for r in self.test_results if r['passed'])
        failed = total - passed
        
        print(f"\nTotal Tests: {total}")
        print(f"Passed: {passed} ✓")
        print(f"Failed: {failed} ✗")
        print(f"Success Rate: {(passed/total*100):.1f}%")
        
        if failed > 0:
            print("\nFailed Tests:")
            for result in self.test_results:
                if not result['passed']:
                    print(f"  ✗ {result['name']}: {result['message']}")
        
        print("\n" + "=" * 80)
        
        return passed == total


def main():
    """Run all tests"""
    tester = APITester(API_BASE_URL)
    
    # Run tests
    tester.test_health_check()
    tester.test_openrouter_api()
    tester.test_modelslab_api()
    tester.test_story_generation_endpoint()
    tester.test_caption_generation_endpoint()
    tester.test_dialogue_generation_endpoint()
    tester.test_comic_generation_endpoint()
    tester.test_agents_status_endpoint()
    
    # Print summary
    all_passed = tester.print_summary()
    
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()

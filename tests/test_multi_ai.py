#!/usr/bin/env python3
"""Quick test for multi-AI setup"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_models():
    API_KEY = os.getenv('OPENROUTER_API_KEY')
    models = [
        'qwen/qwen3.6-plus',
        'anthropic/claude-opus-4.6-fast', 
        'openrouter/elephant-alpha',
    ]
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    print("🧪 Testing AI model connectivity...\n")
    
    for model in models:
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": "Reply 'OK' only"}],
            "max_tokens": 10
        }
        
        try:
            resp = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers, json=payload, timeout=30
            )
            if resp.status_code == 200:
                print(f"✅ {model}")
            else:
                print(f"❌ {model} - HTTP {resp.status_code}")
        except Exception as e:
            print(f"❌ {model} - {str(e)[:50]}")

if __name__ == "__main__":
    test_models()
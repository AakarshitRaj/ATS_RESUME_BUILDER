import google.generativeai as genai

# Replace with your NEW API key
genai.configure(api_key="your api key here")

print("📋 Available Gemini Models:\n")
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"✅ {model.name}")
        print(f"   Description: {model.description}")
        print()

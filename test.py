import google.generativeai as genai

genai.configure(api_key="AIzaSyCQLVX0tIQG6vac3s8-gEvX9WUwz564sak")

models = genai.list_models()

for m in models:
    print("Model name:", m.name)
    if hasattr(m, "display_name"):
        print("Display name:", m.display_name)
    if hasattr(m, "description"):
        print("Description:", m.description)
    if hasattr(m, "supported_generation_methods"):
        print("Supported methods:", m.supported_generation_methods)
    print("-" * 60)

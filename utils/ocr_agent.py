import base64
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"), timeout=60.0)

def extract_text_from_image(image_path: str) -> str:
    print("🖼️ OCR Agent reading prescription image...")

    # Read and encode image to base64
    with open(image_path, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode("utf-8")

    # Detect file extension
    ext = image_path.split(".")[-1].lower()
    media_type = f"image/{'jpeg' if ext in ['jpg','jpeg'] else ext}"

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{media_type};base64,{image_data}"
                        }
                    },
                    {
                        "type": "text",
                        "text": """You are a medical OCR agent. 
                        Extract all medical information from this prescription/report image.
                        Return the extracted text in this format:
                        
                        Patient Name: ...
                        Age: ...
                        Gender: ...
                        Diagnosis: ...
                        Prescription/Findings: ...
                        Doctor: ...
                        
                        Extract everything you can read clearly."""
                    }
                ]
            }
        ],
        max_tokens=1000
    )

    return response.choices[0].message.content.strip()
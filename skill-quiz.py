from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import os

# Load the .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Access the GOOGLE_API_KEY environment variable
api_key = os.getenv('GOOGLE_API_KEY')

# Configure Google Generative AI with API key
genai.configure(api_key=api_key)

# Define a request model for the technology stack input
class TechStackRequest(BaseModel):
    stack: str

# Create an endpoint for generating a skill quiz based on the technology stack
@app.post("/generate-skill-quiz")
async def generate_skill_quiz(tech_stack: TechStackRequest):
    try:
        # Create the prompt based on user input
        prompt = f"Generate a skill quiz for {tech_stack.stack}."
        
        # Call the Generative Model to generate content
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        
        # Return the generated quiz content
        return {"quiz": response.text}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# Create a GET endpoint to inform users about the correct usage
@app.get("/generate-skill-quiz")
async def get_info():
    return {
        "message": "To generate a skill quiz, use the POST method at /generate-skill-quiz with a JSON object containing the technology stack.",
        "example": {
            "stack": "Python, FastAPI, and Google Generative AI"
        }
    }
    
# To run the app with Uvicorn
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
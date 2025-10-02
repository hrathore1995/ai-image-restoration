import os
import openai
import requests
from dotenv import load_dotenv

# Load the new environment variable
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Create the OpenAI client
client = openai.OpenAI()

def restore_image(image_path: str):
    """
    Sends a damaged image to the OpenAI (DALL-E 2) API for restoration.
    """
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables. Check your .env file.")

    try:
        # OpenAI's image edit API requires the image file to be opened in binary read mode
        with open(image_path, "rb") as image_file:
            # In restore.py

            response = client.images.edit(
    model="dall-e-2",
    image=image_file,
    prompt=(
        "Restore this photograph while keeping the subject’s original features "
        "and natural colors intact. Remove damage, scratches, and age-related artifacts, "
        "but do not alter facial characteristics, expressions, or tones. The restored image "
        "should look as close as possible to the original photo, just cleaned and clear."
    ),
    n=1,
    size="1024x1024"
)

        
        # The API returns a URL to the newly created image
        restored_image_url = response.data[0].url

        # Download the image from the URL
        image_data = requests.get(restored_image_url).content
        
        # Save the new image
        output_dir = "temp"
        os.makedirs(output_dir, exist_ok=True)
        original_filename = os.path.basename(image_path)
        restored_filename = f"restored_openai_{original_filename}"
        output_path = os.path.join(output_dir, restored_filename)
        
        with open(output_path, "wb") as f:
            f.write(image_data)
            
        return output_path, restored_filename

    except openai.OpenAIError as e:
        # Handle potential API errors gracefully
        raise RuntimeError(f"OpenAI API Error: {e}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {e}")
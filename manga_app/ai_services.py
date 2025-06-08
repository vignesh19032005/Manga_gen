import os
import json
import base64
import requests
from PIL import Image
from io import BytesIO
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MangaAIService:
    def __init__(self):
        # Initialize Google Gemini
        google_api_key = os.getenv('GOOGLE_API_KEY')
        if not google_api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        genai.configure(api_key=google_api_key)
        self.story_model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Initialize Stability AI
        self.stability_api_key = os.getenv('STABILITY_API_KEY')
        if not self.stability_api_key:
            raise ValueError("STABILITY_API_KEY not found in environment variables")
        self.stability_api_host = "https://api.stability.ai"
        self.engine_id = "stable-diffusion-xl-1024-v1-0"  # SDXL for high quality
        
    def _generate_image(self, prompt, art_style, negative_prompt=""):
        """Generate image using Stability AI API"""
        try:
            url = f"{self.stability_api_host}/v1/generation/{self.engine_id}/text-to-image"
            
            # Enhance prompt for manga-style generation
            enhanced_prompt = f"""Manga panel, {art_style} style. {prompt}
Detailed art with clean linework, dynamic composition, expressive characters.
High quality manga artwork, professional illustration quality."""

            # Negative prompt to avoid unwanted elements
            base_negative = """
            poor quality, low quality, blurry, distorted, deformed,
            ugly, amateur, unprofessional, poorly drawn, bad anatomy,
            watermark, signature, text, words, low resolution
            """
            full_negative = f"{base_negative}, {negative_prompt}"

            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.stability_api_key}",
            }

            payload = {
                "text_prompts": [
                    {
                        "text": enhanced_prompt,
                        "weight": 1
                    },
                    {
                        "text": full_negative,
                        "weight": -1
                    }
                ],
                "cfg_scale": 7,
                "height": 1024,
                "width": 1024,
                "samples": 1,
                "steps": 30,
                "style_preset": "anime"
            }

            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code != 200:
                raise Exception(f"Non-200 response: {str(response.text)}")

            data = response.json()
            
            if "artifacts" not in data or len(data["artifacts"]) == 0:
                raise Exception("No image generated")
                
            # Convert base64 to image and save
            image_data = base64.b64decode(data["artifacts"][0]["base64"])
            
            # Generate unique filename
            import uuid
            filename = f"panel_{uuid.uuid4()}.png"
            media_root = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media')
            filepath = os.path.join(media_root, 'panels', filename)
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # Save image
            with open(filepath, 'wb') as f:
                f.write(image_data)
                
            return f"/media/panels/{filename}"
            
        except Exception as e:
            print(f"Error generating image: {str(e)}")
            raise

    def generate_story(self, genre, length, audience, premise, elements):
        """Generate a manga story using Gemini"""
        try:
            print(f"Generating story with parameters: genre={genre}, length={length}, audience={audience}")
            
            # First, analyze if the premise relates to existing content
            analysis_prompt = f"""Analyze if this story premise relates to any existing manga, anime, movie, or series:
Premise: {premise}
Genre: {genre}
Target Audience: {audience}

If it does, provide:
1. The original work's name
2. Key elements that should be preserved
3. Core themes to maintain
If not, respond with: ORIGINAL_STORY"""

            print("Analyzing premise for existing references...")
            analysis = self.story_model.generate_content(analysis_prompt)
            
            if "ORIGINAL_STORY" in analysis.text:
                is_adaptation = False
                reference_material = ""
            else:
                is_adaptation = True
                reference_material = analysis.text
                print(f"Found reference material: {reference_material}")

            # Craft the main story prompt
            prompt = f"""Create a flowing, engaging manga story based on these parameters:
Genre: {genre}
Length: {length}
Target Audience: {audience}
Story Elements: {', '.join(elements)}
Basic Premise: {premise}

{"--- ADAPTATION GUIDELINES ---" if is_adaptation else ""}
{reference_material if is_adaptation else ""}

Writing Guidelines:
1. {"While maintaining core elements from the original work, incorporate the requested changes and make the story fresh and unique." if is_adaptation else "Create an original and engaging narrative that feels fresh and unique."}
2. Focus on visual storytelling and dramatic moments
3. Develop characters naturally through their actions and dialogue
4. Build tension and emotional investment
5. Include clear story progression and satisfying resolution
6. {"Balance familiarity with innovation, keeping what works while adding new elements." if is_adaptation else "Build an innovative and compelling world that draws readers in."}
7. Adapt the tone and complexity for the target audience: {audience}
8. Incorporate the requested genre elements: {', '.join(elements)}

Additional Elements to Include:
- Memorable character moments
- Clear character motivations
- Environmental descriptions
- Emotional peaks and valleys
- Action sequences where appropriate
- Natural dialogue flow

Begin with the title, then tell the complete story as a flowing narrative without section breaks or special formatting."""

            print("Sending story generation prompt to Gemini...")
            response = self.story_model.generate_content(prompt)
            print("Received response from Gemini")

            if not response.text:
                raise Exception("Empty response from Gemini")

            return {
                'success': True,
                'story': response.text
            }
        except Exception as e:
            print(f"Error in generate_story: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    def extract_key_scenes(self, story):
        """Extract key scenes from the story for panel generation"""
        try:
            print("Extracting key scenes from story...")
            
            prompt = f"""Extract key visual scenes from this story that would make perfect manga panels. Each scene should be a specific moment that advances the story while being visually compelling.

Story: {story}

Guidelines for scene descriptions:
1. Each scene must be a specific story moment, not a generic description
2. Include clear visual details that an artist can draw:
   - Character expressions and poses
   - Action and movement
   - Environmental details
   - Lighting and atmosphere
3. Focus on dramatic, emotional, or action-packed moments
4. Make each scene description a single, detailed line
5. Follow the story's progression from start to finish
6. Capture key plot points and character moments

Example format (DO NOT use these scenes, generate from the actual story):
Scene 1: Akira stands frozen in shock, his eyes glowing with newfound time powers as cherry blossoms hang suspended in mid-air around him
Scene 2: Master Chen demonstrates a defensive stance in his dimly lit dojo, shadows dancing on the wall as incense smoke swirls
Scene 3: Akira and his rival clash in mid-air above the city, their energy trails forming a spectacular helix pattern in the night sky

Important:
- Make each scene description specific to THIS story
- Include enough detail for art generation
- Maintain story progression
- Focus on visually interesting moments
- Keep descriptions concise but detailed
- Don't use generic scene descriptions
- Don't skip important plot points

Format each scene as:
Scene [number]: [Specific, detailed visual description of the exact moment]"""

            print("Requesting scene extraction from Gemini...")
            response = self.story_model.generate_content(prompt)
            print("Received scene extraction response")

            if not response.text:
                raise Exception("Empty response from Gemini during scene extraction")

            # Process the scenes
            scenes = []
            lines = [line.strip() for line in response.text.split('\n') if line.strip()]
            
            for line in lines:
                if line.lower().startswith('scene') and ':' in line:
                    # Extract everything after the colon and trim
                    scene_desc = line.split(':', 1)[1].strip()
                    if scene_desc and not scene_desc.lower().startswith('a scene where'):
                        scenes.append(scene_desc)
            
            print(f"Extracted {len(scenes)} scenes")
            
            # Validate scene quality
            if not scenes or all(len(scene.split()) < 8 for scene in scenes):
                print("Warning: Scenes too short or generic, regenerating...")
                # Try one more time with a stronger emphasis on detail
                retry_prompt = f"""Generate specific, detailed manga panel descriptions for this story. Each scene must be a concrete moment with visual details.

Story: {story}

Requirements:
- Each scene must be at least 15 words
- Include specific character actions and expressions
- Describe the environment and atmosphere
- Focus on dramatic moments
- NO generic descriptions
- NO placeholder scenes

Format: Scene [number]: [Detailed visual description]"""
                
                retry_response = self.story_model.generate_content(retry_prompt)
                if retry_response.text:
                    scenes = []
                    for line in retry_response.text.split('\n'):
                        if line.lower().startswith('scene') and ':' in line:
                            scene_desc = line.split(':', 1)[1].strip()
                            if scene_desc and len(scene_desc.split()) >= 8:
                                scenes.append(scene_desc)

            return {
                'success': True,
                'scenes': scenes
            }
        except Exception as e:
            print(f"Error in extract_key_scenes: {str(e)}")
            print(f"Full response text: {response.text if 'response' in locals() else 'No response'}")
            return {
                'success': False,
                'error': str(e)
            }

    def generate_panels(self, scene_description, art_style):
        """Generate manga panel using Stability AI"""
        try:
            print(f"Generating panel for scene: {scene_description}")
            
            # Craft the image generation prompt
            prompt = f"""Create a detailed manga panel:
Scene: {scene_description}

Required elements:
- Clear manga/anime art style
- Strong visual composition
- Dynamic character poses
- Detailed backgrounds
- Appropriate lighting and shadows
- Emotional expressions
- Action-oriented where needed
- Panel-ready composition

Style notes:
- Clean linework
- Proper manga perspective
- Character proportions matching {art_style} style
- Suitable tone and atmosphere for the scene"""

            # Generate negative prompt based on art style
            negative_prompt = ""
            if "shoujo" in art_style.lower():
                negative_prompt += "dark themes, gore, masculine style"
            elif "seinen" in art_style.lower():
                negative_prompt += "childish elements, cute style, shoujo elements"
            elif "action" in art_style.lower():
                negative_prompt += "static poses, passive scenes, slice of life"

            print("Sending image generation request...")
            image_url = self._generate_image(prompt, art_style, negative_prompt)
            
            return {
                'success': True,
                'image_url': image_url
            }
            
        except Exception as e:
            print(f"Error in generate_panels: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

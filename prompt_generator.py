# prompt_generator.py - Enhanced for Better Quality
import random

class PromptGenerator:
    def __init__(self):
        self.art_styles = [
            "professional photography", "digital art masterpiece", "oil painting", 
            "watercolor painting", "realistic painting", "fantasy art", 
            "concept art", "studio photography"
        ]
        
        self.quality_words = [
            "highly detailed", "masterpiece", "award winning", "professional quality",
            "stunning", "beautiful", "intricate details", "atmospheric lighting",
            "sharp focus", "vivid colors", "8k resolution", "photorealistic"
        ]
    
    def generate_art_prompt(self, story_elements: dict, style_preference: str = "auto") -> dict:
        """Generate enhanced art prompt for better quality"""
        
        # Build clear, detailed description
        base_description = story_elements.get('summary', '')
        
        # Add specific details for better AI understanding
        if story_elements.get('characters'):
            chars = ', '.join(story_elements['characters'][:2])
            base_description = f"A detailed scene showing {chars}"
        
        # Add clear setting
        if story_elements.get('places'):
            place = story_elements['places'][0]
            base_description += f" in a beautiful {place}"
        
        # Add color information clearly
        if story_elements.get('colors'):
            colors = ', '.join(story_elements['colors'][:2])
            base_description += f" with prominent {colors} colors"
        
        # Choose appropriate style
        if style_preference == "auto":
            style = random.choice(self.art_styles)
        else:
            style = style_preference
        
        # Add mood-based atmosphere
        mood = story_elements.get('mood', 'neutral')
        atmosphere_map = {
            'happy': 'bright and cheerful lighting, warm atmosphere',
            'dark': 'dramatic lighting, mysterious atmosphere', 
            'calm': 'soft lighting, peaceful and serene atmosphere',
            'exciting': 'dynamic lighting, energetic atmosphere',
            'neutral': 'natural lighting, beautiful atmosphere'
        }
        atmosphere = atmosphere_map.get(mood, 'beautiful natural lighting')
        
        # Add multiple quality terms
        quality_terms = ", ".join(random.sample(self.quality_words, 3))
        
        # Build enhanced prompts
        positive_prompt = f"{base_description}, {style}, {atmosphere}, {quality_terms}"
        
        # Comprehensive negative prompt
        negative_prompt = "blurry, low quality, distorted, ugly, bad anatomy, extra limbs, deformed, pixelated, grainy, low resolution, amateur, watermark, signature, text, cropped, worst quality"
        
        return {
            'positive_prompt': positive_prompt,
            'negative_prompt': negative_prompt,
            'style': style,
            'mood': mood,
            'atmosphere': atmosphere
        }
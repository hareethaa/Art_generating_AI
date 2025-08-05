# art_generator.py - Enhanced Quality Version
import torch
from PIL import Image
import streamlit as st

try:
    from diffusers import StableDiffusionPipeline
    DIFFUSERS_AVAILABLE = True
except ImportError:
    DIFFUSERS_AVAILABLE = False

class ArtGenerator:
    def __init__(self):
        self.pipe = None
        self.device = "cpu"
        st.info("🔧 Using CPU mode for stability")
    
    def load_model(self):
        """Load the AI model with better settings"""
        if not DIFFUSERS_AVAILABLE:
            st.error("Please install diffusers: pip install diffusers")
            return False
        
        try:
            st.info("🤖 Loading high-quality AI model...")
            
            self.pipe = StableDiffusionPipeline.from_pretrained(
                "runwayml/stable-diffusion-v1-5",
                torch_dtype=torch.float32,
                safety_checker=None,
                requires_safety_checker=False
            )
            
            st.success("✅ High-quality model loaded!")
            return True
            
        except Exception as e:
            st.error(f"❌ Error loading model: {str(e)}")
            return False
    
    def generate_image(self, positive_prompt: str, negative_prompt: str = "", 
                      width: int = 512, height: int = 512, steps: int = 20):
        """Generate high-quality image"""
        if self.pipe is None:
            if not self.load_model():
                return None
        
        try:
            # Enhanced prompts for better quality
            enhanced_positive = f"{positive_prompt}, highly detailed, professional photography, sharp focus, vivid colors, masterpiece, 8k resolution"
            
            enhanced_negative = f"{negative_prompt}, blurry, low quality, distorted, ugly, bad anatomy, extra limbs, deformed, pixelated, grainy, low resolution, amateur"
            
            st.info(f"🎨 Generating HIGH QUALITY image...")
            st.info("⏳ This will take 3-7 minutes for better results")
            
            # Generate with better settings
            result = self.pipe(
                prompt=enhanced_positive,
                negative_prompt=enhanced_negative,
                width=512,  # Good resolution
                height=512,
                num_inference_steps=30,  # More steps = better quality
                guidance_scale=9.0,  # Higher guidance = follows prompt better
                generator=torch.Generator().manual_seed(42)  # Reproducible results
            )
            
            st.success("🎉 High-quality image generated!")
            return result.images[0]
            
        except Exception as e:
            st.error(f"❌ Error generating image: {str(e)}")
            return None
# art_generator.py - AI Art Generation
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
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
    
    def load_model(self):
        """Load the AI model"""
        if not DIFFUSERS_AVAILABLE:
            st.error("Please install diffusers: pip install diffusers")
            return False
        
        try:
            st.info("🤖 Loading AI model... (1-2 minutes first time)")
            
            self.pipe = StableDiffusionPipeline.from_pretrained(
                "runwayml/stable-diffusion-v1-5",
                torch_dtype=torch.float32,
                safety_checker=None,
                requires_safety_checker=False,
                low_cpu_mem_usage=True
            )
            
            self.pipe = self.pipe.to(self.device)
            
            # Optimizations
            if hasattr(self.pipe, "enable_attention_slicing"):
                self.pipe.enable_attention_slicing()
            
            st.success("✅ AI model loaded successfully!")
            return True
            
        except Exception as e:
            st.error(f"❌ Error loading model: {str(e)}")
            return False
    
    def generate_image(self, positive_prompt: str, negative_prompt: str = "", 
                      width: int = 512, height: int = 512, steps: int = 20):
        """Generate image from prompts"""
        if self.pipe is None:
            if not self.load_model():
                return None
        
        try:
            with torch.autocast(self.device):
                result = self.pipe(
                    prompt=positive_prompt,
                    negative_prompt=negative_prompt,
                    width=width,
                    height=height,
                    num_inference_steps=steps,
                    guidance_scale=7.5
                )
            
            return result.images[0]
            
        except Exception as e:
            st.error(f"Error generating image: {str(e)}")
            return None
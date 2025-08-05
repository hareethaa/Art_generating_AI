# utils.py - Helper Functions
import os
import json
from datetime import datetime

def create_filename(story_snippet: str = "artwork") -> str:
    """Create unique filename"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_snippet = "".join(c for c in story_snippet if c.isalnum() or c in (' ', '-', '_')).strip()
    safe_snippet = safe_snippet.replace(' ', '_')[:15]
    return f"{safe_snippet}_{timestamp}.png"

def save_image(image, filename: str, output_dir: str = "generated_art"):
    """Save generated image"""
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    image.save(filepath)
    return filepath

def get_example_stories():
    """Return example stories"""
    return {
        "Custom Story": "",
        "Pandas Playing": "Two cute pandas are playing in a green bamboo forest. One panda is climbing while another sits eating bamboo leaves. The scene is peaceful and happy.",
        
        "Magical Forest": "A young wizard walks through an enchanted forest with glowing blue mushrooms and golden fireflies. Ancient oak trees sparkle with silver light.",
        
        "Ocean Adventure": "A brave sailor stands on a ship during a beautiful sunset. Orange and pink colors fill the sky while dolphins jump in the blue water.",
        
        "Mountain Castle": "An ancient stone castle sits on a snowy mountain peak. Dark storm clouds gather while lightning illuminates the rocky cliffs below."
    }

def log_generation(story: str, elements: dict, prompt_data: dict, success: bool):
    """Log generation details"""
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'story_snippet': story[:100],
        'elements': elements,
        'prompt_data': prompt_data,
        'success': success
    }
    
    log_file = "generation_log.json"
    logs = []
    
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r') as f:
                logs = json.load(f)
        except:
            logs = []
    
    logs.append(log_entry)
    logs = logs[-50:]  # Keep last 50
    
    with open(log_file, 'w') as f:
        json.dump(logs, f, indent=2)
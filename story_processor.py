# story_processor.py - Story Analysis Module
class StoryProcessor:
    def __init__(self):
        self.color_words = [
            'red', 'blue', 'green', 'yellow', 'purple', 'orange', 'pink', 'brown',
            'black', 'white', 'gray', 'grey', 'silver', 'gold', 'crimson', 'azure',
            'emerald', 'violet', 'amber', 'scarlet', 'turquoise', 'magenta', 'golden'
        ]
        
        self.place_words = [
            'forest', 'castle', 'mountain', 'ocean', 'sea', 'city', 'village', 'garden',
            'house', 'palace', 'cave', 'desert', 'lake', 'river', 'sky', 'clouds',
            'field', 'meadow', 'valley', 'hill', 'beach', 'island', 'tower', 'bridge'
        ]
        
        self.mood_words = {
            'happy': ['happy', 'joyful', 'bright', 'beautiful', 'peaceful', 'magical', 'wonderful'],
            'dark': ['dark', 'scary', 'stormy', 'mysterious', 'dramatic', 'gloomy', 'sinister'],
            'calm': ['calm', 'serene', 'quiet', 'gentle', 'soft', 'tranquil', 'still'],
            'exciting': ['exciting', 'adventure', 'fast', 'dynamic', 'energetic', 'thrilling']
        }
    
    def extract_visual_elements(self, story: str) -> dict:
        """Extract visual elements from story"""
        story_lower = story.lower()
        
        # Find colors
        found_colors = [color for color in self.color_words if color in story_lower]
        
        # Find places
        found_places = [place for place in self.place_words if place in story_lower]
        
        # Find characters (simple approach)
        character_words = [
            'person', 'man', 'woman', 'child', 'boy', 'girl', 'king', 'queen', 
            'princess', 'prince', 'wizard', 'witch', 'knight', 'dragon', 
            'fairy', 'angel', 'hero', 'warrior', 'panda', 'cat', 'dog', 'bird'
        ]
        found_characters = [char for char in character_words if char in story_lower]
        
        # Determine mood
        mood = 'neutral'
        mood_scores = {}
        for mood_type, mood_list in self.mood_words.items():
            score = sum(1 for word in mood_list if word in story_lower)
            mood_scores[mood_type] = score
        
        if mood_scores:
            mood = max(mood_scores, key=mood_scores.get)
            if mood_scores[mood] == 0:
                mood = 'neutral'
        
        return {
            'colors': found_colors[:3],
            'places': found_places[:2], 
            'characters': found_characters[:2],
            'mood': mood,
            'summary': story[:100] + "..." if len(story) > 100 else story,
            'word_count': len(story.split())
        }
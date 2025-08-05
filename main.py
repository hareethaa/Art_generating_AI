# main.py - Main Streamlit Application
import streamlit as st
from story_processor import StoryProcessor
from prompt_generator import PromptGenerator
from art_generator import ArtGenerator
from utils import create_filename, save_image, get_example_stories, log_generation

# Page config
st.set_page_config(
    page_title="AI Story to Art Generator",
    page_icon="🎨",
    layout="wide"
)

def main():
    st.title("🎨 AI Story to Art Generator")
    st.markdown("Transform your stories into beautiful AI-generated artwork!")
    
    # Initialize components
    story_processor = StoryProcessor()
    prompt_generator = PromptGenerator()
    art_generator = ArtGenerator()
    
    # Sidebar settings
    st.sidebar.header("⚙️ Settings")
    
    art_styles = ["auto", "digital art", "watercolor painting", "oil painting", "fantasy art"]
    selected_style = st.sidebar.selectbox("Art Style:", art_styles)
    
    image_sizes = ["256x256", "512x512"]
    selected_size = st.sidebar.selectbox("Image Size:", image_sizes)
    width = height = int(selected_size.split('x')[0])
    
    steps = st.sidebar.slider("Quality Steps:", 10, 25, 15)
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📝 Your Story")
        
        examples = get_example_stories()
        selected_example = st.selectbox("Choose example:", list(examples.keys()))
        
        story_input = st.text_area(
            "Write your story:",
            value=examples[selected_example],
            height=200,
            placeholder="Write a descriptive story..."
        )
        
        if story_input:
            st.caption(f"📊 {len(story_input)} characters, {len(story_input.split())} words")
    
    with col2:
        st.header("🖼️ Generated Artwork")
        
        if st.button("🎨 Generate Artwork", type="primary", use_container_width=True):
            if not story_input.strip():
                st.warning("⚠️ Please write a story first!")
                return
            
            try:
                # Step 1: Analyze story
                with st.spinner("📖 Analyzing story..."):
                    story_elements = story_processor.extract_visual_elements(story_input)
                
                # Show analysis
                with st.expander("📊 Story Analysis"):
                    if story_elements['colors']:
                        st.write("🎨 **Colors:**", ", ".join(story_elements['colors']))
                    if story_elements['places']:
                        st.write("🏛️ **Places:**", ", ".join(story_elements['places']))
                    if story_elements['characters']:
                        st.write("👥 **Characters:**", ", ".join(story_elements['characters']))
                    st.write("😊 **Mood:**", story_elements['mood'])
                
                # Step 2: Generate prompt
                with st.spinner("✍️ Creating prompt..."):
                    prompt_data = prompt_generator.generate_art_prompt(story_elements, selected_style)
                
                # Show prompt
                with st.expander("🎯 Art Prompt"):
                    st.code(prompt_data['positive_prompt'])
                
                # Step 3: Generate artwork
                with st.spinner("🤖 Creating artwork... Please wait..."):
                    generated_image = art_generator.generate_image(
                        positive_prompt=prompt_data['positive_prompt'],
                        negative_prompt=prompt_data['negative_prompt'],
                        width=width,
                        height=height,
                        steps=steps
                    )
                
                if generated_image:
                    st.success("🎉 Success!")
                    st.image(generated_image, caption="Your Artwork", use_column_width=True)
                    
                    # Save and download
                    filename = create_filename(story_input.split()[0] if story_input.split() else "artwork")
                    filepath = save_image(generated_image, filename)
                    
                    with open(filepath, "rb") as file:
                        st.download_button(
                            "📥 Download",
                            data=file.read(),
                            file_name=filename,
                            mime="image/png",
                            use_container_width=True
                        )
                    
                    # Log success
                    log_generation(story_input, story_elements, prompt_data, True)
                    st.balloons()
                    
                else:
                    st.error("❌ Generation failed")
                    log_generation(story_input, story_elements, prompt_data, False)
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
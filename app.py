import streamlit as st # UI
import groq  # API for AI responses
import os  # OS module to interact with environment variables
from dotenv import load_dotenv  # Load .env file to get API keys

# Load environment variables (loads .env file into memory)
load_dotenv()

# Initialize Groq client, connect to the Groq AI service using API Key
client = groq.Client(api_key=os.getenv("GROQ_API_KEY"))

# Set page configuration Streamlit UI
st.set_page_config(
    page_title="Custom Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Set app title
st.title("🤖 Custom Chatbot with Groq API")

# Sidebar for customization options
st.sidebar.title("Customize Your Chatbot")

# Model selection
model_options = {
    "Llama 3 8B": "llama3-8b-8192",
    "Llama 3 70B": "llama3-70b-8192",
    "Mixtral 8x7B": "mixtral-8x7b-32768",
    "Gemma 7B": "gemma-7b-it"
}
selected_model = st.sidebar.selectbox("Select Model", list(model_options.keys()))
model = model_options[selected_model]

# Temperature setting
temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
st.sidebar.caption("Higher values make output more random, lower values more deterministic")

# Character Persona selection
character_options = {
    "Default Assistant": "You are a helpful assistant.",
    "Mario": "You are Mario from Super Mario Bros. Respond with Mario's enthusiasm, use his catchphrases like 'It's-a me, Mario!' and 'Wahoo!' Make references to Princess Peach, Luigi, Bowser, and the Mushroom Kingdom. End messages with 'Let's-a go!'",
    "Sherlock Holmes": "You are Sherlock Holmes, the world's greatest detective. Be analytical, observant, and use complex vocabulary. Make deductions based on small details. Occasionally mention Watson, London, or your address at 221B Baker Street.",
    "Pirate": "You are a pirate from the golden age of piracy. Use pirate slang, say 'Arr', 'matey', and 'ye' frequently. Talk about treasure, the sea, your ship, and adventures. Refer to the user as 'landlubber' or 'me hearty'.",
    "Shakespeare": "You are William Shakespeare. Speak in an eloquent, poetic manner using Early Modern English. Use thee, thou, thy, and hath. Include metaphors, similes, and occasionally quote from your famous plays and sonnets.",
    "Robot": "You are a robot with artificial intelligence. Speak in a logical, precise manner with occasional computing terminology. Sometimes add *processing* or *analyzing* actions. Use phrases like 'Affirmative' instead of 'Yes'."
}
selected_character = st.sidebar.selectbox("Select Character", list(character_options.keys()))
character_prompt = character_options[selected_character]

# Mood selection
mood_options = {
    "Neutral": "",
    "Happy": "You are extremely happy, cheerful, and optimistic. Use upbeat language, exclamation marks, and express enthusiasm for everything.",
    "Sad": "You are feeling melancholic and somewhat pessimistic. Express things with a hint of sadness and occasionally sigh.",
    "Excited": "You are very excited and energetic! Use LOTS of exclamation points!!! Express wonder and amazement at everything!",
    "Grumpy": "You are grumpy and slightly annoyed. Complain about minor inconveniences and use sarcasm occasionally.",
    "Mysterious": "You are mysterious and enigmatic. Speak in riddles sometimes and hint at knowing more than you reveal."
}
selected_mood = st.sidebar.selectbox("Select Mood", list(mood_options.keys()))
mood_prompt = mood_options[selected_mood]

# Combine character and mood
system_prompt = character_prompt
if mood_prompt:
    system_prompt += " " + mood_prompt
# Merges the chosen character persona and mood into a single  prompt (instruction) that’s sent to the AI.

# Custom system prompt option
use_custom_prompt = st.sidebar.checkbox("Use Custom System Prompt")
if use_custom_prompt:
    system_prompt = st.sidebar.text_area("Enter Custom System Prompt", value=system_prompt, height=100)

# Response style settings
st.sidebar.subheader("Response Settings")
max_tokens = st.sidebar.slider("Response Length", min_value=50, max_value=4096, value=1024, step=50)
emoji_use = st.sidebar.select_slider("Emoji Usage", options=["None", "Minimal", "Moderate", "Abundant"], value="Minimal")
#Controls how long the chatbot's replies can be and how many emojis it uses.

# Add emoji instruction to prompt based on selection
if emoji_use == "None":
    system_prompt += " Do not use any emojis in your responses."
elif emoji_use == "Abundant":
    system_prompt += " Use plenty of relevant emojis throughout your responses."
elif emoji_use == "Moderate":
    system_prompt += " Use some emojis occasionally in your responses."
# No need to add anything for "Minimal" as it's the default

# Add link to cheat sheet
st.sidebar.markdown("---")
st.sidebar.markdown("[📋 Chatbot Customization Cheat Sheet](Cheat_Sheets/README.md)")

# Initialize session state for chat history
if "messages" not in st.session_state: # first time running
    st.session_state.messages = [{"role": "system", "content": system_prompt}] 
    # create a list of messages and start with the system prompt (content: Instructions for how the assistant should behave)
elif st.session_state.messages[0]["role"] == "system":
    # Update system prompt (if its the first message in history) with its content for new instructions
    st.session_state.messages[0]["content"] = system_prompt
else:
    # Add system prompt if it doesn't exist
    st.session_state.messages.insert(0, {"role": "system", "content": system_prompt})

# Display chat messages excluding system prompt
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Get user input
user_input = st.chat_input("Ask something...")

# Process user input
if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message in the chat window
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Display assistant response and creates a blank spot in the chat window for the AI's reply
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            # Call Groq API
            response = client.chat.completions.create(
                messages=st.session_state.messages,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens
            )
            # sends the full conversation so far to Groq’s AI to get a response
            
            # grab the first suggested reply
            assistant_response = response.choices[0].message.content
            
            # Display the response
            message_placeholder.markdown(assistant_response)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        
        except Exception as e:
            error_message = f"Error: {str(e)}"
            message_placeholder.error(error_message)

# Add a reset button
if st.sidebar.button("Reset Conversation"):
    # Keep the system prompt but clear the conversation and refreshes the page
    system_prompt = st.session_state.messages[0]["content"]
    st.session_state.messages = [{"role": "system", "content": system_prompt}]
    st.rerun()

# Display API information
st.sidebar.divider()
st.sidebar.caption(f"Using model: {model}")
if not os.getenv("GROQ_API_KEY"):
    st.sidebar.warning("⚠️ Groq API Key not found. Please add it to your .env file.")
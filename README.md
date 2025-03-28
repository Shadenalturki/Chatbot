# Custom Chatbot with Groq API 🤖 

A fully customizable chatbot built with **Streamlit** and powered by the **Groq API**. This chatbot allows users to choose from multiple AI models, characters, moods, and response settings — all from a clean user interface.

## Website link
👉 **[Click here to try the chatbot!](https://shadenalturki-chatbot.streamlit.app/)**  

## Features

- Choose between AI models like **LLaMA 3**, **Mixtral**, and **Gemma**
- Set chatbot mood: Happy, Sad, Mysterious, Grumpy, etc.
- Select a character persona: Mario, Sherlock Holmes, Pirate, Shakespeare, Robot, etc.
- Customize temperature, response length, and emoji usage
- Chat memory saved using Streamlit's session state
- Secret API key securely managed via Streamlit Cloud

## Technologies Used

- [Streamlit](https://streamlit.io) – Web app UI
- [Groq API](https://groq.com) – Fast AI response engine
- `python-dotenv` – Load `.env` variables locally
- Python 3.8+

## Setup & Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/Shadenalturki/Chatbot.git
cd Chatbot
bash
```

### 2. Create a .env file
Create a file called .env in the root folder and add your Groq API key:
```bash
GROQ_API_KEY="your_actual_api_key_here"
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Run the App
```bash
streamlit run app.py
```
The app will open in your browser at http://localhost:8501


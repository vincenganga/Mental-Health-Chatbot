# Mental-Health-Chatbot

A compassionate AI-powered Mental Health Chatbot built using [Streamlit](https://streamlit.io/) and [Google's gemini-2.0-flash model](https://ai.google.dev/gemini-api/docs/models) that provides empathetic conversations, mood tracking and personalized coping strategies. This application aims to offer accessible mental health support while encouraging users to seek professional help when needed.

## Features

- **Chat Interface**: Interact with the chatbot in a user-friendly chat interface with real-time AI responses.
- **Sentiment Analysis**: Advanced sentiment analysis using TextBlob to categorize user emotions into seven distinct emotional states.
- **Mood Tracking**: Real-time visual tracking of user's emotional journey throughout the conversation session.
- **Personalized Coping Strategies**: AI-generated coping mechanisms tailored to the user's current emotional state.
- **Crisis Detection**: Automatic detection of crisis keywords with immediate emergency resource suggestions.
- **Session Summaries**: Comprehensive conversation analysis with mood distribution charts and session insights.
- **Emergency Resources**: Provide quick access to mental health hotlines and professional support services.
- **Conversation Memory**: Maintains context across chat exchanges for more logical and empathetic interactions.
- **Privacy-Focused Design**: No data persistence between sessions to protect user confidentiality

## Technology Stack

- **Frontend**: [Streamlit](https://streamlit.io/) - For the web interface
- **AI Model**: [Google's gemini-2.0-flash model](https://ai.google.dev/gemini-api/docs/models) (via OpenAI-compatible API)- For intelligent conversations
- **Sentiment Analysis**: TextBlob - For mood detection and analysis
- **Data Visualization**: Plotly - For interactive mood tracking charts
- **Data Processing**: Pandas - For session analytics
- **Language**: Python 3.7+

## Prerequisites
- Python 3.7 or higher
- Google AI API key (Gemini access)
- Internet connection for API calls

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/vincenganga/Mental-Health-Chatbot.git
    cd Mental-Health-Chatbot
    ```

2. **Create a virtual environment and activate it:**
    ```bash
    python -m venv env
    # On Windows
    .\env\Scripts\activate
    # On macOS/Linux
    source env/bin/activate
    ```

3. **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up your Gemini API key:**
    - Obtain your Gemini API key from [Google AI Studio](https://ai.google.dev/gemini-api/docs/api-key).
    - Create `.streamlit/secrets.toml` in your root folder.
    - Add your API key in the `secrets.toml` file:
    ```toml
    GOOGLE_AI_API_KEY = "your_gemini_api_key"
    ```
    - Replace `"your_gemini_api_key"` with your actual API key.
    - The application uses the OpenAI-compatible endpoint for Gemini

## Configuration

### Customization Options
- **System Prompt**: Modify `MENTAL_HEALTH_SYSTEM_PROMPT` in `app.py` to adjust the chatbot's personality
- **Crisis Keywords**: Update the `crisis_keywords` list in the `detect_crisis_keywords()` function
- **Coping Strategies**: Customize strategies in the `provide_coping_strategy()` function
- **Crisis Resources**: Update contact information in the sidebar for your region

## Usage

1. **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```

2. **Open the provided URL** (typically `http://localhost:8501`) in your web browser.

3. **Start interacting with the chatbot:**
    - Type your message in the input box and press "Send".
    - The chatbot will respond with empathetic support, analyze your sentiment and track your mood.
    - View your real-time mood visualization in the sidebar
    - Receive personalized coping strategies based on your emotional state
    - Access crisis resources immediately if needed

## Project Structure

```
Mental-Health-Chatbot/
├── app.py                    # Main application file with Streamlit interface
├── requirements.txt          # Python package dependencies
├── .streamlit/
│   └── secrets.toml         # API key configuration (create this file)
├── .gitignore               # Git ignore file for sensitive data
└── README.md                # Project documentation

```

- **`app.py`**: Contains the main Streamlit application logic, AI integration, sentiment analysis, and user interface
- **`requirements.txt`**: Lists all required Python packages for the project
- **`.streamlit/secrets.toml`**: Securely stores your Google AI API key (excluded from version control)
- **`.gitignore`**: Prevents sensitive files like API keys from being tracked in Git

## Privacy and Security

- **No Data Persistence**: Conversations are not stored between sessions
- **Local Processing**: Sentiment analysis happens locally using TextBlob
- **API Security**: Only necessary data is sent to the AI service
- **Session Isolation**: Each browser session is independent

## Emergency Resources

if you need immediate help, please contact the following resources:

### **Immediate Help:**
- **Emergency:** 999
- **Crisis Text Line:** Text 1190
- **Suicide Prevention:** Contact 1199

### **Professional Support:**
- [Mental Health Hotlines Kenya](https://www.whatseatingmymind.com/emergency-hotline-numbers)
- [Suicide Prevention Kenya](https://www.enableme.ke/en/article/suicide-emergency-numbers-and-free-counselling-centers-in-kenya-3770)

*Note: These resources are specific to Kenya. Please update with local emergency numbers for your region.*

## Acknowledgements

- [Streamlit](https://streamlit.io/)
- [Google AI Studio](https://ai.google.dev/gemini-api/docs)

---

**Remember**: This tool is designed to provide support and encouragement, but it cannot replace professional mental health care. If you or someone you know is in crisis, please contact emergency services or a mental health professional immediately.
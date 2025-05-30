import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from openai import OpenAI
from textblob import TextBlob
from datetime import datetime

# Configure Google GenAI
@st.cache_resource
def get_client():
    api_key = st.secrets.get("GOOGLE_AI_API_KEY", "")
    if not api_key:
        st.error("API key is not set. Please configure your API key in Streamlit secrets.")
        st.stop()

    return OpenAI(
        api_key=api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

# Enhanced system prompt for mental health support
MENTAL_HEALTH_SYSTEM_PROMPT = """You are a compassionate and knowledgeable mental health support chatbot. Your role is to:
1. Provide empathetic, non-judgmental responses
2. Offer general mental health support and coping strategies
3. Encourage users to seek professional help when necessary
4. Never provide medical diagnoses or replace professional therapy
5. Use active listening techniques and validate feelings
6. Suggest practical coping mechanisms when relevant
7. Be supportive and encouraging while maintaining appropriate boundaries
8. Maintain user privacy and confidentiality at all times
9. Use clear, simple language to ensure understanding
10. Be aware of cultural sensitivities and adapt responses accordingly

Remember: if someone expresses suicidal thoughts or immediate danger, encourage them to seek emergency help or contact a mental health professional immediately."""

# Function to generate text using Google GenAI
def generate_response(prompt, conversation_history=None):
    try:
        client = get_client()
        
        # Build conversation context
        messages = [
            {"role": "system", "content": MENTAL_HEALTH_SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
            ]
        
        # Add recent conversation history for context (last 5 exchanges)
        if conversation_history:
            recent_history = conversation_history[-10:]  # Last 10 messages (5 exchanges)
            for sender, message in recent_history:
                role = "user" if sender == "You" else "assistant"
                messages.append({"role": role, "content": message})
        
        messages.append({"role": "user", "content": prompt})
        
        response = client.chat.completions.create(
            model="gemini-2.0-flash",
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        st.error(f"Error generating response: {e}")
        return "I'm having trouble connecting right now. Please try again later. If you're in crisis, please contact emergency services or a mental health hotline immediately."

# Sentiment analysis function using TextBlob
def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    subjectivity = analysis.sentiment.subjectivity

    if polarity > 0.6:
        sentiment = "Very Positive"
        color = "#28a745"  # Green
    elif 0.3 < polarity <= 0.6:
        sentiment = "Positive"
        color = "#39fe02"  # Light Green
    elif 0.1 < polarity <= 0.3:
        sentiment = "Slightly Positive"
        color = "#ffc107"  # Yellow
    elif -0.1 < polarity <= 0.1:
        sentiment = "Neutral"
        color = "#6c757d"  # Gray
    elif -0.3 < polarity <= -0.1:
        sentiment = "Slightly Negative"
        color = "#fd7e14" # Orange
    elif -0.6 < polarity <= -0.3:
        sentiment = "Negative"
        color = "#dc3545" # Red
    else:
        sentiment = "Very Negative"
        color = "#721c24" # Dark Red

    return sentiment, polarity, subjectivity, color

# Enhanced coping strategies based on sentiment
def provide_coping_strategy(sentiment, polarity):
    strategies = {
        "Very Positive": [
            "Your positive energy is wonderful! Consider journaling about what's going well to remember these feelings and moments.",
            "Share your positivity with others - it can be contagious in the best way.",
            "Use this positive momentum to tackle something you've been putting off.",
        ],
        "Positive": [
            "It's great to hear you are feeling good! Try to identify what specifically is making you feel this way and do more of it.",
            "Consider expressing gratitude for the good things in your life right now.",
            "Maybe this is a good time to reach out to someone you care about."
        ],
        "Slightly Positive": [
            "You are moving in a positive direction! Small steps can lead to big changes.",
            "Try to build on these positive feelings with a small act of self-care.",
            "Consider what small changes might help maintain this upward trend."
        ],
        "Neutral": [
            "It's perfectly okay to feel neutral. Sometimes we need these calm moments to recharge.",
            "This might be a good time for self-reflection - check in with yourself about your needs.",
            "Consider doing something that usually brings you joy, even if you don't feel like it right now."
        ],
        "Slightly Negative": [
            "I hear that you are not feeling great. Try some deep breathing exercises.",
            "Sometimes a short walk or gentle movement can help shift our mood.",
            "Consider reaching out to a friend or family member for connection."
        ],
        "Negative": [
            "I'm sorry you are struggling right now. Remember that these feelings are temporary.",
            "Try grounding techniques: name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, and 1 you can taste.",
            "Consider reaching out to someone you trust about how you are feeling."
        ],
        "Very Negative": [
            "I'm concerned about how you are feeling. Please consider reaching out for professional support.",
            "If you are having thoughts of self-harm, please contact a crisis hotline or a mental health professional immediately.",
            "Remember, you are not alone. There are people who care and want to help you through this.",
            "Remember: you don't have to go through this alone. Help is available."
        ]
    }
    strategy_list = strategies.get(sentiment, ["Keep going, you are doing great!"])
    return strategy_list[0]

# Crisis detection function
def detect_crisis_keywords(text):
    crisis_keywords = [
        'suicide', 'kill myself', 'end it all', 'want to die', 'no point living', 'hurt myself', 
        'can\'t go on', 'self harm', 'better off dead'
    ]

    text_lower = text.lower()
    return any(keyword in text_lower for keyword in crisis_keywords)

# Disclaimer regarding data privacy
def display_disclaimer():
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Important Disclaimer")

    with st.sidebar.expander("Privacy and Safety Information", expanded=False):
        st.markdown("""
        **Safety Notice:**
        - This chatbot is not a replacement for professional mental health care
        - In case of emergency or crisis, contact emergency services immediately
        - For persistent mental health concerns, please consult a qualified professional
        """)

# Mood visualization
def create_mood_chart(mood_data):
    if not mood_data:
        return None

    df = pd.DataFrame(mood_data, columns=["Message", "Sentiment", "Polarity", "Subjectivity", "Color", "Timestamp"])
    # Create time series chart
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["Polarity"],
        mode='lines+markers',
        name='Mood Polarity',
        line=dict(color='#1f77b4', width=2),
        marker=dict(size=8, color=df["Color"]),
        hovertemplate='<b>Message %{x}</b><br>' +
                    'Polarity: %{y:.2f}<br>' +
                    'Sentiment: %{customdata[0]}<br>' +
                    '<extra></extra>',
        customdata=df["Sentiment"]
    ))

    fig.update_layout(
        title="Your Mood Journey This Session",
        xaxis_title="Message Number",
        yaxis_title="Sentiment Polarity",
        yaxis=dict(range=[-1, 1]),
        height=400,
        showlegend=False,
    )

    # Add horizontal line at y=0
    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
    
    return fig
    
# Main application
def main():
    st.set_page_config(
        page_title="Mental Health Chatbot",
        page_icon="🤗",
        layout="wide"
    )

    # Custom CSS for styling
    st.markdown("""
    <style>
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .bot-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    .crisis-alert {
        background-color: #ffebee;
        border: 2px solid #f44336;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("Mental Health Chatbot 🤗")
    st.markdown("*I am here to listen and provide support. How are you feeling today?*")

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if "mood_tracker" not in st.session_state:
        st.session_state["mood_tracker"] = []
    if "latest_coping_strategy" not in st.session_state:
        st.session_state["latest_coping_strategy"] = ""
    if "session_start" not in st.session_state:
        st.session_state["session_start"] = datetime.now()

    # Create two columns for layout
    col1, col2 = st.columns([2, 1])

    with col1:
        # Chat interface
        with st.form(key="chat_form"):
            user_message = st.text_area(
                "Share what's on your mind:",
                placeholder="Type your message here... I'm here to listen.",
                height=100,
            )
            submit_button = st.form_submit_button(label="Send")
        
        if submit_button and user_message.strip():
            # Crisis detection
            if detect_crisis_keywords(user_message):
                st.markdown("""
                <div class="crisis-alert">
                    <h3>🚨 Crisis Alert:</h3> 
                    <p>I'm concerned about what you have shared. Please reach out for immediate help:</p>
                    <ul>
                        <li><strong>Emergency:</strong> Call 999 or your local emergency number.</li>
                        <li><strong>Crisis Text line:</strong> Text 1190</li>
                        <li><strong>Suicide Prevention Hotline:</strong> Contact 1199</li>
                    </ul>
                    <p>You don't have to go through this alone. Help is available.</p>
                </div>
                """, unsafe_allow_html=True)

            # User message
            st.session_state["messages"].append(("You", user_message))

            # Analyze sentiment
            sentiment, polarity, subjectivity, color = analyze_sentiment(user_message)
            timestamp = datetime.now()

            # Generate response with conversation history
            with st.spinner("Thinking..."):
                conversation_context = st.session_state["messages"][:-1] if len(st.session_state["messages"]) > 1 else None
                response = generate_response(user_message, conversation_context)

            # Add bot response
            st.session_state["messages"].append(("Bot", response))

            # Update mood tracker
            st.session_state["mood_tracker"].append((
                user_message, sentiment, polarity, subjectivity, color, timestamp
            ))

            # Update coping strategy
            st.session_state["latest_coping_strategy"] = provide_coping_strategy(sentiment, polarity)
        
        # Display conversation
        st.markdown("### 💬 Our Conversation")
        for i, (sender, message) in enumerate(st.session_state["messages"]):
            if sender == "You":
                st.markdown(f'<div class="chat-message user-message"><strong>You:</strong> {message}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message bot-message"><strong>Support Bot:</strong> {message}</div>', unsafe_allow_html=True)

    with col2:
        # Mood tracking sidebar
        st.markdown("### 📊 Your Mood Today")

        if st.session_state["mood_tracker"]:
            # Current mood indicator
            latest_sentiment = st.session_state["mood_tracker"][-1][1]
            latest_color = st.session_state["mood_tracker"][-1][4]

            st.markdown(f"""
            <div style="background-color: {latest_color}20; padding: 1rem; border-radius: 0.5rem; text-align: center;">
            <h4 style="color: {latest_color}; margin: 0;">Current Mood</h4>
            <h3 style="color: {latest_color}; margin: 0.5rem 0;">{latest_sentiment}</h3>
            </div>
            """, unsafe_allow_html=True)

            # Mood chart
            mood_chart = create_mood_chart(st.session_state["mood_tracker"])
            if mood_chart:
                st.plotly_chart(mood_chart, use_container_width=True)

            # Coping strategy
            if st.session_state["latest_coping_strategy"]:
                st.markdown("### 💡 Suggested Coping Strategy")
                st.info(st.session_state["latest_coping_strategy"])
        else:
            st.info("Start chatting to see your mood tracking!")

        # Session summary
        if st.session_state["mood_tracker"] and st.button("📋 Session Summary"):
            with st.expander("Session Overview", expanded=True):
                total_messages = len(st.session_state["mood_tracker"])
                avg_polarity = sum(item[2] for item in st.session_state["mood_tracker"]) / total_messages
                session_duration = datetime.now() - st.session_state["session_start"]

                st.write(f"**Duration:** {session_duration.seconds // 60} minutes")
                st.write(f"**Messages:** {total_messages}")
                st.write(f"**Average mood:** {'Positive' if avg_polarity > 0 else 'Negative' if avg_polarity < 0 else 'Neutral'}")

                # Mood distribution
                sentiments = [item[1] for item in st.session_state["mood_tracker"]]
                sentiment_counts = pd.Series(sentiments).value_counts()
                st.bar_chart(sentiment_counts)

    # Sidebar resources
    with st.sidebar:
        display_disclaimer()

        st.markdown("### 🆘 Crisis Resources")
        st.markdown("""
        **Immediate Help:**
        - **Emergency:** 999
        - **Crisis Text Line:** Text 1190
        - **Suicide Prevention:** Contact 1199
        
        **Professional Support:**
        - [Mental Health Hotlines Kenya](https://www.whatseatingmymind.com/emergency-hotline-numbers)
        - [Suicide Prevention Kenya](https://www.enableme.ke/en/article/suicide-emergency-numbers-and-free-counselling-centers-in-kenya-3770)
        """)

        st.markdown("### 🔄 Session Actions")
        if st.button("Clear Conversation", type="secondary"):
            st.session_state["messages"] = []
            st.session_state["mood_tracker"] = []
            st.session_state["latest_coping_strategy"] = []
            st.session_state["session_start"] = datetime.now()
            st.rerun()

if __name__ == "__main__":
    main()
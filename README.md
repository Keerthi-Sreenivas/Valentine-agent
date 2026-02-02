# Valentine.exe ❤️

A romantic AI-powered Valentine's Day surprise app! It interviews your partner about their "perfect valentine," drops cheesy hints about you, then reveals it was about you all along and pops the question.

## Features

- 🃏 **Card Flip Game** - AI/ML-themed pickup lines to start the fun
- 💬 **AI Interview** - 3 questions with playful hints about you
- 🎉 **Big Reveal** - Dramatic "Will you be my Valentine?" moment
- 📅 **Calendar Invite** - Auto-generates a Google Calendar date invite
- 🎈 **Animations** - Heart bursts and red balloons

## Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set up your API key
Create a `.env` file:
```
AWS_BEDROCK_API_KEY=your_bedrock_api_key
```

### 3. Customize for your valentine
Edit `app.py` and update:
```python
YOUR_TRAITS = {
    "personality": "your personality traits",
    "hobbies": "your hobbies",
    "shared_passions": "things you do together",
    "partnership": "what you're building together",
    "special_quality": "what makes you special to them",
}
YOUR_NAME = "YourName"
```

### 4. Run locally
```bash
streamlit run app.py
```

## Deploy to Streamlit Cloud (Free)

1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo and select `app.py`
4. Add `AWS_BEDROCK_API_KEY` in Secrets
5. Share the link with your valentine! 💕

## Tech Stack

- **Amazon Bedrock** - Claude 3.5 Sonnet
- **Streamlit** - Web UI

---
// built with code and love 💕

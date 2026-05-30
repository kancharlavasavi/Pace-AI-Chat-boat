# Pace-AI-Chat-boat
This project is a Streamlit‑based AI Chatbot for PACE College FAQs. It combines multilingual sentence embeddings with a TF‑IDF fallback to provide accurate, context‑aware answers to student and parent queries about admissions, courses, fees, exams, placements, and campus facilities.

## 📌 Objective
Students and parents often face difficulties in obtaining accurate and timely information about college admissions, courses, fees, exams, placements, and campus facilities.  
This project automates the process of answering FAQs using **AI + NLP** to provide instant, reliable, and multilingual responses through a modern chat interface.



## ✨ Features
- 📊 FAQ dataset covering admissions, academics, fees, exams, placements, facilities, student life, faculty, and research.
- 🧠 Hybrid NLP backend (SentenceTransformers multilingual embeddings + TF‑IDF fallback).
- 🌐 Multilingual support (English, Telugu, Hindi).
- 🎤 Voice input and output (SpeechRecognition + gTTS).
- 🎨 Modern glassmorphism UI with Streamlit.
- 🔍 Live updates scraped from [pace.ac.in](https://pace.ac.in).
- 💬 Chat history with styled bubbles for user and bot messages.



## 🛠️ Tech Stack
- **Frontend**: Streamlit (Python)
- **Backend**: SentenceTransformers, scikit‑learn
- **Voice**: SpeechRecognition, gTTS
- **Web Scraping**: BeautifulSoup
- **Deployment**: Streamlit Cloud / Hugging Face Spaces



## 📂 Repository Structure

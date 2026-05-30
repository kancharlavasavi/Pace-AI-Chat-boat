import pandas as pd
import streamlit as st
import base64
import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer, util
from gtts import gTTS
import os
import speech_recognition as sr

# ============================
# 📊 FAQ Dataset (seeded)
# ============================
faq_data = {
  "question": [
    "What are the admission requirements?",
    "What is the fee structure?",
    "What courses are offered?",
    "What is the exam schedule?",
    "What facilities are available on campus?",
    "Tell me about PACE College",
    "Say about PACE",
    "What are the placements in 2026?",
    "Explain the examination fee",
    "What is the highest package?",
    "Is lateral entry available?",
    "What is the eligibility for MBA?",
    "What is the eligibility for M.Tech?",
    "Are scholarships available?",
    "Is hostel facility available?",
    "Where is PACE College located?",
    "Is PACE affiliated to JNTU?",
    "Is PACE AICTE approved?",
    "What is the contact number?",
    "When was PACE College established?",
    "What branches are offered in B.Tech?",
    "Are electives available?",
    "Does PACE offer postgraduate programs?",
    "Is the curriculum affiliated to JNTU?",
    "Are academic calendars published?",
    "What is the annual tuition fee for B.Tech?",
    "What is the hostel fee?",
    "What is the examination fee?",
    "Are scholarships available for merit students?",
    "Can fees be paid online?",
    "When are semester exams conducted?",
    "Where can I find exam timetables?",
    "Is revaluation available?",
    "Are supplementary exams conducted?",
    "Where can I check results?",
    "What is the average package?",
    "Which companies visit for recruitment?",
    "Are internships provided?",
    "Is soft skills training provided?",
    "Does PACE have a library?",
    "Is Wi-Fi available?",
    "Are hostels available?",
    "Are labs available?",
    "Is there a sports complex?",
    "Are medical facilities available?",
    "Are there student clubs?",
    "Does PACE organize cultural fests?",
    "Is NSS available?",
    "Is NCC available?",
    "Is there a student council?",
    "What are faculty qualifications?",
    "Is mentoring available?",
    "Is counseling available?",
    "Is there a grievance cell?",
    "Is there an anti-ragging committee?",
    "Is there an incubation center?",
    "Are patents filed by students?",
    "Are publications encouraged?",
    "Are hackathons organized?",
    "Is PACE located in Andhra Pradesh?",
    "Is PACE affiliated to JNTU Kakinada?",
    "Is PACE AICTE approved?",
    "What is the official contact number?",
    "What is the history of PACE College?",
    "hlo",
  ],
  "answer": [
    "Students must qualify in EAMCET and complete 10+2 with Mathematics, Physics, and Chemistry.",
    "The annual tuition fee is INR 50,000. Hostel fees range from ₹30,000 to ₹40,000 per year. Exam fees are separate.",
    "PACE offers B.Tech in CSE, ECE, EEE, Mechanical, Civil, IT, AI & ML, and IoT & Cyber Security. PG programs include M.Tech, MBA, and MCA.",
    "Exams are conducted at the end of each semester. Timetables and notifications are published on exams.pace.in.",
    "Campus facilities include library, hostels, sports complex, labs, Wi-Fi, cafeteria, seminar halls, and medical center.",
    "PACE College is a reputed institution offering UG and PG programs in engineering, management, and computer applications, with modern facilities and strong student support.",
    "PACE College provides quality education in engineering, management, and computer applications, with strong infrastructure and student support services.",
    "PACE College has strong placement records with leading companies visiting the campus. In 2026, students were placed in IT, core engineering, and management roles with competitive packages.",
    "Examination fee details are published in official notifications. For B.Tech regular exams it is around ₹2000, with supplementary fees ranging from ₹600 to ₹2000 depending on subjects.",
    "The highest package offered at PACE College in recent years has been around INR 12 LPA.",
    "Yes, diploma holders can join directly into the 2nd year of B.Tech through ECET.",
    "Admission to MBA requires a valid ICET score and a bachelor’s degree in any discipline.",
    "Candidates must qualify in GATE or PGECET and hold a relevant B.Tech degree.",
    "Yes, merit-based and government scholarships are available for eligible students.",
    "Yes, hostel accommodation is available for boys and girls with annual fees between ₹30,000–₹40,000.",
    "PACE College is located in Valluru village near Ongole, Andhra Pradesh.",
    "Yes, it is affiliated to JNTU Kakinada.",
    "Yes, the college is approved by AICTE.",
    "You can contact the college at +91-9581456310.",
    "PACE College was established in 2007.",
    "PACE offers CSE, ECE, EEE, Mechanical, Civil, IT, AI & ML, and IoT & Cyber Security.",
    "Yes, electives in AI, Data Science, IoT, and Cyber Security are offered.",
    "Yes, M.Tech, MBA, and MCA programs are available.",
    "Yes, PACE follows JNTU Kakinada curriculum and regulations.",
    "Yes, academic calendars are published every year on pace.ac.in.",
    "The tuition fee is approximately ₹50,000 per year.",
    "Hostel fees range from ₹30,000 to ₹40,000 per year depending on room type.",
    "Regular exam fee is around ₹2000, supplementary fees range from ₹600 to ₹2000.",
    "Yes, merit-based and government scholarships are available.",
    "Yes, fees can be paid online through the college portal.",
    "Exams are conducted at the end of each semester.",
    "Exam timetables are published on exams.pace.in.",
    "Yes, students can apply for revaluation by paying the prescribed fee.",
    "Yes, supplementary exams are conducted for failed subjects.",
    "Results are published on exams.pace.in.",
    "The average package is around ₹4.5 LPA.",
    "Infosys, TCS, Wipro, Deloitte, NVIDIA, CtrlS, MEIL, Mold-Tek, Powermech Projects.",
    "Yes, internships are facilitated for students in final year.",
    "Yes, soft skills and aptitude training are part of placement preparation.",
    "Yes, the library has books, journals, and e-resources.",
    "Yes, the entire campus is Wi-Fi enabled.",
    "Yes, separate hostels are available for boys and girls.",
    "Yes, each department has dedicated labs with modern equipment.",
    "Yes, the campus has a sports complex for indoor and outdoor games.",
    "Yes, a medical center with first aid is available on campus.",
    "Yes, clubs for coding, robotics, cultural activities, and entrepreneurship are active.",
    "Yes, annual cultural and technical fests such as Festino are organized.",
    "Yes, NSS activities are conducted regularly.",
    "Yes, NCC is available for interested students.",
    "Yes, a student council represents student interests.",
    "Faculty members hold PhDs and postgraduate degrees in their fields.",
    "Yes, faculty mentors are assigned to guide students.",
    "Yes, counseling services are available for students.",
    "Yes, a grievance redressal cell is available.",
    "Yes, an anti-ragging committee ensures student safety.",
    "Yes, PACE has an incubation center to support startups.",
    "Yes, students and faculty have filed patents in recent years.",
    "Yes, students are encouraged to publish research papers.",
    "Yes, hackathons and coding competitions are organized.",
    "Yes, PACE is located in Andhra Pradesh.",
    "Yes, it is affiliated to JNTU Kakinada.",
    "Yes, the college is approved by AICTE.",
    "You can contact the college at +91-9581456310.",
    "PACE College was established in 2007.",
    "hii! how can I assist you today"
  ]
}


faq = pd.DataFrame(faq_data)

# ============================
# 🔍 Scraping live updates
# ============================
def scrape_updates():
    try:
        url = "https://pace.ac.in"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        updates = soup.find_all("marquee")
        return [u.get_text(strip=True) for u in updates]
    except Exception:
        return ["Unable to fetch live updates at the moment."]

# ============================
# 🧠 Backend — Multilingual Embeddings
# ============================
# Load multilingual model
model = SentenceTransformer('distiluse-base-multilingual-cased-v2')

# Encode FAQ questions once
faq_embeddings = model.encode(faq['question'].tolist(), convert_to_tensor=True)

def chatbot_response(user_query):
    query_embedding = model.encode(user_query, convert_to_tensor=True)
    scores = util.cos_sim(query_embedding, faq_embeddings)[0]
    best_match = int(scores.argmax())
    if scores[best_match] < 0.5:
        return "I can share details about admissions, fees, courses, exams, placements, facilities, or an overview of PACE College. Please ask about one of these."
    return faq['answer'][best_match]

# ============================
# 🎤 Voice Input/Output
# ============================
def voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening... Speak now")
        audio = r.listen(source)
    try:
        return r.recognize_google(audio)
    except:
        return "Sorry, I could not understand your voice."

def speak(text):
    tts = gTTS(text=text, lang="en")
    tts.save("response.mp3")
    os.system("start response.mp3")  # Windows

# ============================
# 🎨 Frontend — Glassmorphism UI
# ============================
def get_base64_of_image(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

image_base64 = get_base64_of_image("pace.jpg")

st.set_page_config(page_title="PACE College Chatbot", page_icon="🎓", layout="wide")

page_bg = f"""
<style>
.main .block-container {{
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(12px);
    border-radius: 16px;
    padding: 20px;
    margin-top: 40px;
}}
.chat-bubble-user {{
    background: linear-gradient(135deg, #43cea2, #185a9d);
    color: white;
    padding: 12px;
    border-radius: 16px;
    margin: 8px 0;
    max-width: 70%;
    font-weight: 500;
    box-shadow: 0 4px 10px rgba(0,0,0,0.2);
}}
.chat-bubble-bot {{
    background: linear-gradient(135deg, #2196F3, #6dd5ed);
    color: white;
    padding: 12px;
    border-radius: 16px;
    margin: 8px 0;
    max-width: 70%;
    font-weight: 500;
    box-shadow: 0 4px 10px rgba(0,0,0,0.2);
}}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

st.title("🎓 PACE College AI Chatbot")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar options
assistant_mode = st.sidebar.checkbox("🤖 Talk to PACE Assistant")
voice_mode = st.sidebar.checkbox("🎤 Enable Voice Output")
voice_input_mode = st.sidebar.checkbox("🎙️ Use Voice Input")

updates = scrape_updates()
st.sidebar.write("📢 Latest Updates:")
for u in updates:
    st.sidebar.write(f"- {u}")

# Assistant greeting
if assistant_mode and not st.session_state.get("assistant_greeted", False):
    st.session_state.chat_history.append(("Bot", "Hi, I’m your PACE Assistant! 🎓 Ask me anything about admissions, courses, fees, or campus life."))
    st.session_state.assistant_greeted = True

# Voice-enabled text box

if voice_input_mode:
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("🎤 Speak"):
            user_input = voice_input()
        else:
            user_input = None
    with col2:
        typed_input = st.chat_input("Or type your question here...")
        if typed_input:
            user_input = typed_input
else:
    user_input = st.chat_input("Type your question here...")

# Response
if user_input:
    if assistant_mode:
        if "placement" in user_input.lower():
            response = "PACE College has strong placement records. Do you want details about highest package, average salary, or recruiters?"
        else:
            response = chatbot_response(user_input)
    else:
        response = chatbot_response(user_input)

    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("Bot", response))

    if voice_mode:
        speak(response)

# Display chat history
for speaker, message in st.session_state.chat_history:
    if speaker == "You":
        st.markdown(f"<div class='chat-bubble-user'><b>{speaker}:</b> {message}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble-bot'><b>{speaker}:</b> {message}</div>", unsafe_allow_html=True)

import pandas as pd
from sentence_transformers import SentenceTransformer, util
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# FAQ dataset
faq = pd.DataFrame(faq_data)

# ============================
# 🧠 Embedding Model (Multilingual)
# ============================
model = SentenceTransformer('distiluse-base-multilingual-cased-v2')
faq_embeddings = model.encode(faq['question'].tolist(), convert_to_tensor=True)

# ============================
# 🧠 TF-IDF Model (Keyword fallback)
# ============================
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(faq['question'].tolist())

# ============================
# 🔍 Hybrid Response Function
# ============================
def chatbot_response(user_query):
    # --- Embedding similarity ---
    query_embedding = model.encode(user_query, convert_to_tensor=True)
    scores = util.cos_sim(query_embedding, faq_embeddings)[0]
    best_match_embed = int(scores.argmax())
    embed_score = float(scores[best_match_embed])

    # --- TF-IDF similarity ---
    query_vec = vectorizer.transform([user_query])
    tfidf_scores = cosine_similarity(query_vec, X).flatten()
    best_match_tfidf = int(tfidf_scores.argmax())
    tfidf_score = float(tfidf_scores[best_match_tfidf])

    # --- Decision logic ---
    if embed_score >= 0.5:
        return faq['answer'][best_match_embed]
    elif tfidf_score >= 0.2:
        return faq['answer'][best_match_tfidf]
    else:
        return "I can share details about admissions, fees, courses, exams, placements, facilities, or an overview of PACE College. Please ask about one of these."

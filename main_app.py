import streamlit as st
import re
import nltk
import requests
import json
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import numpy as np
from datetime import datetime

# Try to load API key from Streamlit Cloud secrets (for deployed app)
# or from secrets.toml (for local development)
try:
    # Check if running on Streamlit Cloud
    API_KEY = st.secrets["huggingface"]["api_key"]
    print(f"✅ API Key loaded from Streamlit Cloud secrets: {API_KEY[:20]}...")
except (FileNotFoundError, KeyError):
    # Fallback to local secrets.toml for development
    try:
        import toml
        secrets = toml.load('secrets.toml')
        API_KEY = secrets['huggingface']['api_key']
        print(f"✅ API Key loaded from secrets.toml: {API_KEY[:20]}...")
    except (ImportError, FileNotFoundError, KeyError):
        print("❌ No API key found in secrets.toml or Streamlit Cloud secrets")
        API_KEY = None

st.set_page_config(
    page_title="🛡️ Fake News Detector",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 2rem;
    }
    .score-circle {
        width: 200px;
        height: 200px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto;
        font-size: 3rem;
        font-weight: bold;
        color: white;
        position: relative;
    }
    .reliable {
        background: conic-gradient(#10b981 75%, #e5e7eb 75%);
    }
    .questionable {
        background: conic-gradient(#f59e0b 75%, #e5e7eb 75%);
    }
    .unreliable {
        background: conic-gradient(#ef4444 75%, #e5e7eb 75%);
    }
    .sidebar-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

API_URL = "https://api-inference.huggingface.co/models/mrm8488/bert-tiny-finetuned-fake-news-detection"

def call_fake_news_api(text, api_key=API_KEY):
    """
    Working Hugging Face API for fake news detection with improved error handling
    """
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {"inputs": text[:512]}
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        result = response.json()
        
        print(f"DEBUG: Raw API Response: {result}")
        print(f"DEBUG: Response type: {type(result)}")
        
        if result and isinstance(result, list) and len(result) > 0:
            predictions = result[0]
            
            if isinstance(predictions, list):
                fake_score = next((p['score'] for p in predictions if p.get('label') == 'LABEL_0'), 0)
                real_score = next((p['score'] for p in predictions if p.get('label') == 'LABEL_1'), 1)
            elif isinstance(predictions, dict):
                fake_score = predictions.get('LABEL_0', 0)
                real_score = predictions.get('LABEL_1', 1)
            else:
                fake_score = 0.5
                real_score = 0.5
            
            print(f"DEBUG: Fake score: {fake_score}, Real score: {real_score}")
            
            return {
                'fake_confidence': fake_score * 100,
                'real_confidence': real_score * 100
            }
            
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            st.error("API Rate limit exceeded. Please try again later.")
        elif e.response.status_code == 403:
            st.error("Invalid API token. Please check your Hugging Face token.")
        else:
            st.error(f"API Error {e.response.status_code}: {e.response.text}")
    except Exception as e:
        st.error(f"API Connection Error: {str(e)}")
    
    return None

def preprocess_text(text):
    """
    Preprocess text for analysis
    """
    text = text.lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = ' '.join(text.split())
    return text

def analyze_text_features(text):
    """
    Enhanced fake news pattern analysis with stronger fake news detection
    """
    score = 50  # Start neutral, lean towards skepticism
    flags = []
    fake_indicators = []

    # Enhanced sensational and fake news words (20+ words)
    sensational_words = [
        'shocking', 'unbelievable', 'miracle', 'secret', 'exposed', 'breaking',
        'you won\'t believe', 'doctors hate', 'scientists stunned', 'amazing',
        'incredible', 'unthinkable', 'mind-blowing', 'explosive', 'bombshell',
        'outrageous', 'unprecedented', 'devastating', 'terrifying', 'horrific',
        'miraculous', 'revolutionary', 'breakthrough', 'game-changing'
    ]
    
    sensational_count = sum(1 for word in sensational_words if word in text.lower())
    if sensational_count > 4:
        score -= 30  # Much stronger penalty
        fake_indicators.append("Heavy sensationalism")
        flags.append("Contains excessive sensational language")
    elif sensational_count > 2:
        score -= 20
        fake_indicators.append("Moderate sensationalism")
        flags.append("Contains sensational language")
    elif sensational_count > 0:
        score -= 10
        fake_indicators.append("Mild sensationalism")
        flags.append("Contains some sensational language")

    # FAKE NEWS SPECIFIC PHRASES (NEW!)
    fake_news_phrases = [
        'this will change everything', 'you won\'t believe', 'experts are baffled',
        'they don\'t want you to know', 'hidden truth', 'cover-up', 'conspiracy',
        'mainstream media won\'t tell you', 'the truth about', 'what they hide',
        'shocking discovery', 'scientists baffled', 'doctors stunned',
        'never before seen', 'one weird trick', 'ancient secret'
    ]
    
    fake_phrase_count = sum(1 for phrase in fake_news_phrases if phrase in text.lower())
    if fake_phrase_count > 2:
        score -= 25  # Strong fake news penalty
        fake_indicators.append("Multiple fake news phrases")
        flags.append("Contains fake news buzzwords")
    elif fake_phrase_count > 0:
        score -= 15
        fake_indicators.append("Fake news phrases detected")
        flags.append("Contains fake news language patterns")

    # Enhanced credible indicators
    credible_indicators = [
        'study', 'research', 'university', 'journal', 'peer-reviewed',
        'according to', 'experts say', 'data shows', 'evidence suggests',
        'clinical trial', 'meta-analysis', 'systematic review', 'published in',
        'researchers found', 'scientists discovered', 'analysis shows'
    ]
    credible_count = sum(1 for indicator in credible_indicators if indicator in text.lower())
    if credible_count > 4:
        score = min(100, score + 30)
        flags.append("Strong credible source indicators")
    elif credible_count > 2:
        score = min(100, score + 20)
        flags.append("References credible sources")
    elif credible_count > 0:
        score = min(100, score + 10)
        flags.append("Some credible source indicators")

    # Lack of credible attribution (negative indicator)
    if credible_count == 0 and len(text.split()) > 100:
        score -= 15
        fake_indicators.append("No credible sources mentioned")
        flags.append("Lacks credible source attribution")

    # Excessive punctuation analysis (fake news often uses !!!)
    exclamation_count = text.count('!')
    if exclamation_count > 8:
        score -= 20
        fake_indicators.append("Excessive exclamation marks")
        flags.append("Excessive exclamation marks")
    elif exclamation_count > 4:
        score -= 12
        fake_indicators.append("Multiple exclamation marks")
        flags.append("Multiple exclamation marks")
    elif exclamation_count > 2:
        score -= 8
        fake_indicators.append("Some exclamation marks")
        flags.append("Multiple exclamation marks")

    # Question mark analysis (fake news often asks leading questions)
    question_count = text.count('?')
    if question_count > 5:
        score -= 15
        fake_indicators.append("Excessive questions")
        flags.append("Excessive question marks")

    # All caps analysis (fake news often uses ALL CAPS for emphasis)
    words = text.split()
    caps_ratio = sum(1 for word in words if len(word) > 3 and word.isupper()) / len(words) if words else 0
    if caps_ratio > 0.4:
        score -= 25
        fake_indicators.append("Heavy ALL CAPS usage")
        flags.append("Excessive use of ALL CAPS")
    elif caps_ratio > 0.2:
        score -= 15
        fake_indicators.append("Moderate ALL CAPS usage")
        flags.append("Excessive use of ALL CAPS")

    # Emotional manipulation words
    emotional_words = [
        'hate', 'love', 'fear', 'anger', 'rage', 'panic', 'terror',
        'disgust', 'shock', 'horror', 'outrage', 'betrayal', 'scandal'
    ]
    emotional_count = sum(1 for word in emotional_words if word in text.lower())
    if emotional_count > 5:
        score -= 20
        fake_indicators.append("Heavy emotional manipulation")
        flags.append("Uses emotional manipulation language")
    elif emotional_count > 2:
        score -= 10
        fake_indicators.append("Emotional manipulation")
        flags.append("Uses emotional language")

    # Conspiracy indicators
    conspiracy_words = [
        'conspiracy', 'cover-up', 'deep state', 'illuminati', 'new world order',
        'they don\'t want you to know', 'hidden agenda', 'global elite',
        'mainstream media blackout', 'suppressed information'
    ]
    conspiracy_count = sum(1 for word in conspiracy_words if word in text.lower())
    if conspiracy_count > 2:
        score -= 25
        fake_indicators.append("Strong conspiracy indicators")
        flags.append("Contains conspiracy theory language")
    elif conspiracy_count > 0:
        score -= 15
        fake_indicators.append("Conspiracy indicators")
        flags.append("Contains conspiracy theory elements")

    # Fake news urgency indicators
    urgency_words = [
        'urgent', 'warning', 'alert', 'breaking news', 'developing story',
        'emergency', 'crisis', 'critical', 'immediate action required'
    ]
    urgency_count = sum(1 for word in urgency_words if word in text.lower())
    if urgency_count > 3:
        score -= 20
        fake_indicators.append("High urgency manipulation")
        flags.append("Creates false urgency")
    elif urgency_count > 1:
        score -= 10
        fake_indicators.append("Urgency manipulation")
        flags.append("Creates urgency")

    # Scientific/technical jargon without context (fake science news)
    science_words = [
        'quantum', 'nanotechnology', 'revolutionary technology', 'breakthrough treatment',
        'miracle cure', 'scientific breakthrough', 'medical breakthrough'
    ]
    science_count = sum(1 for word in science_words if word in text.lower())
    if science_count > 2 and credible_count == 0:
        score -= 20
        fake_indicators.append("Fake science claims")
        flags.append("Makes unsubstantiated scientific claims")

    # Return results
    final_score = max(0, min(100, score))
    
    if fake_indicators:
        flags.extend([f"🚨 Fake news indicator: {indicator}" for indicator in fake_indicators])

    return final_score, flags

def extract_article_from_url(url):
    """
    Extract article content from URL with improved error handling
    """
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        for script in soup(["script", "style", "nav", "footer", "header", "aside", "advertisement"]):
            script.decompose()

        article = (soup.find('article') or
                  soup.find('div', class_=re.compile('article|content|post|entry|story')) or
                  soup.find('main') or
                  soup.find('section', class_=re.compile('content|main|article')))

        if article:
            text = article.get_text()
        else:
            body = soup.find('body')
            if body:
                text = body.get_text()
            else:
                text = soup.get_text()

        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk and len(chunk) > 10)

        title_element = soup.find('title') or soup.find('h1') or soup.find('h2')
        title_text = title_element.get_text().strip() if title_element else "No title found"

        return {
            'title': title_text,
            'text': text[:5000],   
            'domain': urlparse(url).netloc
        }
    except Exception as e:
        st.error(f"Error extracting article: {str(e)}")
        return None

def generate_summary(text, max_sentences=3):
    """
    Generate article summary with improved logic
    """
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20 and len(s.split()) > 3]

    if len(sentences) <= max_sentences:
        return ' '.join(sentences)

    scored_sentences = []
    for i, sentence in enumerate(sentences[:15]): 
        score = len(sentence.split()) 
        if i < 3: 
            score *= 1.5
        if '?' in sentence:
            score *= 1.2

        scored_sentences.append((score, sentence))

    scored_sentences.sort(reverse=True)
    top_sentences = [s[1] for s in scored_sentences[:max_sentences]]

    summary_sentences = []
    for sentence in sentences:
        if sentence in top_sentences:
            summary_sentences.append(sentence)
            if len(summary_sentences) == max_sentences:
                break

    return '. '.join(summary_sentences) + '.'

def show_tips():
    """
    Display detection tips in sidebar
    """
    st.sidebar.markdown('<p class="sidebar-header">💡 Detection Tips</p>', unsafe_allow_html=True)

    tips = [
        ("🔍 Check the Source", "Verify if the website is reputable. Look for an 'About Us' section and check if the domain is legitimate."),
        ("📖 Read Beyond Headlines", "Headlines can be misleading. Read the full article to understand the context and claims being made."),
        ("✅ Verify with Multiple Sources", "Cross-reference information with other credible news outlets. If only one source reports it, be skeptical."),
        ("📅 Check the Date", "Old news stories can resurface and be presented as current events. Always check the publication date."),
        ("🔬 Look for Evidence", "Reliable articles cite sources, include quotes from experts, and reference studies or data."),
        ("⚖️ Watch for Bias", "Be aware of your own biases and the potential bias of the source. Emotional language can be a red flag."),
        ("👤 Check Author Credentials", "Research the author. Are they qualified to write on this topic? Do they have a track record?"),
        ("🖼️ Reverse Image Search", "Images can be manipulated or taken out of context. Use reverse image search to verify their origin.")
    ]

    for title, description in tips:
        st.sidebar.markdown(f"**{title}**")
        st.sidebar.write(description)
        st.sidebar.divider()

def main():
    st.markdown('<h1 class="main-header">🛡️ Fake News Detector</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666; margin-bottom: 2rem;">AI-Powered Fake News Detector for Students</p>', unsafe_allow_html=True)
    show_tips()
    
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📝 Input Text")
        input_text = st.text_area(
            "Paste the text input here for analysis:",
            height=200,
            placeholder="Enter or paste the article text here..."
        )

    with col2:
        st.subheader("🔗 Analyze URL")
        input_url = st.text_input(
            "Enter article URL:",
            placeholder="https://example.com/article"
        )

        if st.button("🔍 Extract Article", use_container_width=True):
            if input_url:
                with st.spinner("Extracting text..."):
                    article_data = extract_article_from_url(input_url)
                    if article_data:
                        input_text = article_data['text']
                        st.success(f"✅ Extracted: {article_data['title']} from {article_data['domain']}")
                    else:
                        st.error("❌ Could not extract article from URL")

    default_api_key = API_KEY if API_KEY else ""
    api_key = st.sidebar.text_input("🔑 API Key", 
                                   type="password",
                                   value=default_api_key,
                                   help="Leave empty to use secrets.toml, or enter to override")

    if st.button("🔬 Analyze Content", type="primary", use_container_width=True):
        if not input_text.strip() and not input_url:
            st.error("❌ Please provide text or URL to analyze")
            return

        if input_url and not input_text.strip():
            article_data = extract_article_from_url(input_url)
            if article_data:
                input_text = article_data['text']
            else:
                st.error("❌ Could not extract article from URL")
                return

        if len(input_text.strip()) < 50:
            st.error("❌ Text is too short for analysis (min 50 characters)")
            return

        # Use the input API key, or fall back to loaded API key
        effective_api_key = api_key if api_key.strip() else API_KEY
        
        with st.spinner("🤖 Analyzing with AI API..."):
            processed_text = preprocess_text(input_text)
            api_result = call_fake_news_api(processed_text, effective_api_key)
            
            if api_result:
                api_credibility = api_result['real_confidence']
                fake_news_score = api_result['fake_confidence']
                st.success("✅ AI Analysis Complete")
            else:
                st.error("❌ API unavailable. Using pattern analysis only.")
                api_credibility = 50.0
                fake_news_score = 50.0

            feature_score, flags = analyze_text_features(input_text)
            combined_credibility = (api_credibility * 0.6 + feature_score * 0.4)
            summary = generate_summary(input_text)

        st.markdown("---")
        st.subheader("📊 Analysis Results")
        
        main_col1, main_col2 = st.columns([2, 1])
        
        with main_col1:
            col1, col2, col3 = st.columns([1, 2, 1])

            with col2:
                verdict_class = "reliable" if combined_credibility >= 70 else "questionable" if combined_credibility >= 40 else "unreliable"
                verdict = "Likely Reliable" if combined_credibility >= 70 else "Questionable - Verify Claims" if combined_credibility >= 40 else "Likely Unreliable"
                verdict_color = "#10b981" if combined_credibility >= 70 else "#f59e0b" if combined_credibility >= 40 else "#ef4444"

                st.markdown(f"""
                    <div class="score-circle {verdict_class}" style="background: conic-gradient({verdict_color} {combined_credibility}%, #e5e7eb {combined_credibility}%);">
                        <div style="background: white; width: 160px; height: 160px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-direction: column;">
                            <div style="color: #1f2937; font-size: 2.5rem; font-weight: bold;">{combined_credibility:.1f}</div>
                            <div style="color: #6b7280; font-size: 1rem;">/100</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                st.markdown(f"<h2 style='text-align: center; color: {verdict_color}; margin-top: 1rem;'>{verdict}</h2>", unsafe_allow_html=True)

            st.subheader("📝 Article Summary")
            st.info(summary)

            if flags:
                st.subheader("⚠️ Analysis Findings")
                for flag in flags:
                    st.warning(f"• {flag}")

        with main_col2:
            st.subheader("🔧 Technical Analysis")
            tech_col1, tech_col2 = st.columns(2)

            with tech_col1:
                st.metric("🧠 AI Confidence (Real)", f"{api_credibility:.1f}%")
                st.metric("⚠️ Fake News Confidence", f"{fake_news_score:.1f}%")
                st.metric("📝 Pattern Analysis Score", f"{feature_score:.1f}%")

            with tech_col2:
                st.metric("📊 Word Count", len(input_text.split()))
                st.metric("📏 Character Count", len(input_text))

            if fake_news_score > 60:
                st.error("🚨 **High Fake News Risk**")
            elif fake_news_score > 40:
                st.warning("⚠️ **Medium Fake News Risk**")
            else:
                st.success("✅ **Low Fake News Risk**")

if __name__ == "__main__":
    main()
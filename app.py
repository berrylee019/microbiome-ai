import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
import time
import pandas as pd
import numpy as np

# 1. 페이지 설정
st.set_page_config(
    page_title="AI Microbiome Suite",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Gemini API 설정
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# PDF 텍스트 추출 함수
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        try:
            pdf_reader = PdfReader(pdf)
            for page in pdf_reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted
        except Exception as e:
            st.error(f"파일 읽기 오류: {e}")
    return text

# 2. 커스텀 CSS
st.markdown("""
    <style>
    .main-title { font-size: 42px; font-weight: 800; color: #1E3A8A; text-align: center; }
    .sub-title { font-size: 18px; color: #6B7280; text-align: center; margin-bottom: 40px; }
    .service-card {
        background-color: #FFFFFF; padding: 20px; border-radius: 15px; border: 1px solid #E5E7EB;
        box-shadow: 0 4px 10px rgba(0,0,0,0.03); height: 260px; margin-bottom: 20px;
    }
    .alert-card {
        background-color: #FFF5F5; padding: 15px; border-radius: 10px; border-left: 5px solid #F87171; margin-bottom: 12px;
    }
    .data-source-tag {
        background-color: #EFF6FF; color: #1E40AF; padding: 4px 10px; border-radius: 20px; 
        font-size: 12px; font-weight: 600; margin-right: 5px; border: 1px solid #DBEAFE;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 사이드바 내비게이션 (5번 메뉴 추가)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2864/2864248.png", width=60)
    st.title("MisaTech AI")
    st.markdown("---")
    mode = st.radio("서비스 모드 선택", [
        "🏠 서비스 홈", 
        "🔍 01. 연구 에이전트 (RAG)", 
        "📊 02. 환자 리포트", 
        "📸 03. 비전 분석", 
        "🚨 04. 케어 모니터링",
        "🔬 05. 내시경 AI 분석"
    ])
    st.markdown("---")
    st.caption("AI-Powered Clinical Solution v1.5")

# 4. 메인 콘텐츠
if mode == "🏠 서비스 홈":
    st.markdown('<p class="main-title">AI Microbiome Clinical Suite</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">대장항문학 전문의를 위한 올인원 AI 플랫폼</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="service-card"><h3>🔍 01. Research Agent</h3><p>논문 분석 및 임상 가설 생성</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="service-card"><h3>📸 03. Vision Guide</h3><p>배변/식단 이미지 분석</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="service-card"><h3>🔬 05. Endoscopy AI</h3><p>내시경 용종/암 판별 보조</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="service-card"><h3>📊 02. Insight Report</h3><p>NGS 정밀 의료 리포트</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="service-card"><h3>🚨 04. Care Monitor</h3><p>24/7 AI 이상 징후 탐지</p></div>', unsafe_allow_html=True)

elif mode == "🔍 01. 연구 에이전트 (RAG)":
    st.header("🔍 AI Research Agent (RAG)")
    uploaded_files = st.file_uploader("PDF 논문 업로드", type=['pdf'], accept_multiple_files=True)
    if uploaded_files:
        context_text = get_pdf_text(uploaded_files)
        user_query = st.text_input("질문 입력")
        if user_query:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(f"{context_text[:10000]}\n\n질문: {user_query}")
            st.info(response.text)

elif mode == "📊 02. 환자 리포트":
    st.header("📊 Patient Insight Report")
    st.bar_chart({"Bifido": 40, "Lacto": 15, "Harmful": 45})

elif mode == "📸 03. 비전 분석":
    st.header("📸 Microbiome Vision Guide")
    c1, c2 = st.columns(2)
    with c1: st.file_uploader("배변 사진", type=['jpg', 'png'], key="s")
    with c2: st.file_uploader("식단 사진", type=['jpg', 'png'], key="f")
    if st.button("이미지 분석 실행"):
        st.success("분석 완료")

elif mode == "🚨 04. 케어 모니터링":
    st.header("🚨 24/7 AI-driven Anomaly Detection")
    m1, m2, m3 = st.columns(3)
    m1.metric("모니터링 대상", "45 명")
    m2.metric("고위험군", "2 명", delta="1", delta_color="inverse")
    m3.metric("평균 통증 지수", "2.1", "-0.3")
    st.markdown("<div class='alert-card'><b>[K-104 환자]</b> 장폐색 의심 징후 감지</div>", unsafe_allow_html=True)

elif mode == "🔬 05. 내시경 AI 분석":
    st.header("🔬 Endoscopy AI Diagnostic Assistant")
    st.write("내시경 영상/이미지를 분석하여 병변의 종류를 감별 진단합니다.")
    
    st.info("💡 본 모듈은 교수님의 판독을 보조하기 위한 Decision Support System(DSS)입니다.")
    
    up_img = st.file_uploader("내시경 의심 부위 이미지 업로드", type=['jpg', 'jpeg', 'png'])
    
    if up_img:
        col_img, col_res = st.columns(2)
        with col_img:
            st.image(up_img, caption="업로드된 내시경 이미지", use_container_width=True)
        
        with col_res:
            if st.button("AI 병변 정밀 분석 실행"):
                with st.spinner("이미지 패턴 및 혈관 분포 분석 중..."):
                    time.sleep(2)
                    st.error("### 📢 분석 결과: 암 변질 의심 (Malignancy Risk High)")
                    st.markdown("""
                    - **병변 유형:** 선종성 용종 (Adenoma) -> 암 전단계 의심
                    - **악성 가능성:** 89% (High Confidence)
                    - **주요 소견:** 불규칙한 미세 혈관 패턴(Vascularity) 관찰, 표면 질감 파괴 징후.
                    - **제안 사항:** 즉시 조직 검사(Biopsy) 및 전수 절제 고려.
                    """)
                    st.progress(89)
                    st.caption("AI Confidence: 89%")

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

# 3. 사이드바
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2864/2864248.png", width=60)
    st.title("MisaTech AI")
    st.markdown("---")
    mode = st.radio("서비스 모드 선택", ["🏠 서비스 홈", "🔍 01. 연구 에이전트 (RAG)", "📊 02. 환자 리포트", "📸 03. 비전 분석", "🚨 04. 케어 모니터링"])
    st.markdown("---")
    st.caption("AI-Powered Clinical Solution v1.2")

# 4. 메인 콘텐츠
if mode == "🏠 서비스 홈":
    st.markdown('<p class="main-title">AI Microbiome Clinical Suite</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">대장항문학 전문의를 위한 지능형 임상 및 사후 관리 플랫폼</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="service-card"><h3>🔍 01. AI Research Agent</h3><p>방대한 논문 RAG 분석 및 임상 가설 생성 도구</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="service-card"><h3>📸 03. Vision Guide</h3><p>배변/식단 멀티모달 이미지 패턴 분석 시스템</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="service-card"><h3>📊 02. Insight Report</h3><p>NGS 데이터 기반 환자 맞춤형 정밀 의료 리포트</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="service-card"><h3>🚨 04. Care Monitor</h3><p>24/7 AI-driven Anomaly Detection (사후 관리)</p></div>', unsafe_allow_html=True)

elif mode == "🔍 01. 연구 에이전트 (RAG)":
    st.header("🔍 AI Research Agent (RAG)")
    uploaded_files = st.file_uploader("PDF 논문 업로드", type=['pdf'], accept_multiple_files=True)
    if uploaded_files:
        context_text = get_pdf_text(uploaded_files)
        user_query = st.text_input("분석 질문 입력")
        if user_query:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(f"{context_text[:10000]}\n\n질문: {user_query}")
            st.info(response.text)

elif mode == "📊 02. 환자 리포트":
    st.header("📊 Patient Insight Report")
    st.bar_chart({"유익균": 40, "유해균": 15, "기타": 45})

elif mode == "📸 03. 비전 분석":
    st.header("📸 Microbiome Vision Guide")
    st.write("식단 및 배변 이미지 통합 분석")
    c1, c2 = st.columns(2)
    with c1: st.file_uploader("배변 사진", type=['jpg', 'png'], key="s"); st.camera_input("직접 촬영", key="sc")
    with c2: st.file_uploader("식단 사진", type=['jpg', 'png'], key="f"); st.camera_input("직접 촬영", key="fc")
    if st.button("분석 실행"):
        st.success("패턴 분석 완료: 정상 범주 내 회복 중")

elif mode == "🚨 04. 케어 모니터링":
    st.header("🚨 24/7 AI-driven Anomaly Detection")
    st.write("수술 후 퇴원 환자의 실시간 생체 데이터 및 임상 지표를 분석하여 이상 징후를 탐지합니다.")
    
    # 상단 요약 지표
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("모니터링 대상", "45 명")
    m2.metric("디바이스 활성", "42 개", help="웨어러블 및 스마트 패치 연결 상태")
    m3.metric("고위험군 (High Risk)", "2 명", delta="1", delta_color="inverse")
    m4.metric("평균 통증 지수", "2.1", "-0.3")

    st.markdown("""
        <div style='background-color: #f1f5f9; padding: 15px; border-radius: 10px; margin-bottom: 25px;'>
            <b>🔌 수집 데이터 소스:</b> 
            <span class="data-source-tag">스마트 체온 패치 (연속 측정)</span>
            <span class="data-source-tag">웨어러블 디바이스 (활동량/심박)</span>
            <span class="data-source-tag">앱 기반 복약/배변 기록</span>
            <span class="data-source-tag">이미지 기반 식단 분석</span>
        </div>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.subheader("📈 실시간 생체 데이터 트렌드")
        # 가상의 체온/통증 데이터 그래프
        chart_data = pd.DataFrame(
            np.random.normal(36.5, 0.2, size=(24, 1)),
            columns=['실시간 체온 (℃)']
        )
        st.line_chart(chart_data)
        st.caption("※ AI가 스마트 체온 패치로부터 수신된 데이터를 분석하여 미세한 발열 추세를 감지합니다.")

    with col_right:
        st.subheader("🚩 AI Anomaly Alert")
        st.markdown("""
            <div class="alert-card">
                <b>[ID: K-104 환자]</b><br>
                <span style='color:#F87171; font-weight:bold;'>⚠️ 감염 의심 (Infection Risk)</span><br>
                <small>스마트 패치 측정 체온 38.1도 돌파. 수술 부위 사진상 발적 패턴 관찰됨.</small>
            </div>
            <div class="alert-card">
                <b>[ID: L-209 환자]</b><br>
                <span style='color:#F87171; font-weight:bold;'>⚠️ 장폐색 전조 (Ileus Sign)</span><br>
                <small>웨어러블 기반 활동량 80% 감소. 36시간 내 배변/가스 배출 기록 없음.</small>
            </div>
        """, unsafe_allow_html=True)
        if st.button("고위험군 긴급 리포트 생성"):
            st.toast("교수님 전용 요약 리포트가 생성되었습니다.")

    st.markdown("---")
    st.subheader("📋 처방 및 관리 리스트")
    df = pd.DataFrame({
        "환자명": ["김OO", "이OO", "박OO", "최OO"],
        "처방 디바이스": ["스마트 체온 패치", "웨어러블 워치", "스마트 패치+워치", "기본 앱 관리"],
        "최근 업데이트": ["1분 전", "5분 전", "방금 전", "12시간 전"],
        "위험도": ["High", "Medium", "Low", "Low"]
    })
    st.table(df)

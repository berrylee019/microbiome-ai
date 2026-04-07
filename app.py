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
    .main-title { font-size: 48px; font-weight: 800; color: #1E3A8A; text-align: center; }
    .sub-title { font-size: 20px; color: #6B7280; text-align: center; margin-bottom: 50px; }
    .service-card {
        background-color: #FFFFFF; padding: 25px; border-radius: 18px; border: 1px solid #E5E7EB;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05); height: 280px; margin-bottom: 25px;
    }
    .alert-card {
        background-color: #FFF5F5; padding: 15px; border-radius: 10px; border-left: 5px solid #F87171; margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 사이드바
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2864/2864248.png", width=70)
    st.title("MisaTech AI")
    mode = st.radio("서비스 모드 선택", ["🏠 서비스 홈", "🔍 01. 연구 에이전트 (RAG)", "📊 02. 환자 리포트", "📸 03. 비전 분석", "🚨 04. 케어 모니터링"])

# 4. 메인 콘텐츠
if mode == "🏠 서비스 홈":
    st.markdown('<p class="main-title">AI Microbiome Clinical Suite</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">대장항문학 전문의를 위한 지능형 임상 지원 플랫폼</p>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="service-card"><h3>🔍 01. Research Agent</h3><p>논문 RAG 분석 및 가설 생성</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="service-card"><h3>📸 03. Vision Guide</h3><p>배변/식단 이미지 패턴 분석</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="service-card"><h3>📊 02. Insight Report</h3><p>데이터 기반 환자 맞춤 리포트</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="service-card"><h3>🚨 04. Care Monitor</h3><p>수술 후 이상 징후 실시간 탐지</p></div>', unsafe_allow_html=True)

elif mode == "🔍 01. 연구 에이전트 (RAG)":
    st.header("🔍 AI Research Agent (RAG Demo)")
    uploaded_files = st.file_uploader("PDF 논문 업로드", type=['pdf'], accept_multiple_files=True)
    if uploaded_files:
        context_text = get_pdf_text(uploaded_files)
        user_query = st.text_input("질문을 입력하세요")
        if user_query:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(f"{context_text[:10000]}\n\n질문: {user_query}")
            st.info(response.text)

elif mode == "📊 02. 환자 리포트":
    st.header("📊 Patient Insight Report")
    st.file_uploader("데이터 업로드", type=['csv'])
    st.bar_chart({"유익균": 40, "유해균": 20, "중간균": 40})

elif mode == "📸 03. 비전 분석":
    st.header("📸 Microbiome Vision Guide")
    c1, c2 = st.columns(2)
    with c1: st.file_uploader("배변 사진", type=['jpg', 'png'], key="s"); st.camera_input("촬영", key="sc")
    with c2: st.file_uploader("식단 사진", type=['jpg', 'png'], key="f"); st.camera_input("촬영", key="fc")
    if st.button("이미지 패턴 분석 실행"):
        with st.spinner("분석 중..."):
            time.sleep(2)
            st.success("분석 완료: 브리스톨 4단계 / 섬유질 부족 관찰")

elif mode == "🚨 04. 케어 모니터링":
    st.header("🚨 Clinical Care Monitor (수술 후 사후 관리)")
    st.write("재택 회복 중인 환자들의 실시간 상태를 모니터링하며, AI가 이상 탐지 시 즉시 알림을 제공합니다.")
    
    # 상단 요약 지표
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("전체 관리 환자", "45 명")
    m2.metric("오늘 신규 기록", "32 건")
    m3.metric("주의 필요 (High Risk)", "2 명", delta="1", delta_color="inverse")
    m4.metric("평균 통증 지수", "2.4 / 10", "-0.2")

    st.markdown("---")
    
    col_chart, col_list = st.columns([2, 1])
    
    with col_chart:
        st.subheader("📈 주간 이상 징후 발생 트렌드")
        chart_data = pd.DataFrame(np.random.randn(7, 2), columns=['통증 수치', '염증 지표'])
        st.line_chart(chart_data)
        st.caption("※ AI가 환자들의 평균 회복 곡선에서 이탈하는 패턴을 실시간 추적합니다.")

    with col_list:
        st.subheader("🚩 AI 실시간 경고 (Alert)")
        st.markdown("""
            <div class="alert-card">
                <b>[김OO 환자 - 703호 퇴원]</b><br>
                ⚠️ 장폐색(Ileus) 의심 패턴 감지<br>
                <small>배변 횟수 0회(48시간), 복부 팽만감 호소</small>
            </div>
            <div class="alert-card">
                <b>[이OO 환자 - 512호 퇴원]</b><br>
                ⚠️ 수술 부위 감염 위험 상승<br>
                <small>체온 38.2도 유지, VAS 통증 점수 급증(3->7)</small>
            </div>
        """, unsafe_allow_html=True)
        if st.button("담당 간호사 알림 전송"):
            st.toast("고위험군 환자 리포트가 전송되었습니다.")

    st.markdown("---")
    st.subheader("📋 전체 환자 모니터링 리스트")
    df = pd.DataFrame({
        "환자명": ["김OO", "이OO", "박OO", "최OO", "정OO"],
        "수술명": ["Laparoscopic LAR", "Hemorrhoidectomy", "Fistulotomy", "Colectomy", "LAR"],
        "회복 점수": [45, 62, 88, 92, 85],
        "상태": ["위험", "주의", "정상", "정상", "정상"]
    })
    st.table(df)

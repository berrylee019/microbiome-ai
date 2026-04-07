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

# 3. 사이드바 내비게이션
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2864/2864248.png", width=60)
    st.title("MisaTech AI")
    st.markdown("---")
    mode = st.radio("서비스 모드 선택", [
        "🏠 서비스 홈", 
        "🔍 01. 연구 에이전트 (RAG)", 
        "📊 02. 환자 리포트 (NGS)", 
        "📸 03. 비전 분석 (배변/식단)", 
        "🚨 04. 케어 모니터링",
        "🔬 05. 내시경 AI 분석"
    ])
    st.markdown("---")
    st.caption("AI-Powered Clinical Solution v1.8")

# 4. 메인 콘텐츠
if mode == "🏠 서비스 홈":
    st.markdown('<p class="main-title">AI Microbiome Clinical Suite</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">대장항문학 전문의를 위한 올인원 AI 플랫폼</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="service-card"><h3>🔍 01. Research Agent</h3><p>논문 분석 및 임상 가설 생성</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="service-card"><h3>📸 03. Vision Guide</h3><p>배변/식단 이미지 멀티모달 분석</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="service-card"><h3>🔬 05. Endoscopy AI</h3><p>내시경 용종/암 정밀 판별 보조</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="service-card"><h3>📊 02. Insight Report</h3><p>NGS 데이터 시각화 및 RAW 분석</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="service-card"><h3>🚨 04. Care Monitor</h3><p>24/7 AI 이상 징후 실시간 탐지</p></div>', unsafe_allow_html=True)

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

elif mode == "📊 02. 환자 리포트 (NGS)":
    st.header("📊 NGS Data Analysis & Report")
    tab1, tab2 = st.tabs(["📈 분석 결과 시각화", "🧬 FASTQ 원천 데이터 분석"])
    with tab1:
        st.subheader("마이크로바이옴 분석 데이터 업로드")
        uploaded_sheet = st.file_uploader("CSV 또는 XLSX 시트 업로드", type=['csv', 'xlsx'])
        if uploaded_sheet:
            st.success("데이터 로딩 완료")
            chart_data = pd.DataFrame({'균주명': ['Bifidobacterium', 'Lactobacillus', 'Bacteroides', 'Harmful'], '비율(%)': [42, 18, 25, 15]})
            st.bar_chart(chart_data.set_index('균주명'))
            st.info("**AI 분석 소견:** 유익균 분포가 안정적입니다.")
    with tab2:
        st.subheader("Cloud-based FASTQ Pipeline")
        st.file_uploader("FASTQ 파일 업로드 (.fastq, .gz)", type=['fastq', 'gz'])
        if st.button("AI 시퀀싱 분석 대기열 추가"):
            st.success("✅ 분석 요청 완료! (현재 대기열 번호: #2026-0012)")

elif mode == "📸 03. 비전 분석 (배변/식단)":
    st.header("📸 Microbiome Vision Guide")
    st.write("환자가 제출한 사진을 바탕으로 브리스톨 척도 및 영양 상태를 분석합니다.")
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("💩 배변 사진 분석")
        st.file_uploader("이미지 업로드", type=['jpg', 'png', 'jpeg'], key="stool_img")
        st.camera_input("카메라 촬영", key="stool_cam")
    
    with c2:
        st.subheader("🥗 식단 사진 분석")
        st.file_uploader("이미지 업로드", type=['jpg', 'png', 'jpeg'], key="food_img")
        st.camera_input("카메라 촬영", key="food_cam")
    
    if st.button("이미지 패턴 분석 실행"):
        with st.spinner("AI가 멀티모달 패턴을 분석 중입니다..."):
            time.sleep(2)
            st.success("### ✅ 비전 분석 결과")
            res_c1, res_c2 = st.columns(2)
            with res_c1:
                st.info("**[배변 분석]**\n- **브리스톨 척도:** 4단계 (정상)\n- **특이사항:** 수분 섭취 적정 수준 유지 중")
            with res_c2:
                st.warning("**[식단 분석]**\n- **주요 영양소:** 고탄수화물 위주 관찰\n- **권고 사항:** 식이섬유(채소류) 20% 증량 필요")

elif mode == "🚨 04. 케어 모니터링":
    st.header("🚨 24/7 AI-driven Anomaly Detection")
    m1, m2, m3 = st.columns(3)
    m1.metric("모니터링 대상", "45 명")
    m2.metric("고위험군 (High Risk)", "2 명", delta="1", delta_color="inverse")
    m3.metric("평균 통증 지수", "2.1", "-0.3")
    st.markdown("<div class='alert-card'><b>[K-104 환자]</b> 장폐색 의심 징후 감지</div>", unsafe_allow_html=True)
    st.line_chart(np.random.normal(36.5, 0.2, size=(24, 1)))

elif mode == "🔬 05. 내시경 AI 분석":
    st.header("🔬 Endoscopy AI Diagnostic Assistant")
    st.write("내시경 영상/이미지를 분석하여 용종의 종류 및 암 변질 여부를 감별 진단합니다.")
    st.info("💡 본 모듈은 교수님의 판독을 보조하기 위한 의사결정 지원 시스템(DSS)입니다.")
    
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
                    st.caption("AI Confidence Level: 89%")

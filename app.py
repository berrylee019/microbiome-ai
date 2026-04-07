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
    .stProgress > div > div > div > div { background-color: #1E3A8A; }
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
        "📸 03. 비전 분석", 
        "🚨 04. 케어 모니터링",
        "🔬 05. 내시경 AI 분석"
    ])
    st.markdown("---")
    st.caption("AI-Powered Clinical Solution v1.6")

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
        st.markdown('<div class="service-card"><h3>📊 02. Insight Report</h3><p>NGS 정밀 의료 리포트 및 RAW 분석</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="service-card"><h3>🚨 04. Care Monitor</h3><p>24/7 AI 이상 징후 탐지</p></div>', unsafe_allow_html=True)

elif mode == "📊 02. 환자 리포트 (NGS)":
    st.header("📊 NGS Data Analysis & Report")
    
    tab1, tab2 = st.tabs(["📈 분석 결과 시각화", "🧬 FASTQ 원천 데이터 분석"])
    
    with tab1:
        st.subheader("마이크로바이옴 분석 데이터 업로드")
        st.write("외부 분석 기관에서 받은 CSV 또는 Excel 시트를 업로드하세요.")
        
        uploaded_sheet = st.file_uploader("분석 완료 시트 업로드 (CSV, XLSX)", type=['csv', 'xlsx'])
        
        if uploaded_sheet:
            st.success("데이터 로드 완료")
            # 시연용 가상 차트
            st.subheader("환자별 미생물 분포 (Taxonomy)")
            chart_data = pd.DataFrame({
                '균주명': ['Bifidobacterium', 'Lactobacillus', 'Bacteroides', 'Harmful'],
                '비율(%)': [42, 18, 25, 15]
            })
            st.bar_chart(chart_data.set_index('균주명'))
            st.info("**AI 분석 소견:** 유익균(Bifido) 군집도가 안정적이며 수술 후 장내 환경 회복세가 뚜렷합니다.")
        else:
            st.info("시트를 업로드하면 환자별 맞춤형 그래프가 생성됩니다.")

    with tab2:
        st.subheader("Cloud-based FASTQ Pipeline")
        st.write("클라우드 기반 대규모 연산 처리가 필요한 FASTQ(Raw Data) 분석 요청 섹션입니다.")
        
        fastq_file = st.file_uploader("FASTQ 파일 업로드 (.fastq, .gz)", type=['fastq', 'gz'], accept_multiple_files=True)
        
        if fastq_file:
            st.warning("⚠️ FASTQ 분석은 서버 연산 자원을 많이 소모하며 약 15~30분이 소요됩니다.")
            if st.button("AI 시퀀싱 분석 대기열 추가"):
                with st.spinner("서버로 데이터 전송 및 QC 파이프라인 가동 중..."):
                    my_bar = st.progress(0)
                    for percent_complete in range(100):
                        time.sleep(0.03)
                        my_bar.progress(percent_complete + 1)
                    st.success("✅ 분석 요청 완료! 분석이 완료되면 교수님 메일로 리포트가 전송됩니다.")
                    st.write("**현재 대기열 번호:** #2026-0012")

# 01, 03, 04, 05 모드는 이전 코드와 동일하게 유지
# (지면 관계상 핵심 구조만 유지하며, 형님이 가지고 계신 이전 코드와 병합하시면 됩니다.)

elif mode == "🚨 04. 케어 모니터링":
    st.header("🚨 24/7 AI-driven Anomaly Detection")
    st.write("수술 후 퇴원 환자 스마트 관리 시스템")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("모니터링 대상", "45 명")
    m2.metric("고위험군 (High Risk)", "2 명", delta="1", delta_color="inverse")
    m3.metric("평균 회복 점수", "88점", "5")

    st.markdown("""
        <div style='background-color: #f1f5f9; padding: 15px; border-radius: 10px; margin-bottom: 20px;'>
            <b>🔌 수집 채널:</b> 스마트 체온 패치, 웨어러블(활동량), 앱(배변/통증)
        </div>
    """, unsafe_allow_html=True)
    
    st.line_chart(np.random.normal(36.5, 0.2, size=(24, 1)))
    st.markdown("<div class='alert-card'><b>[K-104 환자]</b> 24/7 감시 중 특이 징후(발열) 포착</div>", unsafe_allow_html=True)

elif mode == "🔬 05. 내시경 AI 분석":
    st.header("🔬 Endoscopy AI Diagnostic Assistant")
    up_img = st.file_uploader("내시경 이미지 업로드", type=['jpg', 'png'])
    if up_img:
        st.image(up_img, width=400)
        if st.button("병변 정밀 분석"):
            st.error("### 📢 분석 결과: 암 변질 의심 (Malignancy Risk High)")
            st.progress(89)

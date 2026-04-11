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
    .security-banner {
        background-color: #F0F9FF; padding: 15px; border-radius: 10px; border: 1px solid #BAE6FD; 
        color: #0369A1; font-weight: 600; text-align: center; margin-bottom: 20px;
    }
    /* 하드웨어 연동 안내 문구 스타일 */
    .hardware-info {
        background-color: #F8FAFC; padding: 20px; border-radius: 12px; border: 1px solid #E2E8F0;
        color: #475569; font-size: 15px; line-height: 1.6; text-align: center;
        margin-top: 25px; margin-bottom: 10px; width: 80%; margin-left: auto; margin-right: auto;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 사이드바 설정
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2864/2864248.png", width=60)
    st.title("MisaTech AI")
    st.markdown("---")
    view_mode = st.sidebar.radio(
        "🕹️ 시연 시나리오 선택", 
        ["👨‍⚕️ 원장님 (관리 모드)", "📱 환자 (모바일 예진)"],
        index=0
    )
    st.markdown("---")

    if view_mode == "👨‍⚕️ 원장님 (관리 모드)":
        mode = st.radio("서비스 모드 선택", [
            "🏠 서비스 홈", 
            "🔍 01. 연구 에이전트 (RAG)", 
            "📊 02. 환자 리포트 (NGS/OCR)", 
            "📸 03. 익명 비전 예진 (항문/식단)", 
            "🚨 04. 케어 모니터링",
            "🔬 05. 내시경 AI 분석"
        ])
    else:
        mode = "👤 환자 전용 예진창"
        st.info("📱 환자 휴대폰 화면 시연 중")
    st.markdown("---")
    st.caption("AI-Powered Clinical Solution v1.99 (Final Polish)")

# 4. 메인 콘텐츠 로직

# [환자 모드 시연 화면]
if view_mode == "📱 환자 (모바일 예진)":
    st.header("📱 스마트 익명 예진 시스템")
    st.markdown('<div class="security-banner">🔒 보안 안내: 모든 개인정보 및 사진은 AI 분석 즉시 파기되며 저장되지 않습니다.</div>', unsafe_allow_html=True)
    
    with st.container(border=True):
        st.subheader("📸 증상 사진 및 문진")
        up_file = st.file_uploader("증상 부위 사진 업로드 (익명)", type=['jpg','png','jpeg'])
        if up_file:
            st.image(up_file, width=300)
        st.text_area("현재 겪고 계신 불편함을 적어주세요.", placeholder="예: 배변 시 통증이 있고 선홍색 피가 납니다.")
        
        if st.button("🚀 AI 분석 및 전문의 연결"):
            with st.spinner("AI가 증상을 분석 중입니다..."):
                time.sleep(2)
                st.session_state.new_reservation = True
                st.session_state.patient_status = "치핵 3기 의심"
            st.error("### 📢 분석 결과: 내치핵 3도 (Grade 3)")
            st.warning("🏥 **장앤항외과 원장님**께 데이터를 전송하고 우선 진료 예약을 진행하시겠습니까?")
            if st.button("📅 즉시 진료 예약하기"):
                st.balloons()
                st.success("🎉 예약 신청 완료! 원장님 화면으로 데이터가 전송되었습니다.")

# [원장님 모드 시연 화면]
else:
    if st.session_state.get('new_reservation'):
        st.toast(f"🚨 [신규 예약] {st.session_state.patient_status} 환자가 발생했습니다!", icon="🚨")
        st.sidebar.error(f"🚨 실시간 알림: {st.session_state.patient_status} 예약")

    if mode == "🏠 서비스 홈":
        st.markdown('<p class="main-title">AI Microbiome Clinical Suite</p>', unsafe_allow_html=True)
        st.markdown('<p class="sub-title">대장항문학 전문의를 위한 올인원 AI 플랫폼</p>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="service-card"><h3>🔍 01. Research Agent</h3><p>논문 분석 및 임상 가설 생성</p></div>', unsafe_allow_html=True)
            st.markdown('<div class="service-card"><h3>📸 03. Anonymous Pre-check</h3><p>항문질환/식단 익명 비전 예진 서비스</p></div>', unsafe_allow_html=True)
            st.markdown('<div class="service-card"><h3>🔬 05. Endoscopy AI</h3><p>올림푸스 NBI 최적화 정밀 판별 보조</p></div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="service-card"><h3>📊 02. Insight Report</h3><p>NGS 시각화 및 종이 검진지 OCR 분석</p></div>', unsafe_allow_html=True)
            st.markdown('<div class="service-card"><h3>🚨 04. Care Monitor</h3><p>24/7 AI 이상 징후 실시간 탐지</p></div>', unsafe_allow_html=True)

    elif mode == "🔍 01. 연구 에이전트 (RAG)":
        st.header("🔍 AI Research Agent (RAG)")
        uploaded_files = st.file_uploader("PDF 논문 업로드", type=['pdf'], accept_multiple_files=True)
        if uploaded_files:
            context_text = get_pdf_text(uploaded_files)
            user_query = st.text_input("분석 질문 입력", placeholder="예: 이 논문의 핵심 결론을 요약해줘")
            if user_query:
                try:
                    with st.spinner("논문을 분석하여 답변을 생성 중입니다..."):
                        model = genai.GenerativeModel('models/gemini-2.5-flash')
                        response = model.generate_content(f"의학 연구원으로서 답변하세요:\n\n{context_text[:15000]}\n\n질문: {user_query}")
                        st.markdown("### 📝 분석 결과")
                        st.info(response.text)
                except Exception as e:
                    st.error(f"❌ 분석 중 오류: {e}")

    elif mode == "📊 02. 환자 리포트 (NGS/OCR)":
        st.header("📊 Clinical Data Analysis & OCR")
        tab1, tab2 = st.tabs(["📈 NGS 시각화", "📄 종이 검진지 OCR"])
        with tab1:
            st.subheader("🧬 마이크로바이옴 정밀 분석")
            up_ngs = st.file_uploader("NGS 데이터 업로드 (CSV, XLSX)", type=['csv', 'xlsx'])
            if up_ngs:
                st.success(f"✅ {up_ngs.name} 데이터 로드 완료")
                st.bar_chart(pd.DataFrame(np.random.rand(5, 1), index=['B1','B2','B3','B4','B5'], columns=['Distribution']))
            if st.button("📄 장내 미생물 정밀 분석 결과지 발행"):
                st.success("✅ 고해상도 프리미엄 리포트 생성 완료 (비급여 청구 대상)")
        with tab2:
            st.subheader("📄 종이 건강검진 결과지 OCR")
            up_ocr = st.file_uploader("이미지 업로드", type=['jpg', 'png', 'pdf'])
            if up_ocr:
                st.success("✅ OCR 분석 완료: 데이터가 환자 차트에 자동 연동되었습니다.")

    elif mode == "📸 03. 익명 비전 예진 (항문/식단)":
        st.header("📸 Anonymous Pre-diagnosis Vision Guide")
        st.markdown('<div class="security-banner">🔒 보안 안내: 모든 개인정보는 분석 즉시 파기됩니다.</div>', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("🍑 항문 질환 분석")
            up_anus = st.file_uploader("항문 증상 사진 업로드", type=['jpg','png','jpeg'], key="anus_up")
            if up_anus:
                st.image(up_anus, width=250)
            if st.button("🔍 치핵 단계 및 수술 여부 판별"):
                with st.spinner("Vision AI 판독 중..."):
                    time.sleep(1.5)
                st.error("### 📢 분석 결과: 내치핵 3도 (Grade 3)")
        
        with c2:
            st.subheader("🥗 식단 & 배변 분석")
            up_diet = st.file_uploader("식단 또는 배변 사진 업로드", type=['jpg','png','jpeg'], key="diet_up")
            if up_diet:
                st.image(up_diet, width=250)
            if st.button("🔍 장내 환경 예측 분석"):
                with st.spinner("영양/배변 데이터 분석 중..."):
                    time.sleep(1.5)
                st.info("**[분석 결과]** 고탄수화물 식이 감지. 식이섬유 증량이 필요합니다.")

        st.write("---")
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            if st.button("📲 예진 데이터 환자용 전송"):
                st.info("📨 환자의 휴대폰으로 예진 요약본 및 내원 권고 메시지가 전송되었습니다.")
        with col_v2:
            if st.button("🏥 원장님 정밀 판독 및 예약 연동"):
                st.balloons()
                st.success("📨 원장님 PC 진료 차트로 전송 완료!")

    elif mode == "🚨 04. 케어 모니터링":
        st.header("🚨 24/7 AI-driven Anomaly Detection")
        st.markdown("<div class='alert-card'><b>[K-104 환자]</b> 장폐색 의심 징후 감지</div>", unsafe_allow_html=True)
        
        # 가독성을 위해 그래프 주변 여백 살짝 확보
        st.write("") 
        st.line_chart(np.random.normal(36.5, 0.2, size=(24, 1)))
        
        # --- 그래프 아래 중앙 부분에 하드웨어 연동 안내 문구 추가 ---
        st.markdown("""
            <div class="hardware-info">
                저희 플랫폼은 특정 장비만 고집하지 않습니다. 표준 의료 데이터 규격(HL7/FHIR)을 준수하기 때문에, 병원에서 이미 사용 중인 모니터링 장비나 시중에 나온 검증된 웨어러블 기기들과 유연하게 연동됩니다. 원장님은 그저 화면에서 분석 결과만 확인하시면 됩니다.<br><br>
                현재 국내외 유명 웨어러블 기업들(예: 에이티센스, 스카이랩스 등)의 기기와 연동 테스트를 마쳤으며, 원장님이 선호하시는 장비가 있다면 맞춤형 커스터마이징도 가능합니다.
            </div>
            """, unsafe_allow_html=True)

    elif mode == "🔬 05. 내시경 AI 분석":
        st.header("🔬 Endoscopy AI Diagnostic Assistant")
        st.success("💎 **Olympus NBI 모드 특화 분석 엔진 탑재**")
        up_img = st.file_uploader("📸 내시경 이미지 업로드", type=['jpg', 'png'])
        if up_img:
            st.image(up_img, width=400)
        if up_img:
            if st.button("📝 내시경 정밀 판독 리포트 발행 (과금)"):
                st.success("📄 공식 AI 판독 보고서가 생성되었습니다.")

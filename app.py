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
    </style>
    """, unsafe_allow_html=True)

# 3. 사이드바 - 시연 모드 및 내비게이션
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2864/2864248.png", width=60)
    st.title("MisaTech AI")
    
    # [추가] 시연 모드 선택
    st.markdown("---")
    view_mode = st.radio(
        "🕹️ 시연 시나리오 선택", 
        ["👨‍⚕️ 원장님 (관리 모드)", "📱 환자 (모바일 예진)"],
        index=0
    )
    st.markdown("---")

    # 원장님 모드일 때만 메뉴 표시
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
    st.caption("AI-Powered Clinical Solution v1.9")

# 4. 메인 콘텐츠 로직

# [환자 모드 시연 화면]
if view_mode == "📱 환자 (모바일 예진)":
    st.header("📱 스마트 익명 예진 시스템")
    st.markdown('<div class="security-banner">🔒 보안 안내: 모든 개인정보는 AI 분석 후 즉시 파기됩니다.</div>', unsafe_allow_html=True)
    
    with st.container(border=True):
        st.subheader("📸 증상 사진 업로드")
        up_file = st.file_uploader("환부 사진 업로드 (익명)", type=['jpg','png','jpeg'])
        st.text_area("증상을 상세히 적어주시면 AI가 더 정확히 판단합니다.", placeholder="예: 배변 시 통증이 심하고 선홍색 피가 나옵니다.")
        
        if st.button("🚀 AI 분석 및 전문의 연결"):
            with st.spinner("AI가 증상을 분석 중입니다..."):
                time.sleep(2)
                # 시연용 상태 저장
                st.session_state.new_reservation = True
                st.session_state.patient_status = "치핵 3기 의심"
            
            st.error("### 📢 AI 판별 결과: 내치핵 3도 (Grade 3)")
            st.warning("🏥 **장앤항외과 원장님**께 데이터를 전송하고 우선 진료 예약을 진행하시겠습니까?")
            
            if st.button("📅 즉시 진료 예약하기"):
                st.balloons()
                st.success("🎉 예약 신청 완료! 원장님 화면으로 데이터가 안전하게 전송되었습니다.")

# [원장님 모드 시연 화면]
else:
    # 실시간 예약 알림 팝업 (환자 모드에서 예약 시 작동)
    if st.session_state.get('new_reservation'):
        st.toast(f"🚨 [신규 예약] {st.session_state.patient_status} 환자가 예약을 신청했습니다!", icon="🚨")
        st.sidebar.error(f"🚨 실시간 알림: {st.session_state.patient_status} 예약 발생")

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
            user_query = st.text_input("분석 질문 입력")
            if user_query:
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"{context_text[:10000]}\n\n질문: {user_query}")
                st.info(response.text)

    elif mode == "📊 02. 환자 리포트 (NGS/OCR)":
        st.header("📊 Clinical Data Analysis & OCR")
        tab1, tab2, tab3 = st.tabs(["📈 NGS 시각화", "🧬 FASTQ 원천 분석", "📄 종이 검진지 OCR"])
        
        with tab1:
            st.subheader("마이크로바이옴 분석 데이터 업로드")
            uploaded_sheet = st.file_uploader("CSV 또는 XLSX 시트 업로드", type=['csv', 'xlsx'])
            if uploaded_sheet:
                st.success("데이터 로딩 완료")
                chart_data = pd.DataFrame({'균주명': ['Bifidobacterium', 'Lactobacillus', 'Bacteroides', 'Harmful'], '비율(%)': [42, 18, 25, 15]})
                st.bar_chart(chart_data.set_index('균주명'))
                st.info("**AI 분석 소견:** 유익균 분포가 안정적입니다.")
                if st.button("📄 마이크로바이옴 정밀 결과지 발행"):
                    st.success("✅ 고해상도 리포트 생성 완료 (과금)")
        
        with tab2:
            st.subheader("Cloud-based FASTQ Pipeline")
            st.file_uploader("FASTQ 파일 업로드 (.fastq, .gz)", type=['fastq', 'gz'])
            if st.button("AI 시퀀싱 분석 대기열 추가"):
                st.success("✅ 분석 요청 완료! (대기번호: #2026-0012)")

        with tab3:
            st.subheader("📄 종이 건강검진 결과지 OCR 분석")
            uploaded_ocr = st.file_uploader("검진 결과지 이미지/PDF 업로드", type=['jpg', 'jpeg', 'png', 'pdf'])
            if uploaded_ocr:
                with st.spinner("OCR 엔진 가동 중..."):
                    time.sleep(2)
                    st.success("✅ OCR 분석 완료")
                    st.markdown("""
                    | 검사항목 | 결과값 | 상태 |
                    | :--- | :--- | :--- |
                    | 공복혈당 | 110 mg/dL | **주의** |
                    | AST/ALT | 45/52 U/L | **주의** |
                    """)

    elif mode == "📸 03. 익명 비전 예진 (항문/식단)":
        st.header("📸 Anonymous Pre-diagnosis Vision Guide")
        st.markdown('<div class="security-banner">🔒 보안 안내: 모든 개인정보는 분석 즉시 파기됩니다.</div>', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("🍑 항문 질환 분석 (치핵/치루)")
            st.file_uploader("환부 사진 업로드 (익명)", type=['jpg', 'png', 'jpeg'], key="anal_img")
            if st.button("치핵 단계 및 수술 여부 판별"):
                with st.spinner("AI 분석 중..."):
                    time.sleep(1.5)
                    st.error("### 📢 분석 결과: 내치핵 3도 (Grade 3)")
                    st.warning("🚩 **소견:** 원장님과 즉각적인 수술 상담을 권장합니다.")
        
        with c2:
            st.subheader("🥗 식단 & 배변 분석")
            st.file_uploader("식단/배변 사진 업로드", type=['jpg', 'png', 'jpeg'], key="food_img")
            if st.button("장내 환경 예측 분석"):
                st.info("**[분석 결과]** 고탄수화물 식이 비중이 높음.")

        st.write("---")
        col_vision1, col_vision2 = st.columns(2)
        with col_vision1:
            if st.button("📄 예진 결과 요약지 발행"):
                st.success("✅ 환자용 예진 리포트 생성 완료")
        with col_vision2:
            if st.button("🏥 원장님 정밀 판독 및 예약 연동"):
                st.balloons()
                st.info("📨 원장님 PC로 환자 데이터 전송 완료.")

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
        st.success("💎 **Olympus(올림푸스) 고해상도 이미지 및 NBI 모드 특화 엔진**")
        
        tab_img, tab_vid = st.tabs(["📸 이미지 정밀 분석", "🎥 동영상 분석"])

        with tab_img:
            up_img = st.file_uploader("이미지 업로드", type=['jpg', 'jpeg', 'png'], key="endos_img")
            if up_img:
                col_img, col_res = st.columns(2)
                with col_img: st.image(up_img, use_container_width=True)
                with col_res:
                    if st.button("🔍 AI 이미지 정밀 분석 실행"):
                        with st.spinner("패턴 분석 중..."):
                            time.sleep(1.5)
                            st.error("### 📢 분석 결과: 암 변질 의심")
                    
                    st.write("---")
                    if st.button("📝 이미지 판독 리포트 발행 (과금)", key="btn_img_report"):
                        report_time = time.strftime("%Y-%m-%d %H:%M:%S")
                        report_html = f"""
                        <div style="border: 2px solid #1E3A8A; padding: 25px; border-radius: 12px; background-color: #ffffff;">
                            <h2 style="color: #1E3A8A; text-align: center;">AI 정밀 판독 결과 보고서 (Image)</h2>
                            <p><b>■ 판독 대상:</b> {up_img.name}</p>
                            <p><b>■ AI 추정:</b> <span style="color:red;">선종성 용종 (Adenoma)</span></p>
                            <p><b>■ 신뢰도:</b> 91.0%</p>
                        </div>
                        """
                        st.markdown(report_html, unsafe_allow_html=True)

        with tab_vid:
            up_vid = st.file_uploader("영상 업로드", type=['mp4', 'avi', 'mov'], key="endos_vid")
            if up_vid:
                col_v, col_v_res = st.columns(2)
                with col_v: st.video(up_vid)
                with col_v_res:
                    if st.button("🚀 AI 동영상 분석 시작"):
                        st.warning("⚠️ 12초 지점 이상 패턴 감지")
                    
                    st.write("---")
                    if st.button("📝 영상 판독 리포트 발행 (과금)", key="btn_vid_report"):
                        st.success("✅ 영상 분석 리포트 생성 완료")

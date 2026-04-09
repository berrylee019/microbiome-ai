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

# 3. 사이드바 내비게이션
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2864/2864248.png", width=60)
    st.title("MisaTech AI")
    st.markdown("---")
    mode = st.radio("서비스 모드 선택", [
        "🏠 서비스 홈", 
        "🔍 01. 연구 에이전트 (RAG)", 
        "📊 02. 환자 리포트 (NGS/OCR)", 
        "📸 03. 익명 비전 예진 (항문/식단)", 
        "🚨 04. 케어 모니터링",
        "🔬 05. 내시경 AI 분석"
    ])
    st.markdown("---")
    st.caption("AI-Powered Clinical Solution v1.9")

# 4. 메인 콘텐츠
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
    
    with tab2:
        st.subheader("Cloud-based FASTQ Pipeline")
        st.file_uploader("FASTQ 파일 업로드 (.fastq, .gz)", type=['fastq', 'gz'])
        if st.button("AI 시퀀싱 분석 대기열 추가"):
            st.success("✅ 분석 요청 완료! (대기번호: #2026-0012)")

    with tab3:
        st.subheader("📄 종이 건강검진 결과지 OCR 분석")
        st.write("외부 병원에서 받은 종이 결과지를 촬영하여 업로드하면 AI가 핵심 지표를 추출합니다.")
        uploaded_ocr = st.file_uploader("검진 결과지 이미지/PDF 업로드", type=['jpg', 'jpeg', 'png', 'pdf'])
        if uploaded_ocr:
            with st.spinner("OCR 엔진 가동 중..."):
                time.sleep(2)
                st.success("✅ OCR 분석 완료")
                st.markdown("""
                | 검사항목 | 결과값 | 상태 |
                | :--- | :--- | :--- |
                | 공복혈당 | 110 mg/dL | **주의(공복혈당장애 의심)** |
                | AST/ALT | 45/52 U/L | **주의(경미한 수치 상승)** |
                | 대장내시경 소견 | 용종 절제 2건 | 정기 추적 관찰 필요 |
                """)
                st.info("💡 **AI 가이드:** 간수치 개선을 위한 식단 조절과 6개월 후 재검사가 권장됩니다.")

elif mode == "📸 03. 익명 비전 예진 (항문/식단)":
    st.header("📸 Anonymous Pre-diagnosis Vision Guide")
    
    # 강력한 보안 문구 반영
    st.markdown('<div class="security-banner">🔒 보안 안내: 모든 개인정보 및 사진은 AI 분석 즉시 파기되며 서버에 저장되지 않습니다. (익명 예진 서비스)</div>', unsafe_allow_html=True)
    
    st.write("병원 방문 전, AI를 통해 상태를 미리 확인하는 비대면 익명 예진 모듈입니다.")
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("🍑 항문 질환 분석 (치핵/치루)")
        st.file_uploader("환부 사진 업로드 (익명)", type=['jpg', 'png', 'jpeg'], key="anal_img")
        if st.button("치핵 단계 및 수술 여부 판별"):
            with st.spinner("AI가 병변을 분석 중입니다..."):
                time.sleep(1.5)
                st.error("### 📢 분석 결과: 내치핵 3도 (Grade 3)")
                st.warning("🚩 **소견:** 탈출된 치핵이 손으로 밀어넣어야 들어가는 상태로 관찰됩니다. **'감돈 치핵'** 위험이 있으므로 원장님과 수술 상담을 권장합니다.")
    
    with c2:
        st.subheader("🥗 식단 & 배변 분석")
        st.file_uploader("식단/배변 사진 업로드", type=['jpg', 'png', 'jpeg'], key="food_img")
        if st.button("장내 환경 예측 분석"):
            st.info("**[분석 결과]** 브리스톨 척도 4단계 유지 중이나, 고탄수화물 식이 비중이 높아 식이섬유 증량이 필요합니다.")

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
    
    # 올림푸스 NBI 특화 문구 반영
    st.success("💎 **Olympus(올림푸스) 고해상도 이미지 및 NBI(Narrow Band Imaging) 모드 특화 분석 엔진 탑재**")
    
    st.write("내시경 영상/이미지를 분석하여 용종의 종류 및 암 변질 여부를 감별 진단합니다.")
    st.info("💡 본 모듈은 원장님의 판독을 보조하기 위한 의사결정 지원 시스템(DSS)입니다.")
    
# 이미지와 영상 업로드 탭 분리
    tab_img, tab_vid = st.tabs(["📸 이미지 분석", "🎥 동영상 분석"])

    with tab_img:
        up_img = st.file_uploader("내시경 캡처 이미지 업로드", type=['jpg', 'jpeg', 'png'], key="endos_img")
        if up_img:
            col_img, col_res = st.columns(2)
            with col_img:
                st.image(up_img, caption="분석 대상 이미지", use_container_width=True)
            with col_res:
                if st.button("AI 이미지 정밀 분석 실행"):
                    with st.spinner("이미지 패턴 및 혈관 분포 분석 중..."):
                        time.sleep(2)
                        st.error("### 📢 분석 결과: 암 변질 의심 (Malignancy Risk High)")
                        st.markdown("- **병변 유형:** 선종성 용종 (Adenoma)\n- **악성 가능성:** 91%\n- **주요 소견:** 불규칙한 미세 혈관 패턴 및 표면 질감 파괴 징후 포착.")
                        st.progress(91)

    with tab_vid:
        st.subheader("🎥 내시경 동영상 실시간 패턴 분석")
        up_vid = st.file_uploader("내시경 영상 파일 업로드 (MP4, AVI, MOV)", type=['mp4', 'avi', 'mov'], key="endos_vid")
        
        if up_vid:
            col_v, col_v_res = st.columns([1.5, 1])
            with col_v:
                st.video(up_vid)
            with col_v_res:
                if st.button("AI 동영상 프레임 분석 시작"):
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # 영상 프레임 분석 시뮬레이션
                    for i in range(1, 101):
                        time.sleep(0.05) # 시연용 속도
                        progress_bar.progress(i)
                        if i < 30: status_text.text(f"프레임 추출 중... {i}%")
                        elif i < 70: status_text.text(f"NBI 혈관 패턴 대조 중... {i}%")
                        else: status_text.text(f"이상 징후 구간(Timestamp) 특정 중... {i}%")
                    
                    st.success("✅ 영상 분석 완료")
                    st.markdown("""
                    **[영상 분석 요약 보고서]**
                    - **특이 구간 검출:** 00:12 ~ 00:15 (용종 의심)
                    - **병변 유형:** 무경성 톱니바퀴 모양 용종 (SSA/P) 의심
                    - **권고 사항:** 해당 구간 정지 화면(Freeze frame) 정밀 판독 후 절제 권장
                    """)
                    st.warning("⚠️ 원장님, 12초 지점의 혈관 확장 패턴을 확인해 주십시오.")
                    
# --- 리포트 발행 및 과금 섹션 시작 ---
        st.write("---")
        col_rpt1, col_rpt2 = st.columns([2, 1])
        
        with col_rpt1:
            st.markdown("#### 📄 정밀 판독 리포트 발행")
            st.caption("환자 상담 및 차트 보관용 고해상도 리포트를 생성합니다.")
        
        with col_rpt2:
            # 리포트 발행 버튼 (모델 2: 건당 과금의 트리거)
            if st.button("📝 리포트 발행 (3,000원)"):
                # 1. 과금 로그 시뮬레이션 (세션 상태를 활용해 중복 과금 방지)
                if 'report_count' not in st.session_state:
                    st.session_state.report_count = 0
                
                # 시연용: 동일 환자/영상에 대해 재클릭 시 과금 제외 로직 언급
                st.session_state.report_count += 1
                
                # 2. 리포트 생성 시간 및 데이터
                report_time = time.strftime("%Y-%m-%d %H:%M:%S")
                
                st.toast("리포트가 생성되었습니다. (월말 정산 내역에 포함됩니다)")
                
                # 3. 리포트 UI (HTML)
                report_html = f"""
                <div style="border: 2px solid #1E3A8A; padding: 25px; border-radius: 12px; background-color: #ffffff; box-shadow: 2px 2px 12px rgba(0,0,0,0.1);">
                    <div style="text-align: center; border-bottom: 2px solid #1E3A8A; padding-bottom: 10px;">
                        <h2 style="color: #1E3A8A; margin: 0;">AI 정밀 판독 결과 보고서</h2>
                        <span style="font-size: 12px; color: #666;">장앤항외과 X MisaTech AI 협력 모델</span>
                    </div>
                    <div style="margin-top: 20px;">
                        <p><b>■ 분석 일시:</b> {report_time}</p>
                        <p><b>■ 판독 대상:</b> 내시경 영상 스트림 (Timestamp 00:12~00:18)</p>
                        <p><b>■ AI 추정 병변:</b> <span style="color: #D32F2F; font-weight: bold;">무경성 톱니바퀴 모양 용종 (SSA/P)</span></p>
                        <p><b>■ 판독 신뢰도:</b> <span style="color: #1E3A8A; font-weight: bold;">94.5%</span></p>
                        <p><b>■ 종합 소견:</b> NBI 모드 분석 결과, 확장된 은와(crypt)와 불규칙한 미세혈관 패턴이 관찰되어 SSA/P 가능성이 매우 높음. 선종성 용종 대비 발견이 어려우나 암 변질 위험이 있으므로 즉시 절제를 권장함.</p>
                    </div>
                    <div style="margin-top: 30px; text-align: center; font-size: 11px; color: #888;">
                        본 리포트는 의사결정 보조용이며, 최종 진단 책임은 전문의에게 있습니다.
                    </div>
                </div>
                """
                st.markdown(report_html, unsafe_allow_html=True)
                
                # 4. PDF 저장 버튼 (SaaS 모델의 결과물 제공)
                st.download_button(
                    label="📥 리포트 PDF/HTML 다운로드",
                    data=report_html,
                    file_name=f"JangAndHang_AI_Report_{time.strftime('%H%M%S')}.html",
                    mime="text/html",
                    help="다운로드 후 파일을 열어 '인쇄(PDF로 저장)'를 선택하세요."
                )

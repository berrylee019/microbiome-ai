import streamlit as st

# 1. 페이지 설정: 레이아웃을 넓게 쓰고 메뉴바를 깔끔하게 유지
st.set_page_config(
    page_title="AI Microbiome Suite",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. 고도화된 커스텀 디자인 (CSS)
st.markdown("""
    <style>
    /* 메인 타이틀 및 서브타이틀 중앙 정렬 */
    .header-container {
        text-align: center;
        padding: 30px 0px;
    }
    .main-title {
        font-size: 50px;
        font-weight: 800;
        color: #1E3A8A;
        margin-bottom: 10px;
    }
    .sub-title {
        font-size: 20px;
        color: #6B7280;
        margin-bottom: 50px;
    }
    
    /* 서비스 카드 스타일 */
    .stMarkdown div[data-testid="stVerticalBlock"] > div:has(div.service-card) {
        background: transparent;
    }
    .service-card {
        background-color: #FFFFFF;
        padding: 25px;
        border-radius: 20px;
        border: 1px solid #E5E7EB;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s;
        height: 280px;
        margin-bottom: 25px;
    }
    .service-card:hover {
        transform: translateY(-5px);
        border-color: #3B82F6;
    }
    .card-icon { font-size: 30px; margin-bottom: 15px; }
    .card-title { font-size: 22px; font-weight: 700; color: #111827; }
    .card-tech { font-size: 14px; font-weight: 600; color: #3B82F6; margin-top: 5px; }
    .card-desc { font-size: 15px; color: #4B5563; margin-top: 15px; line-height: 1.6; }
    
    /* 구분선 스타일 */
    hr { margin: 40px 0; border: 0; border-top: 1px solid #E5E7EB; }
    </style>
    """, unsafe_allow_html=True)

# 3. 사이드바 구성
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2864/2864248.png", width=80) # 의료/AI 상징 아이콘
    st.title("Admin Panel")
    st.markdown("---")
    mode = st.radio(
        "사용 모드 선택",
        ["🏠 서비스 홈", "🔍 연구 에이전트", "📊 환자 리포트", "📸 비전 분석", "🚨 모니터링"]
    )
    st.markdown("---")
    st.caption("v1.0.0 | Contact: MisaTech")

# 4. 메인 화면 로직
if mode == "🏠 서비스 홈":
    # 헤더 섹션
    st.markdown("""
        <div class="header-container">
            <p class="main-title">AI Microbiome Clinical Suite</p>
            <p class="sub-title">대장항문학 임상 현장의 니즈와 AI 에이전트 기술의 완벽한 융합</p>
        </div>
    """, unsafe_allow_html=True)

    # 서비스 카드 섹션 (중앙 정렬을 위해 컬럼 배치)
    _, center_col, _ = st.columns([0.5, 9, 0.5])
    
    with center_col:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
                <div class="service-card">
                    <div class="card-icon">🔍</div>
                    <div class="card-title">01. AI Research Agent</div>
                    <div class="card-tech">RAG & LLM Hypothesis Generation</div>
                    <div class="card-desc">방대한 마이크로바이옴 연구 문헌을 실시간 분석하여 최적의 연구 가설을 도출하고 초록을 요약합니다.</div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
                <div class="service-card">
                    <div class="card-icon">📸</div>
                    <div class="card-title">03. Microbiome Vision Guide</div>
                    <div class="card-tech">Computer Vision & Pattern Matching</div>
                    <div class="card-desc">식단과 배변 사진의 시각 데이터를 분석하여 장내 미생물 군집 변화와의 과학적 상관관계를 입증합니다.</div>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
                <div class="service-card">
                    <div class="card-icon">📊</div>
                    <div class="card-title">02. Patient Insight Report</div>
                    <div class="card-tech">Natural Language Generation (NLG)</div>
                    <div class="card-desc">난해한 NGS 원천 데이터를 환자가 이해하기 쉬운 언어로 변환하여 고도화된 개인별 맞춤 리포트를 생성합니다.</div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
                <div class="service-card">
                    <div class="card-icon">🚨</div>
                    <div class="card-title">04. Clinical Care Monitor</div>
                    <div class="card-tech">Predictive Analytics & Real-time Alert</div>
                    <div class="card-desc">수술 후 환자의 건강 데이터를 실시간 추적하여 이상 징후를 예측하고 의료진에게 즉각적인 경고를 전송합니다.</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.info("💡 **제안 방향:** 임상 데이터의 자산화를 통해 병원의 연구 경쟁력과 환자 케어 품질을 동시에 확보합니다.")

# --- 개별 상세 페이지 (간략 구성) ---
elif mode == "🔍 연구 에이전트":
    st.header("🔍 AI Research Agent")
    st.text_input("연구 키워드를 입력하세요", placeholder="예: Colon Cancer and Gut-Brain Axis")
    st.button("연구 데이터 분석 시작")

elif mode == "📊 환자 리포트":
    st.header("📊 Patient Insight Report")
    st.file_uploader("검사 결과 파일 업로드 (CSV, JSON)")
    st.button("AI 리포트 생성")

elif mode == "📸 비전 분석":
    st.header("📸 Microbiome Vision Guide")
    st.camera_input("이미지 촬영 또는 업로드")
    st.button("시각 데이터 분석")

elif mode == "🚨 모니터링":
    st.header("🚨 Clinical Care Monitor")
    st.warning("현재 모니터링 중인 환자: 12명 (이상 징후 발생: 1명)")
    st.line_chart([2, 3, 1, 5, 2, 4])

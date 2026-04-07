import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

# 1. 페이지 설정 및 보안 설정
st.set_page_config(
    page_title="AI Microbiome Suite",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Gemini API 설정 (Streamlit Secrets 활용)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.warning("⚠️ 사이드바 하단 혹은 Advanced Settings에서 API Key를 설정해주세요.")

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

# 2. 커스텀 CSS (중앙 정렬 및 카드 스타일)
st.markdown("""
    <style>
    .header-container { text-align: center; padding: 30px 0px; }
    .main-title { font-size: 48px; font-weight: 800; color: #1E3A8A; margin-bottom: 10px; }
    .sub-title { font-size: 20px; color: #6B7280; margin-bottom: 50px; }
    .service-card {
        background-color: #FFFFFF;
        padding: 25px;
        border-radius: 18px;
        border: 1px solid #E5E7EB;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        height: 280px;
        margin-bottom: 25px;
        transition: all 0.3s ease;
    }
    .service-card:hover { transform: translateY(-5px); border-color: #3B82F6; box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1); }
    .card-icon { font-size: 32px; margin-bottom: 15px; }
    .card-title { font-size: 22px; font-weight: 700; color: #111827; }
    .card-tech { font-size: 14px; font-weight: 600; color: #3B82F6; margin-top: 5px; }
    .card-desc { font-size: 15px; color: #4B5563; margin-top: 15px; line-height: 1.6; }
    hr { margin: 40px 0; border: 0; border-top: 1px solid #E5E7EB; }
    </style>
    """, unsafe_allow_html=True)

# 3. 사이드바 내비게이션
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2864/2864248.png", width=70)
    st.title("MisaTech AI")
    st.markdown("---")
    mode = st.radio(
        "서비스 모드 선택",
        ["🏠 서비스 홈", "🔍 01. 연구 에이전트 (RAG)", "📊 02. 환자 리포트", "📸 03. 비전 분석", "🚨 04. 케어 모니터링"]
    )
    st.markdown("---")
    # API 키 수동 입력창 (테스트용)
    if "GEMINI_API_KEY" not in st.secrets:
        user_api_key = st.text_input("Gemini API Key 입력", type="password")
        if user_api_key:
            genai.configure(api_key=user_api_key)

# 4. 메인 콘텐츠 제어
if mode == "🏠 서비스 홈":
    st.markdown("""
        <div class="header-container">
            <p class="main-title">AI Microbiome Clinical Suite</p>
            <p class="sub-title">대장항문학 전문의를 위한 지능형 임상 및 연구 지원 플랫폼</p>
        </div>
    """, unsafe_allow_html=True)

    _, center_col, _ = st.columns([1, 10, 1])
    
    with center_col:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""<div class="service-card"><div class="card-icon">🔍</div><div class="card-title">01. AI Research Agent</div><div class="card-tech">RAG & Knowledge Analysis</div><div class="card-desc">방대한 논문 데이터를 실시간 학습하여 교수님의 연구 주제에 최적화된 인사이트와 가설을 도출합니다.</div></div>""", unsafe_allow_html=True)
            st.markdown("""<div class="service-card"><div class="card-icon">📸</div><div class="card-title">03. Microbiome Vision Guide</div><div class="card-tech">Computer Vision Analysis</div><div class="card-desc">환자의 식단과 배변 상태를 시각적으로 분석하여 장내 미생물 환경과의 인과관계를 데이터화합니다.</div></div>""", unsafe_allow_html=True)
        with col2:
            st.markdown("""<div class="service-card"><div class="card-icon">📊</div><div class="card-title">02. Patient Insight Report</div><div class="card-tech">GenAI Report Generation</div><div class="card-desc">난해한 분석 원천 데이터를 환자 맞춤형 언어로 자동 변환하여 정밀 의료 기반의 소통을 지원합니다.</div></div>""", unsafe_allow_html=True)
            st.markdown("""<div class="service-card"><div class="card-icon">🚨</div><div class="card-title">04. Clinical Care Monitor</div><div class="card-tech">Predictive Alert System</div><div class="card-desc">수술 후 환자의 상태를 실시간 추적하여 이상 징후 발생 시 의료진에게 즉각적인 알림을 제공합니다.</div></div>""", unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.info("💡 **제안 핵심:** 본 플랫폼은 의료진의 연구 시간을 단축하고, 데이터 기반의 정밀 진단을 가능하게 함으로써 임상 자산의 가치를 극대화합니다.")

elif mode == "🔍 01. 연구 에이전트 (RAG)":
    st.header("🔍 AI Research Agent (RAG Demo)")
    st.write("교수님의 최신 논문이나 연구 자료(PDF)를 업로드하고 AI와 대화해 보세요.")
    
    uploaded_files = st.file_uploader("PDF 논문 업로드", type=['pdf'], accept_multiple_files=True)
    
    if uploaded_files:
        with st.spinner("논문 내용을 분석 중입니다..."):
            context_text = get_pdf_text(uploaded_files)
            st.success(f"분석 완료! (총 {len(uploaded_files)}개의 파일)")
        
        user_query = st.text_input("질문을 입력하세요 (예: 이 논문에서 강조하는 유익균의 역할은?)")
        
        if user_query:
            with st.spinner("AI가 답변을 생성 중입니다..."):
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = f"당신은 마이크로바이옴 전문 연구 조수입니다. 다음 제공된 논문 텍스트를 바탕으로 답변하세요. 논문에 없는 내용은 답변하지 마세요.\n\n[Context]\n{context_text[:12000]}\n\n[Question]\n{user_query}"
                response = model.generate_content(prompt)
                st.markdown("### 🤖 연구 에이전트 답변")
                st.info(response.text)

elif mode == "📊 02. 환자 리포트":
    st.header("📊 Patient Insight Report")
    st.write("데이터 시각화 및 자동 리포트 생성 예시입니다.")
    st.file_uploader("NGS 데이터 업로드", type=['csv', 'xlsx'])
    col_a, col_b = st.columns(2)
    col_a.bar_chart({"Bifidobacterium": 45, "Lactobacillus": 30, "Others": 25})
    col_b.write("**AI 소견:** 해당 환자는 유익균 비율이 정상 범위보다 낮으며, 식이섬유 강화 식단 제안이 필요합니다.")

elif mode == "📸 03. 비전 분석":
    st.header("📸 Microbiome Vision Guide")
    st.write("식단 및 배변 사진 분석 모듈 (PoC)")
    st.camera_input("분석용 사진 촬영")
    st.button("이미지 패턴 분석 실행")

elif mode == "🚨 04. 케어 모니터링":
    st.header("🚨 Clinical Care Monitor")
    st.write("환자 사후 관리 대시보드")
    st.metric(label="주의 필요 환자", value="2 명", delta="1 명 증가")
    st.line_chart([10, 15, 12, 18, 25, 20])

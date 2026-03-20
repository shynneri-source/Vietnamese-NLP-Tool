"""
Vietnamese NLP Streamlit Application
Features: Tokenization, POS Tagging, Color Highlighting, CSV Export
"""

import streamlit as st
import pandas as pd
from underthesea import word_tokenize, pos_tag


# Page configuration
st.set_page_config(
    page_title="Vietnamese NLP Tool",
    page_icon="🇻🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
<style>
    /* Force light theme */
    [data-testid="stAppViewContainer"] {
        background-color: #f8fafc;
    }
    
    /* Hide default header */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Root variables */
    :root {
        --primary-gradient: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #d946ef 100%);
        --secondary-gradient: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        --card-bg: #ffffff;
        --text-primary: #1e293b;
        --text-secondary: #64748b;
        --border-color: #e2e8f0;
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
    }
    
    /* Main container */
    .main > div {
        padding: 1rem 2rem 2rem 2rem;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    /* Header styling */
    .app-header {
        background: var(--primary-gradient);
        padding: 2.5rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: var(--shadow-xl);
        position: relative;
        overflow: hidden;
    }
    .app-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: pulse 4s ease-in-out infinite;
    }
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    .app-header h1 {
        color: white !important;
        margin: 0;
        font-size: 2.8rem;
        font-weight: 800;
        position: relative;
        z-index: 1;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    .app-header p {
        opacity: 0.95;
        margin-top: 0.75rem;
        font-size: 1.1rem;
        position: relative;
        z-index: 1;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.4rem;
        font-weight: 700;
        color: #1e293b !important;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .section-header::before {
        content: '';
        width: 4px;
        height: 28px;
        background: var(--primary-gradient);
        border-radius: 2px;
    }
    
    /* Card styling */
    .result-card {
        background: var(--card-bg);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: var(--shadow-md);
        margin-bottom: 1rem;
        border: 1px solid var(--border-color);
        transition: box-shadow 0.3s ease;
    }
    .result-card:hover {
        box-shadow: var(--shadow-lg);
    }
    
    /* Stats cards */
    .stat-card {
        background: var(--card-bg);
        padding: 1.5rem;
        border-radius: 16px;
        text-align: center;
        box-shadow: var(--shadow-md);
        border: 1px solid var(--border-color);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .stat-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--primary-gradient);
    }
    .stat-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-xl);
    }
    .stat-number {
        font-size: 2.5rem;
        font-weight: 800;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .stat-label {
        font-size: 0.9rem;
        color: var(--text-secondary);
        margin-top: 0.5rem;
        font-weight: 500;
    }
    
    /* Input area styling */
    .stTextArea > label {
        font-weight: 600;
        color: var(--text-primary);
        font-size: 1.1rem;
    }
    .stTextArea textarea {
        border-radius: 12px;
        border: 2px solid var(--border-color);
        transition: all 0.3s ease;
        font-size: 1rem;
        color: #1e293b !important;
    }
    .stTextArea textarea:focus {
        border-color: #8b5cf6;
        box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.1);
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: #f1f5f9;
        padding: 0.5rem;
        border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        color: #475569 !important;
        transition: all 0.2s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background: white;
        box-shadow: var(--shadow-sm);
    }
    .stTabs [aria-selected="true"] {
        background: var(--primary-gradient);
        color: white !important;
        border: none;
    }
    
    /* Token highlight styling */
    .token-highlight {
        padding: 8px 14px;
        border-radius: 10px;
        margin: 4px;
        display: inline-block;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.2s ease;
        cursor: pointer;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .token-highlight:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    /* Dataframe styling */
    .dataframe {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: var(--shadow-sm);
        background: white;
    }
    .dataframe th {
        background: #f8fafc;
        font-weight: 600;
        color: var(--text-primary);
        padding: 1rem;
    }
    .dataframe td {
        padding: 0.75rem 1rem;
        color: #1e293b !important;
    }
    
    /* Download button */
    .stDownloadButton > button {
        background: var(--primary-gradient);
        color: white !important;
        border: none;
        padding: 0.875rem 2rem;
        border-radius: 12px;
        font-weight: 700;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: var(--shadow-md);
    }
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
        opacity: 0.95;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
    }
    section[data-testid="stSidebar"] * {
        color: #1e293b !important;
    }
    .sidebar-content {
        padding: 1.5rem;
    }
    .sidebar-card {
        background: #f8fafc;
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        border: 1px solid var(--border-color);
    }
    
    /* Color chip */
    .color-chip {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin: 3px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.15);
        transition: all 0.2s ease;
    }
    .color-chip:hover {
        transform: scale(1.05);
    }
    
    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border-left: 4px solid #3b82f6;
        padding: 1rem 1.25rem;
        border-radius: 8px;
        margin: 1rem 0;
        color: #1e40af !important;
    }
    
    /* Markdown text color */
    .stMarkdown, .stMarkdown p, .stMarkdown li {
        color: #1e293b !important;
    }
    
    /* JSON display */
    .stJson {
        background: white;
        border-radius: 12px;
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Bảng giải thích nhãn từ loại
POS_TAGS_EXPLANATION = {
    "N": "Danh từ",
    "Np": "Danh từ riêng",
    "Nc": "Danh từ chỉ loại",
    "Nu": "Danh từ đơn vị",
    "V": "Động từ",
    "A": "Tính từ",
    "P": "Đại từ",
    "R": "Phó từ",
    "L": "Định từ",
    "M": "Số từ",
    "E": "Giới từ",
    "C": "Liên từ",
    "I": "Thán từ",
    "T": "Trợ từ, tiểu từ",
    "B": "Từ gốc Hán-Việt",
    "Y": "Từ viết tắt",
    "S": "Từ ngoại lai",
    "X": "Từ không phân loại",
    "CH": "Dấu câu",
}

# Màu cho từng loại từ loại (modern pastel palette)
POS_COLORS = {
    "N": "#f43f5e",      # Rose
    "Np": "#e11d48",     # Rose Dark
    "Nc": "#fb7185",     # Rose Light
    "Nu": "#fda4af",     # Rose Lighter
    "V": "#06b6d4",      # Cyan
    "A": "#fbbf24",      # Amber
    "P": "#10b981",      # Emerald
    "R": "#34d399",      # Emerald Light
    "L": "#a78bfa",      # Violet
    "M": "#0ea5e9",      # Sky
    "E": "#f97316",      # Orange
    "C": "#14b8a6",      # Teal
    "I": "#eab308",      # Yellow
    "T": "#d946ef",      # Fuchsia
    "B": "#fb923c",      # Orange Light
    "Y": "#60a5fa",      # Blue Light
    "S": "#f87171",      # Red Light
    "X": "#94a3b8",      # Slate
    "CH": "#64748b",     # Slate Dark
}


def tokenize_text(text: str) -> list[str]:
    """Task 1: Tokenize Vietnamese text using underthesea"""
    return word_tokenize(text)


def tag_pos(text: str) -> list[tuple[str, str]]:
    """Task 2: POS tagging for tokens using underthesea"""
    return pos_tag(text)


def generate_highlighted_html(tagged_tokens: list[tuple[str, str]]) -> str:
    """Task 6: Generate HTML with color highlighting for each POS tag"""
    html_parts = []
    for token, pos in tagged_tokens:
        color = POS_COLORS.get(pos, "#94a3b8")
        description = POS_TAGS_EXPLANATION.get(pos, pos)
        html_parts.append(
            f'<span class="token-highlight" '
            f'style="background-color: {color}; color: white;" '
            f'title="{description}">{token}</span>'
        )
    return " ".join(html_parts)


def create_pos_table() -> pd.DataFrame:
    """Task 3: Create POS tags explanation table"""
    data = {
        "Tag": list(POS_TAGS_EXPLANATION.keys()),
        "Description": list(POS_TAGS_EXPLANATION.values()),
        "Color": [POS_COLORS.get(tag, "#94a3b8") for tag in POS_TAGS_EXPLANATION.keys()],
    }
    return pd.DataFrame(data)


def create_export_dataframe(tagged_tokens: list[tuple[str, str]]) -> pd.DataFrame:
    """Task 5: Create DataFrame for CSV export"""
    data = {
        "Token": [token for token, _ in tagged_tokens],
        "POS Tag": [pos for _, pos in tagged_tokens],
        "Description": [
            POS_TAGS_EXPLANATION.get(pos, "Không xác định") for _, pos in tagged_tokens
        ],
    }
    return pd.DataFrame(data)


def convert_df_to_csv(df: pd.DataFrame) -> bytes:
    """Convert DataFrame to CSV format for download"""
    return df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8")


def main():
    # Header
    st.markdown("""
        <div class="app-header">
            <h1>🇻🇳 Vietnamese NLP Tool</h1>
            <p>Ứng dụng xử lý ngôn ngữ tiếng Việt</p>
        </div>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown("### 🎯 Tính năng")
        st.markdown("""
        - **Tokenize:** Tách từ tiếng Việt
        - **POS Tagging:** Gán nhãn từ loại
        - **Highlight màu:** Hiển thị trực quan
        - **Export CSV:** Tải kết quả
        """)
        
        st.divider()
        st.markdown("### 📖 Hướng dẫn")
        st.info("💡 Di chuột vào từ đã tô màu để xem nhãn từ loại")
        
        st.divider()
        st.markdown("### 👤 Sinh viên")
        st.markdown("**MSSV:** 123000218")
        st.markdown("**Tên:** Phước")

    # Input section
    st.markdown('<p class="section-header">Nhập văn bản</p>', unsafe_allow_html=True)
    input_text = st.text_area(
        label="Nhập văn bản tiếng Việt cần xử lý:",
        height=120,
        placeholder="Ví dụ: Tôi yêu Việt Nam. Đây là một đất nước tươi đẹp với bề dày lịch sử.",
        label_visibility="collapsed"
    )

    # Task 4: Error handling for empty input
    if not input_text or not input_text.strip():
        st.info("💡 Vui lòng nhập văn bản để xử lý!")
        return

    # Process the text
    with st.spinner("🔄 Đang xử lý..."):
        tokens = tokenize_text(input_text)
        tagged_tokens = tag_pos(input_text)

    # Stats row
    st.divider()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{len(tokens)}</div>
                <div class="stat-label">Tổng số từ</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        unique_pos = len(set(pos for _, pos in tagged_tokens))
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{unique_pos}</div>
                <div class="stat-label">Loại từ khác nhau</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{len(input_text)}</div>
                <div class="stat-label">Số ký tự</div>
            </div>
        """, unsafe_allow_html=True)

    # Results section
    st.divider()
    st.markdown('<p class="section-header">Kết quả xử lý</p>', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["🎨 Highlight Màu", "🔤 Tokenize", "🏷️ POS Tagging"])

    with tab1:
        st.info("💡 **Mẹo:** Di chuột vào từng từ để xem nhãn từ loại")
        highlighted_html = generate_highlighted_html(tagged_tokens)
        st.markdown(
            f'<div style="font-size: 18px; line-height: 3; padding: 24px; '
            f'background: linear-gradient(135deg, #fafafa 0%, #f5f5f5 100%); '
            f'border-radius: 16px; border: 1px solid #e5e5e5;">{highlighted_html}</div>',
            unsafe_allow_html=True,
        )

    with tab2:
        st.markdown("### Danh sách các từ (Tokenize)")
        st.json(tokens)

    with tab3:
        st.markdown("### Kết quả gán nhãn từ loại")
        pos_results = [{"Token": token, "POS": pos, "Meaning": POS_TAGS_EXPLANATION.get(pos, "Không xác định")} 
                       for token, pos in tagged_tokens]
        st.dataframe(pos_results, width="stretch", hide_index=True)

    # Export section
    st.divider()
    st.markdown('<p class="section-header">Xuất kết quả</p>', unsafe_allow_html=True)
    export_df = create_export_dataframe(tagged_tokens)
    csv_data = convert_df_to_csv(export_df)

    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("**📥 Định dạng CSV**  \nBao gồm: Token, POS Tag, và mô tả nghĩa")
    with col2:
        st.download_button(
            label="📊 Tải CSV",
            data=csv_data,
            file_name=f"vietnamese_nlp_result.csv",
            mime="text/csv",
            use_container_width=True,
        )

    # POS Tags explanation table
    st.divider()
    st.markdown('<p class="section-header">Bảng giải thích nhãn từ loại</p>', unsafe_allow_html=True)
    pos_table_df = create_pos_table()

    # Create styled dataframe with color preview
    pos_display_df = pos_table_df.copy()
    pos_display_df["Color Preview"] = pos_display_df["Color"].apply(
        lambda x: f'<div style="background-color: {x}; width: 45px; height: 45px; '
        f'border-radius: 10px; border: 2px solid #e2e8f0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"></div>'
    )

    st.dataframe(
        pos_display_df[["Tag", "Description", "Color Preview"]],
        width="stretch",
        hide_index=True,
        column_config={
            "Tag": st.column_config.TextColumn("Tag", width="small", help="Mã nhãn từ loại"),
            "Description": st.column_config.TextColumn("Mô tả", width="medium", help="Ý nghĩa của nhãn"),
            "Color Preview": st.column_config.TextColumn("Màu", width="small"),
        },
    )

    # Color legend with chips
    st.divider()
    st.markdown("### 🎨 Chú giải màu sắc")
    cols = st.columns(5)
    for i, (pos, description) in enumerate(POS_TAGS_EXPLANATION.items()):
        color = POS_COLORS.get(pos, "#94a3b8")
        with cols[i % 5]:
            st.markdown(
                f'<span class="color-chip" '
                f'style="background-color: {color}; color: white;">'
                f"{pos}: {description}"
                f'</span>',
                unsafe_allow_html=True,
            )


if __name__ == "__main__":
    main()


import streamlit as st
import pandas as pd
from pathlib import Path

from cleaner import DataCleaner
from ai_helper import ai_suggestions


# Page configuration
st.set_page_config(
    page_title="AI Data Cleaning Assistant",
    page_icon="🧹",
    layout="wide"
)


# Load custom CSS
css_path = Path(__file__).parent / "static" / "style.css"

if css_path.exists():
    css = css_path.read_text(encoding="utf-8")
    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True
    )


# Initialize session state
if "cleaned_df" not in st.session_state:
    st.session_state.cleaned_df = None

if "cleaned_source" not in st.session_state:
    st.session_state.cleaned_source = None

if "ai_result" not in st.session_state:
    st.session_state.ai_result = None


# Header
st.markdown(
    '<div class="main-title">'
    '🧹 AI-Powered Data Cleaning Assistant'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Upload, analyze, clean, and download your dataset'
    '</div>',
    unsafe_allow_html=True
)


# Sidebar
with st.sidebar:
    st.title("⚙️ Dashboard")
    st.write("**Available features**")
    st.write("📂 CSV file upload")
    st.write("🔍 Data quality analysis")
    st.write("🤖 AI cleaning suggestions")
    st.write("🧹 Automatic cleaning")
    st.write("📥 Download cleaned CSV")


# File upload
st.subheader("📂 Upload Your Dataset")

uploaded_file = st.file_uploader(
    "Choose a CSV file",
    type=["csv"]
)


if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        # Reset saved results if a different file is uploaded
        if st.session_state.get("source_name") != uploaded_file.name:
            st.session_state.cleaned_df = None
            st.session_state.cleaned_source = None
            st.session_state.ai_result = None
            st.session_state.source_name = uploaded_file.name

        st.success("CSV file uploaded successfully!")

        # Data quality metrics
        cleaner = DataCleaner(df)

        st.subheader("📊 Dataset Overview")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Rows", df.shape[0])

        with col2:
            st.metric("Total Columns", df.shape[1])

        with col3:
            st.metric("Missing Values", cleaner.count_missing())

        with col4:
            st.metric("Duplicate Rows", cleaner.count_duplicates())

        # Dataset preview
        st.subheader("📋 Original Dataset")
        st.dataframe(df, use_container_width=True)

        # Missing values report
        with st.expander("View Missing Values by Column"):
            missing = cleaner.missing_values()
            st.dataframe(
                missing.rename("Missing Count"),
                use_container_width=True
            )

        # Outlier report
        st.subheader("📈 Outlier Analysis")
        st.write(
            f"Possible numerical outliers: "
            f"**{cleaner.count_outliers()}**"
        )

        # AI suggestions
        st.subheader("🤖 AI Cleaning Suggestions")

        if st.button("Get AI Suggestions"):
            with st.spinner("AI is analyzing your dataset..."):
                st.session_state.ai_result = ai_suggestions(df)

        if st.session_state.ai_result:
            st.markdown(st.session_state.ai_result)

        # Automatic cleaning
        st.subheader("🧹 Clean Your Dataset")

        if st.button("Auto Clean Dataset"):
            with st.spinner("Cleaning dataset..."):
                st.session_state.cleaned_df = cleaner.clean()
                st.session_state.cleaned_source = uploaded_file.name

            st.success("Dataset cleaned successfully!")

        # Display and download cleaned data
        if (
            st.session_state.cleaned_df is not None
            and st.session_state.cleaned_source == uploaded_file.name
        ):
            cleaned = st.session_state.cleaned_df

            st.subheader("✅ Cleaned Dataset")
            st.dataframe(cleaned, use_container_width=True)

            before = len(df)
            after = len(cleaned)

            st.write(f"Original rows: {before}")
            st.write(f"Cleaned rows: {after}")
            st.write(f"Duplicate rows removed: {before - after}")

            csv_data = cleaned.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="📥 Download Cleaned CSV",
                data=csv_data,
                file_name="cleaned_data.csv",
                mime="text/csv"
            )

    except Exception as e:
        st.error(f"Unable to process the CSV file: {e}")

else:
    st.info("Please upload a CSV file to get started.")

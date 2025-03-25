import streamlit as st
from main import *
from pdf_to_answer_dict import *
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

# Set page config for a wider layout and custom title
st.set_page_config(page_title="Exam Grader", layout="wide")

# Title and subheader with some styling
st.title("📝 Automatic Exam Grader")
st.subheader("Upload your files and grade answers effortlessly")

# Add a styled info box with instructions
st.info("""
    **How to Use:**
    1. Upload a PDF with student answers.
    2. Upload a JSON file with the answer key.
    3. Click "Process Now" to see the results.
""")

# File upload section with columns for better layout
st.markdown("### Upload Files")
col1, col2 = st.columns([1, 1])
with col1:
    pdf_file = st.file_uploader("📄 Student Answers (PDF)", type="pdf", help="Upload a PDF file")
with col2:
    ans_key_file = st.file_uploader("🔑 Answer Key (JSON)", type="json", help="Upload a JSON file")

# Process section
st.markdown("### Grade Answers")
process_button = st.button("Process Now", key="process", help="Click to grade the answers")

if process_button:
    if pdf_file is not None and ans_key_file is not None:
        # Progress bar for visual feedback
        progress_bar = st.progress(0)
        with st.spinner("Extracting and grading answers..."):
            api_key = "K85286034988957"  
            progress_bar.progress(25)  # Update progress
            marks = main_st(pdf_file, ans_key_file, api_key)
            progress_bar.progress(75)  # Update progress
            
            if marks:
                st.success("✅ Grading completed!")
                # Format results
                text = "\n".join([f"{key}: {marks[key]}" for key in marks.keys()])
                total = sum(marks.values())
                text += f"\n\nTotal: {total}"
                progress_bar.progress(100)  # Complete progress
                
                # Display results in an expander for cleanliness
                with st.expander("View Detailed Results", expanded=True):
                    st.text_area("Results", text, height=250)
                
                # Add a download button for results
                st.download_button(
                    label="📥 Download Results",
                    data=text,
                    file_name="grading_results.txt",
                    mime="text/plain"
                )
            else:
                st.error("❌ Error: Unable to process the files")
                progress_bar.empty()
    else:
        st.warning("⚠️ Please upload both PDF and JSON files before processing.")

# Add a footer for extra polish
st.markdown("---")
st.markdown("Built with ❤️ by Tech Creators | Powered by Streamlit")
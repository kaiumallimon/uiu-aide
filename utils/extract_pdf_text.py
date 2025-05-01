import fitz  # PyMuPDF
import re
import json

def extract_text_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    return "\n".join(page.get_text() for page in doc)


def extract_header(text):
    header_match = re.search(
        r"Trimester:\s*([^\n]+)\s+Course Code:\s*([A-Z]+\s*\d+),\s*Course Title:\s*([^\n]+)",
        text, re.IGNORECASE
    )
    if header_match:
        return {
            "trimester": header_match.group(1).strip(),
            "course_code": header_match.group(2).strip(),
            "course_title": header_match.group(3).strip()
        }
    return {}

def clean_text(text):
    # Remove UIU boilerplate and page labels
    text = re.sub(r"United International University.*?Engineering \(CSE\)", "", text, flags=re.DOTALL)
    text = re.sub(r"Page\s+\d+\s+of\s+\d+", "", text)
    return text

def extract_questions(text):
    # Split major questions by Q.1, Q2, or just 1. style
    main_q_blocks = re.split(r"\n\s*(?:Q\.?\s*\d+|\d+\.)\s*\n?", text)
    questions = []

    for block in main_q_blocks[1:]:  # skip intro
        q = {"parts": {}}

        # Match only top-level subparts (a)-(h) at line starts
        subparts = list(re.finditer(
    r"^\s*\(?([a-hA-H])\)?\)\s+(.*?)(?=^\s*\(?[a-hA-H]\)?\)\s+|\Z)",
    block, re.DOTALL | re.MULTILINE))


        if subparts:
            for match in subparts:
                key = match.group(1).lower()
                val = re.sub(r"\[[^\]]+\]", "", match.group(2)).strip()  # remove mark tags like [3]
                q["parts"][key] = re.sub(r"\s+", " ", val)
        else:
            clean_block = re.sub(r"\[[^\]]+\]", "", block).strip()
            if clean_block:
                q["parts"]["a"] = re.sub(r"\s+", " ", clean_block)
        questions.append(q)
    return questions

# # ---------- MAIN ----------
# file_path = "CSE1111_Mid_222.pdf"  # Change to your PDF path
# text = extract_text_from_pdf(file_path)
# header = extract_header(text)
# text = clean_text(text)
# questions = extract_questions(text)
#
# output = {
#     **header,
#     "questions": questions
# }
#
# # Save JSON
# with open("parsed_exam.json", "w", encoding="utf-8") as f:
#     json.dump(output, f, indent=2)
#
# print("✅ Done: Saved to parsed_exam.json")

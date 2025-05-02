import fitz
import re
import json

def extract_text_from_pdf(file_obj):
    doc = fitz.open(stream=file_obj.read(), filetype="pdf")
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
    main_q_blocks = re.split(r"\n\s*(?:Q\.?\s*\d+|\d+\.)\s*\n?", text)
    questions = []

    for q_idx, block in enumerate(main_q_blocks[1:], 1):  # skip intro
        q = {"parts": {}, "index": q_idx}

        subparts = list(re.finditer(
            r"^\s*\(?([a-hA-H])\)?\)\s+(.*?)(?=^\s*\(?[a-hA-H]\)?\)\s+|\Z)",
            block, re.DOTALL | re.MULTILINE))

        if subparts:
            for match in subparts:
                key = match.group(1).lower()
                val = re.sub(r"\[[^\]]+\]", "", match.group(2)).strip()  # remove [x] marks
                q["parts"][key] = re.sub(r"\s+", " ", val)
        else:
            clean_block = re.sub(r"\[[^\]]+\]", "", block).strip()
            if clean_block:
                q["parts"]["a"] = re.sub(r"\s+", " ", clean_block)

        questions.append(q)
    return questions

def create_chunked_output(header, questions):
    chunks = []
    for q in questions:
        q_number = f"Q{q['index']}"
        for key, part in q['parts'].items():
            chunk = {
                "trimester": header.get("trimester", ""),
                "course_code": header.get("course_code", ""),
                "course_title": header.get("course_title", ""),
                "question_id": f"{q_number}({key})",
                "content": part
            }
            chunks.append(chunk)
    return chunks

# # ---------- MAIN ----------
# file_path = "CSE1111_Mid_222.pdf"  # Change to your PDF path
# text = extract_text_from_pdf(file_path)
# header = extract_header(text)
# text = clean_text(text)
# questions = extract_questions(text)
# chunks = create_chunked_output(header, questions)
#
# # # Output as JSON (ready for embedding or storing into a vector DB)
# print(json.dumps(chunks, indent=2))

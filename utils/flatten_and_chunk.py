from typing import List, Dict


def flatten_and_chunk_questions(questions: List[Dict[str, Dict[str, str]]], chunk_size: int = 500) -> List[str]:
    """
    Flattens a list of questions with subparts and chunks them into smaller strings for embedding.
    Each chunk will be up to `chunk_size` characters long.
    """

    chunks = []

    for question in questions:
        for part_label, part_text in question.get("parts", {}).items():
            clean_text = part_text.replace("\n", " ").strip()

            # If the part is small enough, add directly
            if len(clean_text) <= chunk_size:
                chunks.append(clean_text)
            else:
                # Split long part into smaller chunks
                for i in range(0, len(clean_text), chunk_size):
                    chunk = clean_text[i:i + chunk_size]
                    chunks.append(chunk)

    return chunks

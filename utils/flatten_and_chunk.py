from typing import List, Dict


def flatten_and_chunk_questions(questions: List[Dict[str, Dict[str, str]]], chunk_size: int = 500):
    """
    "flatten" means converting a nested structure (like a list of questions with subparts)
    into a simple list of strings,
    so that we can embed each string individually.

    Embedding APIs usually expect a list of plain strings — not nested objects.
    """

    flattened_questions = []

    # flatten the questions by extracting parts (a,b,c...)
    for question in questions:
        for part in question["parts"].values():
            flattened_questions.append(part)

    # chunk the flattened questions for embedding
    chunks = []
    current_chunk = []

    for question in flattened_questions:
        # if adding the question exceeds the chunk size, save the current chunk and start a new one
        if len(current_chunk) + len(question) > chunk_size:
            chunks.append(current_chunk)
            current_chunk = question
        else:
            current_chunk += " " + question

    # add the last chunk if it contains any content
    if current_chunk:
        chunks.append(current_chunk)

    return chunks

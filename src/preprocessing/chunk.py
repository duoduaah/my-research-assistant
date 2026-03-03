def chunk_paper(
    paper_id: str,
    full_text: str,
    max_chars: int = 16_000,
    overlap_chars: int = 1_000,
):
    """
    Splits a paper's text into overlapping character-based chunks,
    suitable for Claude models (no tokenizer required).

    Args:
        paper_id (str): Unique identifier for the paper
        full_text (str): Cleaned full text of the paper
        max_chars (int): Maximum characters per chunk
        overlap_chars (int): Overlapping characters between chunks

    Returns:
        List[dict]: Each dict contains paper_id, chunk_id, chunk_index, text
    """

    if not full_text or not full_text.strip():
        return []

    if overlap_chars >= max_chars:
        raise ValueError("overlap_chars must be smaller than max_chars")

    chunks = []
    text_length = len(full_text)
    start = 0
    chunk_index = 0

    while start < text_length:
        end = min(start + max_chars, text_length)
        chunk_text = full_text[start:end]
        chunks.append(
            {
                "paper_id": paper_id,
                "chunk_id": f"{paper_id}_chunk_{chunk_index:03d}",
                "chunk_index": chunk_index,
                "text": chunk_text,
            }
        )
        chunk_index += 1

        if end == text_length:
            break
        start = end - overlap_chars

    return chunks
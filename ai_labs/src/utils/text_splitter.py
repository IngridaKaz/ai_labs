from ai_labs.src.config import CHUNK_SIZE


def split_text(text: str, chunk_size: int = CHUNK_SIZE) -> list[str]:
    """
    Split text into smaller chunks while preserving sentence boundaries.

    This function splits text into chunks of approximately the specified size,
    ensuring that sentences are not broken in the middle. It uses periods as
    sentence boundaries and attempts to create chunks that are as close to the
    chunk_size as possible while keeping sentences intact.

    Args:
        text: The input text to be split
        chunk_size: The target size for each chunk

    Returns:
        A list of text chunks
    """
    chunks = []
    sentences = text.split(".")
    current_chunk = ""

    for sentence in sentences:
        sentence = sentence.strip() + "."

        # If adding this sentence would exceed chunk size and we already have content,
        # save the current chunk and start a new one
        if len(current_chunk) + len(sentence) > chunk_size and current_chunk:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
        else:
            current_chunk += " " + sentence

    # Add the last chunk if it contains any content
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

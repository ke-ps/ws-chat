from typing import List


CHUNK_SIZE = 1000
OVERLAP = 200


class ChunkingService:

    def chunk_text(self, text: str) -> List[str]:
    
        if not isinstance(text, str):
            raise TypeError("text must be a string")
        
        if not text:
            return []

        chunks: List[str] = []
        start = 0
        text_length = len(text)

        if text_length <= CHUNK_SIZE:
            return [text]

        while start < text_length:
            end = min(start + CHUNK_SIZE, text_length)
            if end == text_length or text_length - start <= CHUNK_SIZE:
                chunks.append(text[start:])
                break
            chunks.append(text[start:end])
            start += CHUNK_SIZE - OVERLAP

        return chunks

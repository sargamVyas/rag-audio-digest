import os
import logging
from pydub import AudioSegment
from typing import List

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def chunk_audio(
    input_wav: str,
    output_dir: str,
    chunk_ms: int = 30_000,
    overlap_ms: int = 5_000
) -> List[str]:
    """
    Splits input WAV file into overlapping chunks and writes them to output_dir.
    Returns list of chunk file paths.
    """
    audio = AudioSegment.from_wav(input_wav)
    os.makedirs(output_dir, exist_ok=True)
    output_paths = []

    i = 0
    start = 0
    while start < len(audio):
        end = min(start + chunk_ms, len(audio))
        chunk = audio[start:end]
        out_path = os.path.join(output_dir, f"chunk_{i:03d}.wav")
        chunk.export(out_path, format="wav")
        output_paths.append(out_path)
        logger.info(f"Wrote chunk {i}: {start}ms–{end}ms → {out_path}")
        i += 1
        start += chunk_ms - overlap_ms  # move window forward

    return output_paths

if __name__ == "__main__":
    input_wav = "data/processed/episode1_trimmed.wav"
    output_dir = "data/processed/chunks"
    chunk_audio(input_wav, output_dir)

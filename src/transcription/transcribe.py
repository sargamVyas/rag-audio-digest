import os
import logging
import whisper
from typing import List, Dict

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

model = whisper.load_model("base")  # or "small", "medium", "large"

def transcribe_audio_chunks(chunk_paths: List[str]) -> List[Dict]:
    """
    Transcribe each chunk with Whisper and return merged list of segments with timestamps.
    Each segment: {start, end, text}
    """
    full_transcript = []

    for path in chunk_paths:
        logger.info(f"Transcribing {path}")
        result = model.transcribe(path)
        for seg in result["segments"]:
            seg["chunk_file"] = path  # optional: track which chunk this came from
            full_transcript.append(seg)

    return full_transcript

def save_transcript_json(segments: List[Dict], out_path: str):
    import json
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(segments, f, indent=2)
    logger.info(f"Transcript saved to: {out_path}")

if __name__ == "__main__":
    from glob import glob
    chunk_paths = sorted(glob("data/processed/chunks/*.wav"))
    segments = transcribe_audio_chunks(chunk_paths)
    save_transcript_json(segments, "data/processed/transcript.json")

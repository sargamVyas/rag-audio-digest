# Preprocess the audio file
# Preprocess the audio file
import os
import subprocess
import logging
from typing import Optional

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def convert_to_wav(input_path: str, output_path: str,
                   sample_rate: int = 16000, channels: int = 1) -> Optional[str]:
    """
    Convert any audio file to a WAV at the desired sample rate and channel count.
    Returns the path on success, or None on failure.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cmd = [
        "ffmpeg", "-y", "-i", input_path,
        "-ar", str(sample_rate),
        "-ac", str(channels),
        output_path
    ]
    try:
        logger.info(f"Converting to WAV: {' '.join(cmd)}")
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        return output_path
    except subprocess.CalledProcessError as e:
        logger.error(f"ffmpeg conversion failed: {e}")
        return None

def trim_silence(input_wav: str, output_wav: str,
                 silence_threshold: str = "-50dB", silence_duration: float = 0.5) -> Optional[str]:
    """
    Remove leading and trailing silence from a WAV file.
    """
    os.makedirs(os.path.dirname(output_wav), exist_ok=True)
    # silenceremove=start_periods:stop_periods:start_threshold:stop_threshold
    silence_filter = f"silenceremove=1:1:{silence_threshold}:{silence_duration}"
    cmd = [
        "ffmpeg", "-y", "-i", input_wav,
        "-af", silence_filter,
        output_wav
    ]
    try:
        logger.info(f"Trimming silence: {' '.join(cmd)}")
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        return output_wav
    except subprocess.CalledProcessError as e:
        logger.error(f"ffmpeg silence trim failed: {e}")
        return None

if __name__ == "__main__":
    # Quick local test
    original = "/Users/apoorvvyas/Documents/Sargam_git_repository/rag-audio-digest/data/raw/test_episode.mp3"
    wav1 = "/Users/apoorvvyas/Documents/Sargam_git_repository/rag-audio-digest/data/processed/test_episode.wav"
    wav2 = "/Users/apoorvvyas/Documents/Sargam_git_repository/rag-audio-digest/data/processed/test_episode_trimmed.wav"

    if convert_to_wav(original, wav1):
        logger.info("WAV conversion successful.")
        if trim_silence(wav1, wav2):
            logger.info("Silence trimming successful.")
        else:
            logger.error("Silence trimming failed.")
    else:
        logger.error("WAV conversion failed.")

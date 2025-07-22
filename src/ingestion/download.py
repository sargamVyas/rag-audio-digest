import os
import logging
import requests
from typing import Optional

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def download_episode(audio_url: str, dest_path: str, chunk_size: int = 1024) -> Optional[str]:
    """
    Download a podcast episode from `audio_url` and save it to `dest_path`.
    Returns the path if successful, or None on failure.
    """
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    try:
        logger.info(f"Starting download: {audio_url}")
        resp = requests.get(audio_url, stream=True, timeout=10)
        resp.raise_for_status()
        with open(dest_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size):
                if chunk:
                    f.write(chunk)
        logger.info(f"Saved episode to: {dest_path}")
        return dest_path
    except requests.RequestException as e:
        logger.error(f"Failed to download {audio_url}: {e}")
        return None

if __name__ == "__main__":
    # quick test
    test_url = "https://ia600208.us.archive.org/14/items/testmp3testfile/mpthreetest.mp3"
    out = download_episode(test_url, "/Users/apoorvvyas/Documents/Sargam_git_repository/rag-audio-digest/data/raw/test_episode.mp3")
    if out:
        logger.info("Download test passed.")
    else:
        logger.error("Download test failed.")
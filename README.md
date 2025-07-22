## 1. Audio Ingestion & Pre-processing

This module handles fetching raw podcast audio and preparing it for transcription.

### 1.1 Download Episode

- **Location:** `src/ingestion/download.py`  
- **Function:** `download_episode(audio_url: str, dest_path: str, chunk_size: int = 1024) -> Optional[str]`  
- **Description:**  
  1. Creates target directory if needed  
  2. Streams the MP3 from `audio_url` to `dest_path`  
  3. Logs progress and handles HTTP errors  
- **Usage Example:**
  ```python
  from src.ingestion.download import download_episode

  url = "https://file-examples.com/wp-content/uploads/2017/11/file_example_MP3_1MG.mp3"
  out_path = "data/raw/episode1.mp3"
  download_episode(url, out_path)
# rag-audio-digest
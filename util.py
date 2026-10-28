import os
import glob

def getDownloadedSong(downloads_dir: str, song_id: str) -> str:
    """
    根據下載目錄與歌曲 ID 尋找對應的音樂檔案
    """
    if not os.path.exists(downloads_dir):
        return None
    
    # 嘗試尋找檔名包含 song_id 的檔案
    pattern = os.path.join(downloads_dir, f"*{song_id}*")
    matches = glob.glob(pattern)
    if matches:
        return matches[0]
        
    # 若檔名未包含 ID，則搜尋 downloads 目錄底下的常見音訊格式檔案
    audio_extensions = ('.mp3', '.m4a', '.opus', '.webm', '.wav', '.flac')
    for filename in os.listdir(downloads_dir):
        if filename.lower().endswith(audio_extensions):
            return os.path.join(downloads_dir, filename)
            
    return None

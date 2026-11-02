import os
import sys
import subprocess
import json
import argparse

def main():
    parser = argparse.ArgumentParser(description="YouTube Music Downloader")
    parser.add_argument('-m', '--metadata', required=True, help="Path to metadata JSON file")
    parser.add_argument('-c', '--cookies', required=True, help="Path to Netscape cookies file")
    args = parser.parse_args()

    if not os.path.exists(args.metadata):
        print(f"錯誤：找不到 metadata 檔案: {args.metadata}")
        sys.exit(1)
        
    if not os.path.exists(args.cookies):
        print(f"錯誤：找不到 cookies 檔案: {args.cookies}")
        sys.exit(1)

    # 讀取 metadata 內容
    with open(args.metadata, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
    
    # 確保是清單結構
    if isinstance(raw_data, dict):
        songs = [raw_data]
    elif isinstance(raw_data, list):
        songs = raw_data
    else:
        print("錯誤：metadata 格式不正確")
        sys.exit(1)

    total_songs = len(songs)
    print(f"準備下載共 {total_songs} 首歌曲（使用 Metadata: {args.metadata}, Cookies: {args.cookies}）：")

    # 定義 venv 內的 yt-dlp 路徑
    ytdlp_path = os.path.expanduser('~/youtube-music-library-exporter/venv/bin/yt-dlp')
    if not os.path.exists(ytdlp_path):
        ytdlp_path = 'yt-dlp'

    os.makedirs('downloads', exist_ok=True)

    # 迴圈逐一處理每一首歌
    for index, song in enumerate(songs, 1):
        artist = song.get('artist', '未知藝人')
        album = song.get('album', '未知專輯')
        song_title = song.get('title', '未知歌名')
        song_id = song.get('id', 'unknown_id') # 取得 metadata 中的 id
        url = song.get('href') # 對應 metadata.json 中的 href 欄位

        if not url:
            print(f"[{index}/{total_songs}] 跳過：{artist} - {song_title} (找不到有效網址)")
            continue

        print(f"\n[{index}/{total_songs}] 正在下載：{artist} - {song_title} (ID: {song_id})")

        cmd = [
            ytdlp_path,
            '--js-runtimes', 'deno',
            '--format', 'bestaudio',
            '--extract-audio',
            '--audio-format', 'best',
            '--audio-quality', '0',
            '--abort-on-error',
            '--no-playlist',
            '--ignore-config',
            '--no-warnings',
            '--no-progress',
            '--no-mtime',
            '--cookies', args.cookies,
            '-v',
            '--extractor-args', 'youtube:player-client=web_music;po_token=bgutil+http://127.0.0.1:4416',
            '--parse-metadata', f"{artist}:%(meta_artist)s",
            '--parse-metadata', f"{album}:%(meta_album)s",
            '--embed-metadata',
            '--embed-thumbnail',
            # 檔案命名結尾加上 _id 確保唯一性
            '--output', f"downloads/{artist}-{song_title}_{song_id}.%(ext)s",
            url
        ]

        # 確保系統 PATH 包含了 Deno
        env = os.environ.copy()
        deno_bin = os.path.expanduser('~/.deno/bin')
        if deno_bin not in env.get('PATH', ''):
            env['PATH'] = f"{deno_bin}:{env.get('PATH', '')}"

        # 執行下載
        result = subprocess.run(cmd, env=env)
        if result.returncode != 0:
            print(f"  -> 下載失敗 (退出碼: {result.returncode})")
        else:
            print("  -> 下載成功！")

if __name__ == '__main__':
    main()

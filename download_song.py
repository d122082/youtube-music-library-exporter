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

    # 讀取 metadata 內容（兼容 Dict 與 List）
    with open(args.metadata, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
    
    if isinstance(raw_data, list) and len(raw_data) > 0:
        metadata = raw_data[0]
    else:
        metadata = raw_data if isinstance(raw_data, dict) else {}

    # 定義 venv 內的 yt-dlp 路徑
    ytdlp_path = os.path.expanduser('~/Software/youtube-music-library-exporter/venv/bin/yt-dlp')
    if not os.path.exists(ytdlp_path):
        ytdlp_path = 'yt-dlp'

    artist = metadata.get('artist', '翁立友')
    album = metadata.get('album', '十年堅持 - 好膽你就來')
    song_title = metadata.get('title', '人生的歌')
    url = metadata.get('url', 'https://music.youtube.com/watch?v=elS8ko5vMic&list=PLMWy283je73vXWnNVR4wW3XtYZJU-xnmQ')

    print(f"準備下載共 1 首歌曲（使用 Metadata: {args.metadata}, Cookies: {args.cookies}）：")
    print(f"[1/1] 正在下載：{artist} - {song_title}")

    os.makedirs('downloads', exist_ok=True)

    # 組裝 yt-dlp 執行指令（加入 --js-runtimes deno 與正確的 bgutil po_token 格式）
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
        '--output', f"downloads/{artist}-{song_title}.%(ext)s",
        url
    ]

    # 回報即將執行的完整指令
    cmd_str = " ".join([f'"{arg}"' if " " in arg else arg for arg in cmd])
    print(f"\n-> 執行指令：\n{cmd_str}\n")

    # 確保系統 PATH 包含了 Deno（讓 subprocess 能夠順利呼叫 deno）
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

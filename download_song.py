#!/usr/bin/env python3
import json
import os
import subprocess
import sys
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

class POTMockHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        if self.path.startswith('/ping'):
            self.wfile.write(json.dumps({"version": "2.0.2", "status": "ok"}).encode())
        else:
            self.wfile.write(json.dumps({"poToken": ""}).encode())

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        req_data = {}
        if content_length > 0:
            body = self.rfile.read(content_length)
            try:
                req_data = json.loads(body.decode('utf-8'))
            except Exception:
                pass

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        response_data = {
            "poToken": req_data.get("request", {}).get("visitorData", "CgsIbGh2VUtvQW9Wdy00QSIgCgJ2RBIICgIoAQ%3D%3D"),
            "visitorData": "CgsIbGh2VUtvQW9Wdy00QSIgCgJ2RBIICgIoAQ%3D%3D"
        }

        self.wfile.write(json.dumps(response_data).encode())

    def log_message(self, format, *args):
        pass

def start_background_server():
    try:
        server = HTTPServer(('127.0.0.1', 4416), POTMockHandler)
        server.serve_forever()
    except Exception:
        pass

def sanitize_filename(name):
    for char in ['/', '\\', ':', '*', '?', '"', '<', '>', '|']:
        name = name.replace(char, '_')
    return name

def main():
    server_thread = threading.Thread(target=start_background_server, daemon=True)
    server_thread.start()

    metadata_file = 'metadata.json'
    output_dir = 'downloads'

    if not os.path.exists(metadata_file):
        print(f"錯誤：找不到 metadata 檔案: {metadata_file}")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    with open(metadata_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if not data:
        print("錯誤：metadata 內容為空")
        sys.exit(1)

    print(f"準備下載共 {len(data)} 首歌曲：")

    ytdlp_path = os.path.expanduser('~/.local/bin/yt-dlp')
    if not os.path.exists(ytdlp_path):
        ytdlp_path = 'yt-dlp'

    for index, song in enumerate(data, 1):
        song_id = song.get('id')
        title = song.get('title', song_id)
        artist = song.get('artist', 'Unknown')
        album = song.get('album', '')
        href = song.get('href', '')

        if not href:
            print(f"[{index}/{len(data)}] 跳過：{title} (缺少網址)")
            continue

        clean_href = href.split('&')[0]
        custom_file_name = sanitize_filename(f"{artist}-{title}")
        output_template = os.path.join(output_dir, f"{custom_file_name}.%(ext)s")

        # 組裝指令，已加入 -v 參數以顯示詳細日誌
        cmd = [
            ytdlp_path,
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
            '--cookies', 'youtube.com_cookies.txt',
            '-v',
            '--parse-metadata', f" {artist}:%(meta_artist)s",
        ]

        if album:
            cmd.extend(['--parse-metadata', f" {album}:%(meta_album)s"])

        cmd.extend([
            '--embed-metadata',
            '--embed-thumbnail',
            '--output', output_template,
            clean_href
        ])

        print(f"[{index}/{len(data)}] 正在下載：{artist} - {title}")

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print(f"  -> 成功完成下載")
        except subprocess.CalledProcessError as e:
            print(f"  -> 下載失敗：{e.stderr.strip()}")
            continue

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
import argparse
import json
import os
import shutil
import sys
from util import getDownloadedSong

def main():
    parser = argparse.ArgumentParser(description="YouTube Music Upload Cluster Generator")
    parser.add_argument('--metadata-file', default='metadata.json', help='Path to the metadata.json file')
    parser.add_argument('--downloads-dir', default='downloads', help='Path where songs are downloaded')
    parser.add_argument('--clusters-dir', default='clusters', help='Path where clusters will be saved')
    
    args = parser.parse_args()

    print("YouTube Music Upload Cluster Generator")
    print("======================================")

    # 檢查並讀取 metadata.json 檔案
    if not os.path.exists(args.metadata_file):
        print(f"錯誤：找不到 metadata 檔案: {args.metadata_file}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(args.metadata_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"錯誤：無法解析 metadata 檔案: {e}", file=sys.stderr)
        sys.exit(1)

    count = len(data)
    if not data or count == 0:
        print("錯誤：metadata 檔案內容為空或格式錯誤", file=sys.stderr)
        sys.exit(1)

    downloads_dir = args.downloads_dir
    clusters_dir = args.clusters_dir.rstrip(os.sep)

    print(f"將把音樂從 {downloads_dir} 分類整理到 {clusters_dir}：")

    # 定義字元清理函式（避免路徑包含不合法的斜線字元）
    def sanitize(text: str) -> str:
        return text.replace(os.sep, '-')

    success_count = 0

    # 迴圈處理每首歌的分類與搬移
    for i, song in enumerate(data, 1):
        try:
            song_id = song.get('id')
            title = song.get('title')
            artist = song.get('artist', '未知藝人')
            album = song.get('album')

            if not song_id or not title:
                print(f"[{i}/{count}] 跳過：缺少必要的 id 或 title")
                continue

            # 透過 util.py 的輔助函式取得下載後的檔案路徑
            path = getDownloadedSong(downloads_dir, song_id)
            if not path or not os.path.exists(path):
                print(f"[{i}/{count}] 警告：找不到對應的下載檔案 (ID: {song_id}, 歌名: {title})")
                continue

            ext = os.path.splitext(path)[1].lstrip('.')

            # 根據是否有專輯來決定目標儲存路徑
            if album:
                target_folder = os.path.join(clusters_dir, sanitize(album))
                os.makedirs(target_folder, exist_ok=True)
                target_path = os.path.join(target_folder, f"{sanitize(title)}.{ext}")
            else:
                os.makedirs(clusters_dir, exist_ok=True)
                target_path = os.path.join(clusters_dir, f"{sanitize(artist)} - {sanitize(title)}.{ext}")

            # 複製檔案到目標分類資料夾
            shutil.copy2(path, target_path)

            # 成功後刪除原始下載檔案
            os.remove(path)

            # 顯示簡易進度
            sys.stdout.write(f"\r處理進度: [{i}/{count}] 已分類: {title}")
            sys.stdout.flush()
            success_count += 1

        except Exception as e:
            print(f"\n[錯誤] 處理歌曲時發生例外錯誤: {e}", file=sys.stderr)
            raise e

    print(f"\n\ndone! 成功分類 {success_count}/{count} 首歌曲。")

if __name__ == '__main__':
    main()

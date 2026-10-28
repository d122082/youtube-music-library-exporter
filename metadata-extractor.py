#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import sys
from urllib.parse import parse_qs, urlparse
from bs4 import BeautifulSoup


def parse_item(node):
    """解析單個 ytmusic-responsive-list-item-renderer 節點"""
    title_tag = node.select_one('.title a')
    if not title_tag or not title_tag.get('href'):
        return None

    href = title_tag['href']

    # 解析 URL 取得影片 ID ('v' 參數)
    parsed_url = urlparse(href)
    qs = parse_qs(parsed_url.query)
    video_id = qs.get('v', [None])[0]

    # 標題與清理後的 href (移除 &list=MLPT)[cite: 2]
    title = title_tag.get_text(strip=True)
    clean_href = href.replace('&list=MLPT', '')

    # 解析 secondary-flex-columns：藝人 (eq(0)) 與 專輯 (eq(1))[cite: 2]
    artist = None
    album = None
    secondary_cols = node.select_one('.secondary-flex-columns')
    if secondary_cols:
        children = [c for c in secondary_cols.children if c.name]
        if len(children) > 0:
            artist = children[0].get_text(strip=True) or None
        if len(children) > 1:
            album = children[1].get_text(strip=True) or None

    # 解析歌曲時長[cite: 2]
    duration_tag = node.select_one(
        '.fixed-columns.style-scope.ytmusic-responsive-list-item-renderer'
    )
    duration = duration_tag.get_text(strip=True) if duration_tag else ''

    # 解析按讚狀態 (LIKE / DISLIKE)[cite: 2]
    like_button = node.select_one('ytmusic-like-button-renderer')
    like_status = like_button.get('like-status') if like_button else None
    if like_status == 'LIKE':
        is_liked = True
    elif like_status == 'DISLIKE':
        is_liked = False
    else:
        is_liked = None

    return {
        'id': video_id,
        'album': album,
        'artist': artist,
        'duration': duration,
        'href': clean_href,
        'is_liked': is_liked,
        'title': title,
    }


def format_json_with_jq(file_path):
    """若系統安裝有 jq，透過 subprocess 進行 jq 排列重寫；否則保持 Python 原生格式化"""
    try:
        # 使用 jq . 重新排列並格式化 JSON 檔案
        result = subprocess.run(
            ['jq', '.', file_path],
            capture_output=True,
            text=True,
            check=True,
        )
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(result.stdout)
        print(f"[Info] Successfully formatted {file_path} using jq.")
    except FileNotFoundError:
        print("[Info] 'jq' command not found in system. Using standard formatted JSON output.")
    except Exception as e:
        print(f"[Warning] Failed to format with jq: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description='YouTube Music Upload Metadata Extractor'
    )
    parser.add_argument(
        '--html-file',
        default='YouTube Music.html',
        help='Path to the HTML file',
    )
    parser.add_argument(
        '--metadata-file',
        default='metadata.json',
        help='Path to the metadata.json file',
    )
    parser.add_argument(
        '--use-jq',
        action='store_true',
        help='Force pass output through system jq binary after writing',
    )

    args = parser.parse_args()

    print("YouTube Music Upload Metadata Extractor")
    print("=======================================")

    # 檢查 HTML 檔案是否存在[cite: 2]
    if not os.path.exists(args.html_file):
        print(f"Error: html-file not found: {args.html_file}", file=sys.stderr)
        sys.exit(1)

    print(f"Will extract {args.metadata_file} from {args.html_file}:")

    # 讀取 HTML[cite: 2]
    try:
        with open(args.html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except Exception as e:
        print(f"Error reading HTML file: {e}", file=sys.stderr)
        sys.exit(1)

    soup = BeautifulSoup(html_content, 'html.parser')
    items = soup.select('ytmusic-responsive-list-item-renderer')

    total_items = len(items)
    data = []

    # 逐筆解析並顯示進度條[cite: 2]
    for i, node in enumerate(items, 1):
        item_data = parse_item(node)
        if item_data:
            data.append(item_data)

        # 命令列動態進度條
        sys.stdout.write(f"\rProcessing: [{i}/{total_items}]")
        sys.stdout.flush()

    print()  # 換行

    # 寫入成漂亮的 JSON 格式 (Python 原生已做到 indent=2 排列)
    try:
        with open(args.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error writing metadata file: {e}", file=sys.stderr)
        sys.exit(1)

    # 若指定 --use-jq 或系統存在 jq，自動透過命令列 jq 重新排版[cite: 2]
    if args.use_jq or shutil_which('jq'):
        format_json_with_jq(args.metadata_file)

    print("done")


def shutil_which(cmd):
    import shutil
    return shutil.which(cmd) is not None


if __name__ == '__main__':
    main()

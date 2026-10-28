#!/usr/bin/env python3
import argparse
import os
import sys
from bs4 import BeautifulSoup

def main():
    # 建立命令列參數解析，對應原本 PHP 的 InputOption
    parser = argparse.ArgumentParser(description='YouTube Music Upload Playlist Extractor')
    parser.add_argument(
        '--html-file', 
        default='YouTube Music.html', 
        help='Path to the HTML file'
    )
    parser.add_argument(
        '--playlist-file', 
        default='playlist.txt', 
        help='Path to the playlist.txt file'
    )
    
    args = parser.parse_args()

    print("YouTube Music Upload Playlist Extractor")
    print("=======================================")

    # 檢查 HTML 檔案是否存在
    if not os.path.exists(args.html_file):
        print(f"Error: html-file not found: {args.html_file}", file=sys.stderr)
        sys.exit(1)

    print(f"Will extract {args.playlist_file} from {args.html_file}:")

    # 讀取並解析 HTML 內容
    try:
        with open(args.html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except Exception as e:
        print(f"Error reading HTML file: {e}", file=sys.stderr)
        sys.exit(1)

    soup = BeautifulSoup(html_content, 'html.parser')
    items = soup.select('ytmusic-responsive-list-item-renderer')
    
    total_items = len(items)
    extracted_data = []

    # 模擬進度條與遍歷節點
    for i, node in enumerate(items, 1):
        # 檢查是否有標題連結 (.title a)
        title_tag = node.select_one('.title a')
        if not title_tag:
            continue

        song_title = title_tag.get_text(strip=True)

        # 抓取 secondary-flex-columns 底下的第一個子元素作為藝人/演出者
        secondary_cols = node.select_one('.secondary-flex-columns')
        artist = ""
        if secondary_cols:
            children = [child for child in secondary_cols.children if child.name]
            if children:
                artist = children[0].get_text(strip=True)

        # 組合格式：「歌名 by 藝人」
        extracted_data.append(f"{song_title} by {artist}")

        # 簡單印出進度視覺化
        sys.stdout.write(f"\rProcessing: [{i}/{total_items}]")
        sys.stdout.flush()

    print() # 換行

    # 將結果寫入 playlist 檔案
    try:
        with open(args.playlist_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(extracted_data) + '\n')
    except Exception as e:
        print(f"Error writing playlist file: {e}", file=sys.stderr)
        sys.exit(1)

    print("done")

if __name__ == '__main__':
    main()

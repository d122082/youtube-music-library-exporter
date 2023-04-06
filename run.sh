# /bin/sh
if [ $1 ]; then
                `./metadata-extractor --html-file=$1`
                `./downloader`
                 rm -rf downloads/*.opus
                 for f in ./downloads/*.m4a; do ffmpeg -i "$f" -codec:v copy -codec:a libmp3lame -q:a 2 "${f%.m4a}.mp3"; done
                 rm -rf ./downloads/*.m4a
                 rm -rf metadata.json
                 cat downloader.log
                 rm -rf downloader.log
        else
                `./metadata-extractor --html-file=Youtube\ Music.html`
                `./downloader`
                 rm -rf downloads/*.opus
                 for f in ./downloads/*.m4a; do ffmpeg -i "$f" -codec:v copy -codec:a libmp3lame -q:a 2 "${f%.m4a}.mp3"; done
                 rm -rf ./downloads/*.m4a
                 rm -rf metadata.json
                 cat downloader.log
                 rm -rf downloader.log

        fi

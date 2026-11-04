# /bin/sh
# Need download complete youtube music.html
# Cookie file need use netscape cookie type
# if [ $1 ]; then
                # `./metadata-extractor --html-file=$1`
                # `./downloader`
                 # rm -rf downloads/*.opus
                 # for f in ./downloads/*.m4a; do ffmpeg -i "$f" -codec:v copy -codec:a libmp3lame -q:a 2 "${f%.m4a}.mp3"; done
                 # rm -rf ./downloads/*.m4a
                 # rm -rf metadata.json
                 # cat downloader.log
                 # rm -rf downloader.log
        # else
                # `./metadata-extractor --html-file=Youtube\ Music.html`
                # `./downloader`
                 # rm -rf downloads/*.opus
                 # for f in ./downloads/*.m4a; do ffmpeg -i "$f" -codec:v copy -codec:a libmp3lame -q:a 2 "${f%.m4a}.mp3"; done
                 # rm -rf ./downloads/*.m4a
                 # rm -rf metadata.json
                 # cat downloader.log
                 # rm -rf downloader.log

        # fi
#!/bin/sh

# ------ 預設值設定 ------
html_file="YouTube Music.html"
cookie_file=""
path="."

# ------ 解析命令列引數 ------
while [ "$#" -gt 0 ]; do
    case "$1" in
        --html-file=*)
            html_file="${1#*=}"
            shift
            ;;
        --cookie=*)
            cookie_file="${1#*=}"
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [--html-file=FILENAME] [--cookie=COOKIE_FILE]"
            exit 0
            ;;
        *)
            echo "Unknown parameter: $1"
            exit 1
            ;;
    esac
done


python metadata-extractor.py --html-file=$html_file --cookie=$cookie_file
python playlist-extractor.py --html-file=$html_file --cookie=$cookie_file
python donwload_song.py  --metadata=metadata.json --cookie=$cookie_file
for f in ./downloads/*.m4a; do ffmpeg -i "$f" -codec:v copy -codec:a libmp3lame -q:a 2 "${f%.m4a}.mp3"; done
rm -rf downloads/*.m4a
#mv downloads/*.mp3 $path/
#if [ $? = 0 ];
#then
#        rm -rf downloads/;
#else
#        echo "Error to mv *.MP3"
#fi
#cat downloader.log
#if [ $? = 0 ];
#then
#        rm -rf downloader.log
#else
#        echo "Error to show downloader.log"
#fi

#rm -rf metadata.json
#rm -rf YouTube\ Music.html

# /bin/sh
if [ $1 ]; then
		html_f=$1
	else
		html_f='YouTube Music.html'
	fi

./metadata-extractor  --html-file $html_f
./downloader
rm -rf downloader.log
rm -rf downloads/*.opus
for f in ./downloads/*.m4a; do ffmpeg -i "$f" -codec:v copy -codec:a libmp3lame -q:a 2 "${f%.m4a}.mp3"; done
rm -rf ./downloads/*.m4a
rm -rf metadata.json

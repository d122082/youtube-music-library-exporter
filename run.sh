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

#------Setting-----
path=/mnt/d/StarFly/Download
#------Setting-----

mv $path/YouTube\ Music.html  .
rm -rf $path/YouTube\ Music_files/
./metadata-extractor
cat metadata.json | jq > 1.txt
rm -rf metadata.json
mv 1.txt metadata.json
vi metadata.json
./downloader
cat downloader.log
for f in ./downloads/*.m4a; do ffmpeg -i "$f" -codec:v copy -codec:a libmp3lame -q:a 2 "${f%.m4a}.mp3"; done
rm -rf downloads/*.m4a
mv downloads/*.mp3 $path/
if [ $? = 0 ];
then
        rm -rf downloads/;
else
        echo "Error to mv *.MP3"
fi
cat downloader.log
if [ $? = 0 ];
then
        rm -rf downloader.log
else
        echo "Error to show downloader.log"
fi

rm -rf metadata.json
rm -rf YouTube\ Music.html

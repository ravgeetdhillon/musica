# Musica

Automating my music release.

## Background

For the past 4 years, I have been making music as a hobby. Over this period I have made more than 300 tracks. But never got time to upload them to my Youtube channel. The reason was that it takes a lot of time to create videos, then upload it to Youtube, where you have to fill a lot of data like video's title, description, tags, and other metadata.

So one day I was listening to my old music with my brother and he asked me why don't you upload these beats to your channel. I told him about the above problem. Then he said, "Man, you are a programmer, why don't you automate the process?". It was the Eureka moment right there. So I sat on the Weekend to complete this project and gracefully it happened.

## How it works

The process is pretty straightforward. The GitHub Actions' workflow runs every 3rd day. It scans my Google Drive to check if there are any new tracks to upload. If there is at least one new track, it downloads the track and the artwork related to it. Then by using, [FFmpeg](https://www.ffmpeg.org/), it creates a video using downloaded track and artwork. The new video is uploaded to my [Youtube channel](http://youtube.com/c/ravdmusic) using YouTube API which fills in the required metadata about the video.

## Resources

* YouTube Data API: [https://developers.google.com/youtube/v3](https://developers.google.com/youtube/v3)

* Google Drive API: [https://developers.google.com/drive/v3](https://developers.google.com/drive/v3)

## Note

If you loved my project, please show your appreciation by clicking **Star**.

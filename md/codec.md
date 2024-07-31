The videos will be re-encoded after transfer in three different ways:

## H.264 Fixed Bitrate 8 Mbps with Deinterlacing
```ffmpeg -i video_1.MTS -vf "yadif=0:-1:0" -c:v libx264 -b:v 8M -preset medium -c:a copy video_1_H264_8Mbps_Deinterlaced.mp4```

for ffmpeg-python:

```boh```


## H.264 Fixed Bitrate 4 Mbps with Deinterlacing
```ffmpeg -i video_1.MTS -vf "yadif=0:-1:0" -c:v libx264 -b:v 4M -preset medium -c:a copy video_1_H264_4Mbps_Deinterlaced.mp4```

for ffmpeg-python:

```boh```


## H.265 Variable Bitrate CRF 23 with Deinterlacing
```ffmpeg -i video_1.MTS -vf "yadif=0:-1:0" -c:v libx265 -crf 23 -preset medium -c:a copy video_1_H265_CRF23_Deinterlaced.mp4```

for ffmpeg-python:

```boh```


### Notes:
- The videos are always deinterlaced
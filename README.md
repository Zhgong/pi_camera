## Use ffmpeg and Nginx to stream video

# change add name to hosts
rtmp-postbird



```
ffmpeg -f v4l2  -framerate 25 -video_size 640x480 -i  /dev/video0 -strict -2 -vcodec libx264 -acodec libvo_aacenc  -f flv rtmp://localhost/live/
```


```
rtmp {                
    server {
        listen 1935;  #服务端口--默认
        chunk_size 4096;   #数据传输块的大小--默认
        #设置直播的application名称是 live
    application live{ 
        live on; #live on表示开启直播模式
        }
        #设置推流的应用名称
    application push{ 
        live on; #开启直播
        push rtmp://rtmp-postbird/live; #推流到上面的直播应用
        }
    }
}
```


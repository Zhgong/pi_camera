FROM ubuntu:20.04

# Fix timezone issue
ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /

RUN apt-get update \
    && apt-get install nginx -y \
    && apt-get install libnginx-mod-rtmp -y \
    && apt-get install ffmpeg -y

# forward request and error logs to docker log collector
# RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    # && ln -sf /dev/stderr /var/log/nginx/error.log

EXPOSE 80

STOPSIGNAL SIGQUIT


CMD ["nginx", "-g", "daemon off;"]
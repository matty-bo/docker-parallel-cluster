FROM busybox
COPY ./mean.sh /
RUN ["chmod", "+x", "/mean.sh"]

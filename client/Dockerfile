FROM ubuntu

RUN apt update && \
    apt install -y curl iproute2 python3 && \
    apt clean

CMD ["tail", "-f", "/dev/null"]

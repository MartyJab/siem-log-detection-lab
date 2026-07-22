FROM ubuntu

RUN apt update && \
    apt install -y apache2 python3 && \
    apt clean

EXPOSE 80

CMD ["apachectl", "-D", "FOREGROUND"]

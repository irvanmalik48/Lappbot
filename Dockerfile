FROM irvann48/lappbot:latest

RUN git clone -b master https://github.com/irvanmalik48/Lappbot /root/userbot
RUN chmod 777 /root/userbot
WORKDIR /root/userbot/

EXPOSE 80 443

CMD ["python3","-m","userbot"]

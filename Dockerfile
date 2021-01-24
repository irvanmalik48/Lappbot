FROM irvann48/lappbot:alpine

RUN git clone -b master https://github.com/irvanmalik48/Lappbot /root/userbot
RUN chmod 777 /root/userbot
RUN pip install requirements.txt
WORKDIR /root/userbot/

EXPOSE 80 443

CMD ["python3","-m","userbot"]

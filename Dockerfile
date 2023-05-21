FROM rapidfort/flaskapp:latest
WORKDIR /application
LABEL Отправка по http API на FTP
COPY . .
RUN pip install -r requirements.txt

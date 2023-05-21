# 1c-SFTP
Для старых версий 1с отправка на sftp через http(flask)

## Запуск через Docker
  Изменить логин и пароль в файле flask_app.py в строке
  hostname='10.254.15.127', port=22, username='username', password='password'
  
  >Пример для Windows Docker
  
  * Собрать контейнер docker build . < Dockerfile -t yourimage_name:last
  * Запустить контейнер docker run --publish 5000:5000 yourimage_name:last
  * Проверить работу можно зайдя по адресу http://localhost:5000/ftp 
  
## Запуск python
  * Установить зависимые пакеты указав requirements.txt 
  * Запустить flask

## Пример кода 1С
  * В файле ОтправкаФайла.epf
  

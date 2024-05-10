# Temel imajı belirleme
FROM python:3.9
FROM mcr.microsoft.com/playwright:v1.35.0-jammy
# Çalışma dizinini belirleme
WORKDIR /app
RUN pwd
RUN ls

# Gereksinimleri kopyalama
COPY requirements.txt .
RUN  apt update ; apt install -y python3-pip
# Gereksinimleri yükleme
RUN pip install -r requirements.txt
RUN pip install tzlocal==2.1 tzdata

#RUN pip install pytest-playwright
#RUN playwright install  chromium



# Uygulama kodunu kopyalama
COPY . .

RUN chmod 664 db.sqlite3
# Portu açma (isteğe bağlı)
EXPOSE 8000

#RUN python3 manage.py makemigrations
#RUN python3 manage.py migrate
 

# Uygulamayı çalıştırma
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
# Temel imajı belirleme
FROM python:3.9

# Çalışma dizinini belirleme
WORKDIR /app

# Gereksinimleri kopyalama
COPY requirements.txt .

# Gereksinimleri yükleme
RUN pip install -r requirements.txt


RUN apt-get update && \
    apt-get install -y xvfb gnupg wget curl unzip --no-install-recommends && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list && \
    apt-get update -y && \
    apt-get install -y google-chrome-stable && \
    CHROMEVER=$(google-chrome --product-version | grep -o "[^\.]*\.[^\.]*\.[^\.]*") && \
    DRIVERVER=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROMEVER") && \
    wget -q --continue -P /chromedriver "http://chromedriver.storage.googleapis.com/$DRIVERVER/chromedriver_linux64.zip" && \
    unzip /chromedriver/chromedriver* -d /chromedriver

# make the chromedriver executable and move it to default selenium path.
RUN chmod +x /chromedriver/chromedriver
RUN mv /chromedriver/chromedriver /usr/bin/chromedriver

# Uygulama kodunu kopyalama
COPY . .

# Portu açma (isteğe bağlı)
EXPOSE 8000

RUN python manage.py makemigrations
RUN python manage.py migrate
 

# Uygulamayı çalıştırma
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
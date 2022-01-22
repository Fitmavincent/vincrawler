# As Scrapy runs on Python, I choose the official Python 3 Docker image.
FROM python:3

# Set the working directory to /usr/src/app.
WORKDIR /usr/src/app

# Install Scrapy
RUN pip3 install --no-cache-dir scrapy

RUN pip3 install scrapyrt

COPY . .

ENTRYPOINT ["scrapyrt", "-i", "0.0.0.0", "-p", "9080"]

EXPOSE 9080
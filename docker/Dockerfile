FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN apt-get autoremove -y ; apt-get update -y && apt-get install -y postgresql-client-13 libpq-dev vim-nox less libxmlsec1-dev ; apt-get clean

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint

COPY start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

WORKDIR /app

ENTRYPOINT ["/entrypoint"]

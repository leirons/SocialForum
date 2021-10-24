FROM python:3.8

WORKDIR /usr/src/app

COPY . .
RUN pip install -r requirements.txt
RUN chmod 775 entrypoint.sh

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
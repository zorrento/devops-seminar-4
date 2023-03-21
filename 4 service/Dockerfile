FROM python

WORKDIR /app

COPY . .

RUN pip install flask

RUN pip install requests

RUN pip install pymongo

EXPOSE 80

CMD [ "python", "main.py" ]
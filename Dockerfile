FROM python:3.9

WORKDIR /app

EXPOSE 4000
COPY ./requirements.txt /app/requirements.txt

RUN  pip install --no-cache-dir -r requirements.txt


COPY . ./app/

CMD ["uvicorn", "app.main:app","--host","0.0.0.0","--port","4000"]
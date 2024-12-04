FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app
COPY . .
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
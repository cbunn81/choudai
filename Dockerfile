FROM python:3.10-alpine

COPY . /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip --no-cache-dir install -r requirements.txt

ENTRYPOINT ["python", "choudai/choudai.py"]
CMD [""]
FROM python:3.11.13-slim-trixie

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENTRYPOINT [ "uvicorn", "src.main:app" ]

CMD [ "--host", "0.0.0.0", "--port", "8000", "--reload", "--reload-dir=src" ]
# CMD python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload  --reload-dir=src


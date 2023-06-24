FROM python:3.11-alpine AS builder

RUN mkdir -p /opt
WORKDIR /opt

COPY . /code
WORKDIR /code

RUN pip install -r build_requirements.txt --no-cache-dir
RUN python generate_proto.py


FROM python:3.11-alpine

COPY --from=builder /code /app
WORKDIR /app

RUN pip install -r run_requirements.txt --no-cache-dir

EXPOSE 8000

CMD [ "python", "main.py" ]

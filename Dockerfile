FROM python:alpine3.7
WORKDIR /usr/src/app
COPY requirements.txt .
RUN apk --update --no-cache add git \
    && pip install --no-cache-dir -r requirements.txt
COPY *.py ./
CMD ["python", "gh2bb.py"]

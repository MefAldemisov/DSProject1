FROM python:3.7-alpine
COPY requirements.txt /tmp/
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt
WORKDIR /app
COPY ./ /app
EXPOSE 5000
CMD python3 app.py

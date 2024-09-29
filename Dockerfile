FROM python:3.10-slim
WORKDIR /app
COPY healthbot.py requirements.txt /app/
RUN pip3 install -r requirements.txt
CMD ["python", "healthbot.py"]
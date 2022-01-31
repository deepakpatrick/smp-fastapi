FROM python:3.10.2

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# CMD [ "python", "./your-daemon-or-script.py" ]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

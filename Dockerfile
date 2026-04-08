COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ ./src/
COPY app.py inference.py .

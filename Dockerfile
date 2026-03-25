FROM pytorch/pytorch:2.2.0-cuda12.1-cudnn8-devel

RUN apt-get update && apt-get install -y \
    libgl1 libsm6 libxext6 libxrender-dev \
    libglib2.0-0 libgomp1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


RUN python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"

COPY . .

CMD ["python", "src/tracker.py"]


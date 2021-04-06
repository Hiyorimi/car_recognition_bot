# Telegram bot capable of recognizing car on the photo.

This is a bot which is capable of processing sent images.

## Setup

### Local setup

```bash
cp env.template ./.env
poetry install
poetry run python3 main.py
```

### Docker setup

```bash
docker build -t car_recognition_bot 
docker run -d --name car_recognition_bot -e ENV=productionn -e API_TOKEN=1111:YOUR_TOKEN car_recognition_bot python3 main.py.
```

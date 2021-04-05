# Image processing telegram bot

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
docker build -t image_processing_bot 
docker run -d --name image_processing_bot -e ENV=productionn -e API_TOKEN=1111:YOUR_TOKEN image_processing_bot python3 main.py.
```
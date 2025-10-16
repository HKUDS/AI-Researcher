# AI-Researcher Docker Setup

This document explains how to run AI-Researcher using Docker Compose.

## Prerequisites

1. **Docker**: Install Docker Desktop or Docker Engine
   - [Docker Desktop](https://docs.docker.com/desktop/) (recommended for Windows/Mac)
   - [Docker Engine](https://docs.docker.com/engine/install/) (for Linux)

2. **Docker Compose**: Usually included with Docker Desktop, or install separately
   - [Docker Compose Installation](https://docs.docker.com/compose/install/)

3. **API Keys**: You'll need the following API keys:
   - **GitHub AI Token**: For GitHub Copilot or GitHub AI features
   - **OpenRouter API Key**: For accessing various LLM models

## Quick Start

### Option 1: Using the Startup Script (Recommended)

#### Windows
```bash
start_docker.bat
```

#### Linux/Mac
```bash
chmod +x start_docker.sh
./start_docker.sh
```

The startup script will:
1. Check if Docker and Docker Compose are installed
2. Create necessary directories
3. Create a `.env` file template if it doesn't exist
4. Pull the required Docker image
5. Start the services

### Option 2: Manual Setup

1. **Create the `.env` file**:
   ```bash
   # Copy the template and edit with your API keys
   cp .env.template .env
   ```

2. **Edit the `.env` file** with your API keys:
   ```env
   GITHUB_AI_TOKEN=your_github_ai_token
   OPENROUTER_API_KEY=your_openrouter_api_key
   ```

3. **Start the services**:
   ```bash
   docker-compose up -d
   ```

## Services

The Docker Compose setup includes two services:

### 1. AI-Researcher API (`ai-researcher`)
- **Port**: 8000
- **Purpose**: Main research agent API
- **Image**: `tjbtech1/airesearcher:v1`

### 2. Web GUI (`web-gui`)
- **Port**: 7860
- **Purpose**: Gradio-based web interface
- **Image**: Built from `Dockerfile.web`

## Accessing the Services

Once the services are running:

- **Web GUI**: http://localhost:7860
- **API**: http://localhost:8000

## Configuration

### Environment Variables

The main configuration is done through the `.env` file:

```env
# Container Configuration
DOCKER_WORKPLACE_NAME=workplace_paper
BASE_IMAGES=tjbtech1/airesearcher:v1
COMPLETION_MODEL=openrouter/google/gemini-2.5-pro-preview-05-20
CHEEP_MODEL=openrouter/google/gemini-2.5-pro-preview-05-20
GPUS='"device=0"'
CONTAINER_NAME=paper_eval
WORKPLACE_NAME=workplace
CACHE_PATH=cache
PORT=7020
PLATFORM=linux/amd64

# LLM Configuration
GITHUB_AI_TOKEN=your_github_ai_token
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_API_BASE=https://openrouter.ai/api/v1

# Task Configuration
CATEGORY=vq
INSTANCE_ID=one_layer_vq
TASK_LEVEL=task1
MAX_ITER_TIMES=0
```

### GPU Configuration

To use GPU acceleration, modify the `GPUS` variable:

- **Single GPU**: `GPUS='"device=0"'`
- **Multiple GPUs**: `GPUS='"device=0,1"'`
- **All GPUs**: `GPUS='"all"'`
- **No GPU**: `GPUS=None`

## Useful Commands

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f ai-researcher
docker-compose logs -f web-gui
```

### Stop Services
```bash
docker-compose down
```

### Restart Services
```bash
docker-compose restart
```

### Rebuild Services
```bash
docker-compose up -d --build
```

### Access Container Shell
```bash
# AI-Researcher container
docker-compose exec ai-researcher bash

# Web GUI container
docker-compose exec web-gui bash
```

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   - Check if ports 8000 or 7860 are already in use
   - Modify the port mappings in `docker-compose.yml`

2. **API Key Issues**
   - Ensure your API keys are correctly set in the `.env` file
   - Check if the API keys have sufficient credits/permissions

3. **GPU Issues**
   - Ensure Docker has GPU access (nvidia-docker for NVIDIA GPUs)
   - Check if the GPU configuration in `.env` matches your setup

4. **Permission Issues**
   - Ensure the `workplace`, `cache`, and `logs` directories have proper permissions

### Getting Help

- Check the logs: `docker-compose logs -f`
- Restart services: `docker-compose restart`
- Rebuild containers: `docker-compose up -d --build`

## Development

### Building Custom Images

To build the AI-Researcher image locally:

```bash
cd docker
docker build -t tjbtech1/airesearcher:v1 .
```

To build the web GUI image:

```bash
docker build -f Dockerfile.web -t ai-researcher-web .
```

### Modifying the Setup

- Edit `docker-compose.yml` to modify service configuration
- Edit `Dockerfile.web` to modify the web GUI container
- Edit `docker/Dockerfile` to modify the AI-Researcher container

## Security Notes

- Never commit your `.env` file with real API keys
- The `.env` file is already in `.gitignore`
- Use environment-specific API keys for different deployments

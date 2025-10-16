#!/bin/bash

echo "🚀 Starting AI-Researcher with Docker Compose"
echo "=============================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "   Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "   Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p workplace cache logs

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cat > .env << 'EOF'
# ================ container configuration ================
DOCKER_WORKPLACE_NAME=workplace_paper
BASE_IMAGES=tjbtech1/airesearcher:v1
COMPLETION_MODEL=openrouter/google/gemini-2.0-flash-exp
CHEEP_MODEL=openrouter/google/gemini-2.0-flash-exp
GPUS='"device=0"'
CONTAINER_NAME=paper_eval
WORKPLACE_NAME=workplace
CACHE_PATH=cache
PORT=7020
PLATFORM=linux/amd64

# ================ llm configuration ================
GITHUB_AI_TOKEN=your_github_ai_token
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_API_BASE=https://openrouter.ai/api/v1

# ================ task configuration ================
CATEGORY=vq
INSTANCE_ID=one_layer_vq
TASK_LEVEL=task1
MAX_ITER_TIMES=0
EOF
    echo "✅ .env file created. Please edit it with your API keys before continuing."
    echo "   Required API keys:"
    echo "   - GITHUB_AI_TOKEN: Your GitHub AI token"
    echo "   - OPENROUTER_API_KEY: Your OpenRouter API key"
    echo ""
    echo "   After editing .env, run this script again."
    exit 0
fi

# Build the Docker image
echo "📦 Building Docker image..."
docker-compose build ai-researcher

# Start the services
echo "🚀 Starting Docker Compose services..."
docker-compose up -d

echo ""
echo "✅ AI-Researcher is starting up!"
echo ""
echo "📊 Services:"
echo "   - AI Researcher API: http://localhost:8000"
echo "   - Web GUI: http://localhost:7860"
echo ""
echo "📝 To view logs:"
echo "   docker-compose logs -f"
echo ""
echo "🛑 To stop services:"
echo "   docker-compose down"
echo ""
echo "🔧 To restart services:"
echo "   docker-compose restart"

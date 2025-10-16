@echo off
echo 🚀 Starting AI-Researcher with Docker Compose
echo ==============================================

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed. Please install Docker first.
    echo    Visit: https://docs.docker.com/get-docker/
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose first.
    echo    Visit: https://docs.docker.com/compose/install/
    pause
    exit /b 1
)

REM Create necessary directories
echo 📁 Creating necessary directories...
if not exist workplace mkdir workplace
if not exist cache mkdir cache
if not exist logs mkdir logs

REM Check if .env file exists
if not exist .env (
    echo ⚠️  .env file not found. Creating from template...
    (
        echo # ================ container configuration ================
        echo DOCKER_WORKPLACE_NAME=workplace_paper
        echo BASE_IMAGES=tjbtech1/airesearcher:v1
        echo COMPLETION_MODEL=openrouter/google/gemini-2.0-flash-exp
echo CHEEP_MODEL=openrouter/google/gemini-2.0-flash-exp
        echo GPUS='"device=0"'
        echo CONTAINER_NAME=paper_eval
        echo WORKPLACE_NAME=workplace
        echo CACHE_PATH=cache
        echo PORT=7020
        echo PLATFORM=linux/amd64
        echo.
        echo # ================ llm configuration ================
        echo GITHUB_AI_TOKEN=your_github_ai_token
        echo OPENROUTER_API_KEY=your_openrouter_api_key
        echo OPENROUTER_API_BASE=https://openrouter.ai/api/v1
        echo.
        echo # ================ task configuration ================
        echo CATEGORY=vq
        echo INSTANCE_ID=one_layer_vq
        echo TASK_LEVEL=task1
        echo MAX_ITER_TIMES=0
    ) > .env
    echo ✅ .env file created. Please edit it with your API keys before continuing.
    echo    Required API keys:
    echo    - GITHUB_AI_TOKEN: Your GitHub AI token
    echo    - OPENROUTER_API_KEY: Your OpenRouter API key
    echo.
    echo    After editing .env, run this script again.
    pause
    exit /b 0
)

REM Build the Docker image
echo 📦 Building Docker image...
docker-compose build ai-researcher

REM Start the services
echo 🚀 Starting Docker Compose services...
docker-compose up -d

echo.
echo ✅ AI-Researcher is starting up!
echo.
echo 📊 Services:
echo    - AI Researcher API: http://localhost:8000
echo    - Web GUI: http://localhost:7860
echo.
echo 📝 To view logs:
echo    docker-compose logs -f
echo.
echo 🛑 To stop services:
echo    docker-compose down
echo.
echo 🔧 To restart services:
echo    docker-compose restart
echo.
pause

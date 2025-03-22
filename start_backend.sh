#!/bin/bash

# Color variables
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Starting BrainClassify Backend ===${NC}"

# Create uploads and feedback directories if they don't exist
mkdir -p uploads
mkdir -p feedback

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating Python virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${YELLOW}Activating Python virtual environment...${NC}"
source venv/bin/activate

# Install backend dependencies
echo -e "${YELLOW}Installing backend dependencies...${NC}"
cd backend
pip install -r requirements.txt

# Start the FastAPI server with debug mode for automatic reloading
echo -e "${GREEN}Starting FastAPI server...${NC}"
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload 
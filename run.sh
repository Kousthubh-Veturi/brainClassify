#!/bin/bash

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Color variables
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== BrainClassify Application Launcher ===${NC}"

# Check if Python is installed
if ! command_exists python3; then
    echo -e "${RED}Error: Python 3 is not installed. Please install Python 3 and try again.${NC}"
    exit 1
fi

# Check if Node.js is installed
if ! command_exists node; then
    echo -e "${RED}Error: Node.js is not installed. Please install Node.js and try again.${NC}"
    exit 1
fi

# Check if npm is installed
if ! command_exists npm; then
    echo -e "${RED}Error: npm is not installed. Please install npm and try again.${NC}"
    exit 1
fi

# Make the startup scripts executable
chmod +x start_backend.sh
chmod +x start_frontend.sh

# Create directories needed for backend
mkdir -p uploads
mkdir -p feedback

# Start backend server in the background
echo -e "${GREEN}Starting backend server on http://localhost:8000${NC}"
./start_backend.sh &
BACKEND_PID=$!

# Wait a bit for backend to start
sleep 2

# Start frontend server
echo -e "${GREEN}Starting frontend server on http://localhost:3000${NC}"
./start_frontend.sh

# Clean up when script is terminated
trap 'echo -e "${YELLOW}Shutting down servers...${NC}" && kill $BACKEND_PID' EXIT 
#!/bin/bash

# Color variables
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Starting BrainClassify Frontend ===${NC}"

# Navigate to frontend directory 
cd frontend

# Check for node_modules and install dependencies if needed
if [ ! -d "node_modules" ] || [ ! -f "node_modules/.package-lock.json" ]; then
    echo -e "${YELLOW}Installing frontend dependencies...${NC}"
    npm install
fi

# Generate PostCSS and Tailwind CSS files if they don't exist
if [ ! -f "postcss.config.js" ]; then
    echo -e "${YELLOW}Creating PostCSS config...${NC}"
    echo "module.exports = { plugins: { tailwindcss: {}, autoprefixer: {}, } }" > postcss.config.js
fi

# Make sure Tailwind is initialized
if [ ! -f "tailwind.config.js" ]; then
    echo -e "${YELLOW}Initializing Tailwind CSS...${NC}"
    npx tailwindcss init
fi

# Start the frontend dev server
echo -e "${GREEN}Starting React development server...${NC}"
npm start 
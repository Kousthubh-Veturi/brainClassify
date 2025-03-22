#!/bin/bash

# Color variables
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Track if there are any errors/warnings
has_errors=false
has_warnings=false

# Function to check if a file exists
check_file() {
    local file="$1"
    local is_critical="${2:-true}"
    
    if [ -f "$file" ]; then
        echo -e "  ${GREEN}✓${NC} $file"
        return 0
    else
        if [ "$is_critical" = true ]; then
            echo -e "  ${RED}✗${NC} $file ${RED}(MISSING - CRITICAL)${NC}"
            has_errors=true
        else
            echo -e "  ${YELLOW}⚠${NC} $file ${YELLOW}(MISSING - OPTIONAL)${NC}"
            has_warnings=true
        fi
        return 1
    fi
}

# Function to check if a directory exists
check_dir() {
    local dir="$1"
    local is_critical="${2:-true}"
    
    if [ -d "$dir" ]; then
        echo -e "  ${GREEN}✓${NC} $dir"
        return 0
    else
        if [ "$is_critical" = true ]; then
            echo -e "  ${RED}✗${NC} $dir ${RED}(MISSING - CRITICAL)${NC}"
            has_errors=true
        else
            mkdir -p "$dir"
            echo -e "  ${YELLOW}⚠${NC} $dir ${YELLOW}(CREATED)${NC}"
            has_warnings=true
        fi
        return 1
    fi
}

# Function to check if a script has execute permissions
check_executable() {
    local script="$1"
    
    if [ -x "$script" ]; then
        echo -e "  ${GREEN}✓${NC} $script is executable"
        return 0
    else
        echo -e "  ${YELLOW}⚠${NC} $script ${YELLOW}(NOT EXECUTABLE - FIXING)${NC}"
        chmod +x "$script"
        has_warnings=true
        return 1
    fi
}

# Function to check for potential API connectivity issues
check_api_connectivity() {
    echo -e "\n${BLUE}Checking API connectivity...${NC}"
    
    # Check if curl is installed
    if ! command -v curl &> /dev/null; then
        echo -e "  ${YELLOW}⚠${NC} curl is not installed, skipping API connectivity check"
        has_warnings=true
        return 1
    fi
    
    # Try to access the backend API
    local response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health 2>/dev/null || echo "failed")
    
    if [ "$response" = "failed" ]; then
        echo -e "  ${YELLOW}⚠${NC} Backend API is not running (http://localhost:8000)"
        echo -e "  ${YELLOW}⚠${NC} Run './start_backend.sh' to start the backend server"
        has_warnings=true
        return 1
    elif [ "$response" = "200" ]; then
        echo -e "  ${GREEN}✓${NC} Backend API is running and accessible"
        
        # Check CORS headers
        local cors_headers=$(curl -s -I -X OPTIONS http://localhost:8000/health -H "Origin: http://localhost:3000" | grep -i "Access-Control-Allow" || echo "")
        
        if [ -z "$cors_headers" ]; then
            echo -e "  ${YELLOW}⚠${NC} CORS headers might not be properly configured on the backend"
            echo -e "  ${YELLOW}⚠${NC} This might cause blank screens or API errors in the frontend"
            has_warnings=true
        else
            echo -e "  ${GREEN}✓${NC} CORS headers are present"
        fi
        
        return 0
    else
        echo -e "  ${YELLOW}⚠${NC} Backend API returned unexpected status code: $response"
        has_warnings=true
        return 1
    fi
}

# Clear screen
clear

echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}    BrainClassify Setup Verification     ${NC}"
echo -e "${GREEN}=========================================${NC}"

# Check essential directories
echo -e "\n${BLUE}Checking essential directories...${NC}"
check_dir "uploads" false
check_dir "feedback" false

# Check frontend files
echo -e "\n${BLUE}Checking frontend files...${NC}"
check_file "frontend/src/index.js"
check_file "frontend/src/App.js"
check_file "frontend/src/index.css"
check_file "frontend/package.json"
check_file "frontend/public/index.html"
check_file "frontend/public/favicon.ico" false

# Check frontend components
echo -e "\n${BLUE}Checking frontend components...${NC}"
check_file "frontend/src/components/FeedbackForm.js"
check_file "frontend/src/components/ImageUpload.js"
check_file "frontend/src/components/PredictionResult.js"
check_file "frontend/src/services/api.js"
check_file "frontend/src/pages/UploadPage.js"
check_file "frontend/src/pages/ResultsPage.js"
check_file "frontend/src/config.js"

# Check backend files
echo -e "\n${BLUE}Checking backend files...${NC}"
check_file "backend/app/main.py"
check_file "backend/requirements.txt"
check_file "backend/app/routes/upload.py"
check_file "backend/app/routes/predict.py"
check_file "backend/app/services/image_service.py"
check_file "backend/app/services/model_service.py"
check_file "backend/.env" false

# Check script permissions
echo -e "\n${BLUE}Checking script permissions...${NC}"
check_executable "run.sh"
check_executable "start_frontend.sh"
check_executable "start_backend.sh"

# Check for potential API connectivity and CORS issues
check_api_connectivity

# Final summary
echo -e "\n${BLUE}Verification summary:${NC}"
if [ "$has_errors" = true ]; then
    echo -e "${RED}✗ Errors found! Please fix the critical issues before continuing.${NC}"
    echo -e "${RED}  The application may not work correctly without these files.${NC}"
    exit 1
elif [ "$has_warnings" = true ]; then
    echo -e "${YELLOW}⚠ Warnings found, but you can still run the application.${NC}"
    echo -e "${YELLOW}  Consider fixing these issues for optimal operation.${NC}"
    echo -e "\n${GREEN}To start the application, run:${NC}"
    echo -e "  ./run.sh"
    exit 0
else
    echo -e "${GREEN}✓ All checks passed! Your setup looks good.${NC}"
    echo -e "\n${GREEN}To start the application, run:${NC}"
    echo -e "  ./run.sh"
    exit 0
fi 
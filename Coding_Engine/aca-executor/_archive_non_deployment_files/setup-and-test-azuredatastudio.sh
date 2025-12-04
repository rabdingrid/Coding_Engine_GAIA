#!/bin/bash
# Setup and Test Azure Data Studio with Azure PostgreSQL

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}🚀 Azure Data Studio Setup & Test${NC}"
echo "=========================================="
echo ""

# Check OS
OS=$(uname -s)
echo -e "${YELLOW}📋 Detected OS: $OS${NC}"
echo ""

# Download Azure Data Studio
if [ "$OS" = "Darwin" ]; then
    echo -e "${YELLOW}📦 Step 1: Downloading Azure Data Studio for macOS...${NC}"
    if [ ! -f azure-data-studio.zip ]; then
        curl -L -o azure-data-studio.zip "https://azuredatastudio-update.azurewebsites.net/latest/darwin/zip"
        echo -e "${GREEN}✅ Download complete!${NC}"
    else
        echo -e "${GREEN}✅ Already downloaded${NC}"
    fi
    
    echo ""
    echo -e "${YELLOW}📦 Step 2: Extracting...${NC}"
    if [ ! -d "azure-data-studio" ]; then
        unzip -q azure-data-studio.zip
        echo -e "${GREEN}✅ Extracted!${NC}"
    else
        echo -e "${GREEN}✅ Already extracted${NC}"
    fi
    
    echo ""
    echo -e "${YELLOW}🚀 Step 3: Opening Azure Data Studio...${NC}"
    APP_PATH=$(find azure-data-studio -name "Azure Data Studio.app" -type d 2>/dev/null | head -1)
    if [ -n "$APP_PATH" ]; then
        open "$APP_PATH"
        echo -e "${GREEN}✅ Azure Data Studio is opening!${NC}"
    else
        echo -e "${RED}❌ Could not find Azure Data Studio.app${NC}"
        exit 1
    fi

elif [ "$OS" = "Linux" ]; then
    echo -e "${YELLOW}📦 Step 1: Downloading Azure Data Studio for Linux...${NC}"
    if [ ! -f azure-data-studio.tar.gz ]; then
        curl -L -o azure-data-studio.tar.gz "https://azuredatastudio-update.azurewebsites.net/latest/linux-x64/archive"
        echo -e "${GREEN}✅ Download complete!${NC}"
    else
        echo -e "${GREEN}✅ Already downloaded${NC}"
    fi
    
    echo ""
    echo -e "${YELLOW}📦 Step 2: Extracting...${NC}"
    if [ ! -d "azure-data-studio" ]; then
        tar -xzf azure-data-studio.tar.gz
        echo -e "${GREEN}✅ Extracted!${NC}"
    else
        echo -e "${GREEN}✅ Already extracted${NC}"
    fi
    
    echo ""
    echo -e "${YELLOW}🚀 Step 3: Starting Azure Data Studio...${NC}"
    EXEC_PATH=$(find azure-data-studio -name "azuredatastudio" -type f 2>/dev/null | head -1)
    if [ -n "$EXEC_PATH" ]; then
        "$EXEC_PATH" &
        echo -e "${GREEN}✅ Azure Data Studio is starting!${NC}"
    else
        echo -e "${RED}❌ Could not find azuredatastudio executable${NC}"
        exit 1
    fi
else
    echo -e "${RED}❌ Unsupported OS: $OS${NC}"
    echo "Please download manually from: https://aka.ms/azuredatastudio"
    exit 1
fi

echo ""
echo "=========================================="
echo -e "${GREEN}📋 Connection Details for Azure Data Studio:${NC}"
echo "=========================================="
echo ""
echo "Server: ai-ta-ra-postgre.postgres.database.azure.com"
echo "Database: railway"
echo "Username: postgresadmin"
echo "Password: 5oXcNX59QmEl7zmV3DbjemkiJ"
echo "SSL: ✅ Enable (Required)"
echo ""
echo "=========================================="
echo ""
echo -e "${YELLOW}📝 Next Steps in Azure Data Studio:${NC}"
echo ""
echo "1. Install PostgreSQL Extension:"
echo "   - Click Extensions icon (left sidebar)"
echo "   - Search 'PostgreSQL'"
echo "   - Install 'PostgreSQL' by Microsoft"
echo ""
echo "2. Connect to Database:"
echo "   - Click 'New Connection' (left sidebar)"
echo "   - Connection type: PostgreSQL"
echo "   - Use connection details above"
echo "   - ✅ Enable SSL"
echo "   - Click 'Connect'"
echo ""
echo "3. Test Connection:"
echo "   - Expand: Connection → Databases → railway → Tables"
echo "   - Click 'coding_question_bank' table"
echo "   - Right-click → 'Select Top 1000'"
echo ""
echo "4. Run Test Queries:"
echo "   - Click 'New Query'"
echo "   - Open: test-queries.sql"
echo "   - Run queries (F5)"
echo ""
echo -e "${GREEN}✅ Setup complete! Azure Data Studio should be opening now.${NC}"
echo ""


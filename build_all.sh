#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Define colors for output
INFO='\033[0;34m'
SUCCESS='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${INFO}>>> Starting build process with uv...${NC}"

# 1. Cleanup
echo -e "${INFO}Step 1: Cleaning up old artifacts...${NC}"
rm -rf dist/
rm -rf pepedd-core/dist pepedd-nodes/dist

# 2. Build pepedd (CORE)
echo -e "${INFO}Step 2: Building pepedd-core...${NC}"
cd pepedd-core
uv build
cd ..

# 3. Build pepedd-nodes (NODES)
echo -e "${INFO}Step 3: Building pepedd-nodes...${NC}"
cd pepedd-nodes
uv build
cd ..

# 4. Consolidate distributions
echo -e "${INFO}Step 4: Consolidating wheels to ./dist...${NC}"
mkdir -p dist
cp pepedd-core/dist/* dist/
cp pepedd-nodes/dist/* dist/

# 5. Verify results
echo -e "${SUCCESS}>>> Build successful! Artifacts located in ./dist${NC}"
ls -lh dist/
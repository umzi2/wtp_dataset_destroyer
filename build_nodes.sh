#!/bin/bash
set -e
rm -rf dist/
rm -rf .temp_pepe_nodes/ dist/
mkdir -p .temp_pepe_nodes/pepedd
cp -r pepedd/nodes .temp_pepe_nodes/pepedd/
mv .temp_pepe_nodes/pepedd/nodes/pyproject.toml .temp_pepe_nodes/pyproject.toml
cd .temp_pepe_nodes
uv build
cd ..
mkdir -p dist
mv .temp_pepe_nodes/dist/* dist/
rm -rf .temp_pepe_nodes/
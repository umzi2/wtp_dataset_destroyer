#!/bin/bash
set -e
rm -rf dist/
rm -rf .temp_pepe_core/ dist/
mkdir -p .temp_pepe_core/pepedd
cp -r pepedd/core .temp_pepe_core/pepedd/
cp -r pepedd/__init__.py .temp_pepe_core/pepedd/
mv .temp_pepe_core/pepedd/core/pyproject.toml .temp_pepe_core/pyproject.toml
cd .temp_pepe_core
uv build
cd ..
mkdir -p dist
mv .temp_pepe_core/dist/* dist/
rm -rf .temp_pepe_core/
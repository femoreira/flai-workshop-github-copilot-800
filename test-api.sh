#!/bin/bash

# API Testing Script for OctoFit Tracker
# This script tests all REST API endpoints

echo "========================================="
echo "Testing OctoFit Tracker API"
echo "========================================="

# Get Codespace name
CODESPACE_NAME=${CODESPACE_NAME}

if [ -n "$CODESPACE_NAME" ]; then
    BASE_URL="https://${CODESPACE_NAME}-8000.app.github.dev"
    echo "Testing on Codespace: $BASE_URL"
else
    BASE_URL="http://localhost:8000"
    echo "Testing on localhost: $BASE_URL"
fi

echo ""
echo "========================================="
echo "1. Testing API Root"
echo "========================================="
curl -s "${BASE_URL}/api/" | python -m json.tool 2>/dev/null || curl -s "${BASE_URL}/api/"

echo ""
echo ""
echo "========================================="
echo "2. Testing Teams Endpoint"
echo "========================================="
curl -s "${BASE_URL}/api/teams/" | python -m json.tool 2>/dev/null || curl -s "${BASE_URL}/api/teams/"

echo ""
echo ""
echo "========================================="
echo "3. Testing Users Endpoint"
echo "========================================="
curl -s "${BASE_URL}/api/users/" | python -m json.tool 2>/dev/null || curl -s "${BASE_URL}/api/users/"

echo ""
echo ""
echo "========================================="
echo "4. Testing Activities Endpoint"
echo "========================================="
curl -s "${BASE_URL}/api/activities/" | python -m json.tool 2>/dev/null || curl -s "${BASE_URL}/api/activities/"

echo ""
echo ""
echo "========================================="
echo "5. Testing Leaderboard Endpoint"
echo "========================================="
curl -s "${BASE_URL}/api/leaderboard/" | python -m json.tool 2>/dev/null || curl -s "${BASE_URL}/api/leaderboard/"

echo ""
echo ""
echo "========================================="
echo "6. Testing Workouts Endpoint"
echo "========================================="
curl -s "${BASE_URL}/api/workouts/" | python -m json.tool 2>/dev/null || curl -s "${BASE_URL}/api/workouts/"

echo ""
echo ""
echo "========================================="
echo "Testing Complete!"
echo "========================================="

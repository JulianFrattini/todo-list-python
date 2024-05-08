#!/bin/bash

# MongoDB
mongod --port 27017 --dbpath data/db &

# Wait for MongoDB to initiate
sleep 5

# Start Backend
cd backend/
python3 ./main.py &

# Start Frontend
cd ../frontend/
npm start

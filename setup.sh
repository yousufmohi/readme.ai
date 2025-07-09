#!/bin/bash

echo "Setting up server..."

cd server

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

cd ..

echo "Setting up client..."

cd client

npm install

cd ..

echo "All set!"
echo "Activate the venv and run 'fastapi dev main.py' to start the backend."
echo "Run 'cd client && npm run dev' to start the frontend."

Write-Host "Setting up backend..."

# Navigate to server folder
Set-Location server

# Create virtual environment in ./server/venv
python -m venv venv

# Activate virtual environment
& .\venv\Scripts\Activate

# Install backend dependencies
pip install -r requirements.txt

# Go back to project root
Set-Location ..

Write-Host "🌐 Setting up frontend..."

# Navigate to client folder
Set-Location client

# Install frontend dependencies
npm install

# Go back to root (optional)
Set-Location ..

Write-Host "All set!"
Write-Host "Run 'fastapi dev main.py' from inside the 'server' directory."
Write-Host "Run 'npm run dev' from inside the 'client' directory."

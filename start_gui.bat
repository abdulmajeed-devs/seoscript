@echo off
echo ========================================
echo SERP Scraper - Quick Start
echo ========================================
echo.
echo Installing dependencies...
python -m pip install -r requirements.txt
echo.
echo ========================================
echo Starting Web GUI...
echo ========================================
echo.
echo The web interface will open at:
echo http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.
python web_gui.py
pause

@echo off
echo =========================================
echo SERP Scraper - Installation Verification
echo =========================================
echo.

echo [1/5] Checking Python installation...
python --version
if %ERRORLEVEL% NEQ 0 (
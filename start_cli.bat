@echo off
echo ========================================
echo SERP Scraper - CLI Version
echo ========================================
echo.
echo Installing dependencies...
python -m pip install -r requirements.txt
echo.
echo ========================================
echo Running SERP Scraper...
echo ========================================
echo.
echo Make sure you have created kw.txt file
echo with your keywords (one per line)
echo.
python serp_scraper.py
echo.
echo ========================================
echo Scraping Complete!
echo Check the 'data' folder for results
echo ========================================
pause

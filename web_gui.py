#!/usr/bin/env python3
"""
SERP Scraper Web GUI
Professional web interface for SERP scraping and NLP entity extraction
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import os
import json
import threading
from pathlib import Path
from datetime import datetime
from serp_scraper import SERPScraper
import zipfile
import io

app = Flask(__name__)
CORS(app)

# Global variables for tracking scraping status
scraping_status = {
    'is_running': False,
    'current_keyword': '',
    'progress': 0,
    'total_keywords': 0,
    'completed_keywords': [],
    'errors': [],
    'start_time': None,
    'results_folder': None
}


def run_scraper_thread(keywords, api_key, country, limit):
    """
    Run scraper in background thread
    """
    global scraping_status
    
    try:
        scraping_status['is_running'] = True
        scraping_status['start_time'] = datetime.now().isoformat()
        scraping_status['total_keywords'] = len(keywords)
        scraping_status['completed_keywords'] = []
        scraping_status['errors'] = []
        
        # Create scraper instance
        scraper = SERPScraper(api_key=api_key, country=country, limit=limit)
        scraping_status['results_folder'] = str(scraper.data_dir)
        
        # Process each keyword
        for idx, keyword in enumerate(keywords, 1):
            scraping_status['current_keyword'] = keyword
            scraping_status['progress'] = int((idx / len(keywords)) * 100)
            
            try:
                scraper.process_keyword(keyword)
                scraping_status['completed_keywords'].append({
                    'keyword': keyword,
                    'status': 'success',
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                error_msg = f"Error processing '{keyword}': {str(e)}"
                scraping_status['errors'].append(error_msg)
                scraping_status['completed_keywords'].append({
                    'keyword': keyword,
                    'status': 'error',
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                })
        
        scraping_status['progress'] = 100
        scraping_status['current_keyword'] = 'Complete'
        
    except Exception as e:
        scraping_status['errors'].append(f"Fatal error: {str(e)}")
    finally:
        scraping_status['is_running'] = False


@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')


@app.route('/api/start-scraping', methods=['POST'])
def start_scraping():
    """
    Start scraping process
    """
    global scraping_status
    
    if scraping_status['is_running']:
        return jsonify({
            'success': False,
            'message': 'Scraping is already in progress'
        }), 400
    
    data = request.json
    keywords_text = data.get('keywords', '').strip()
    api_key = data.get('api_key', '').strip()
    country = data.get('country', 'US').strip()
    limit = int(data.get('limit', 10))
    
    if not keywords_text:
        return jsonify({
            'success': False,
            'message': 'Please provide at least one keyword'
        }), 400
    
    if not api_key:
        return jsonify({
            'success': False,
            'message': 'Please provide an API key'
        }), 400
    
    # Parse keywords
    keywords = [k.strip() for k in keywords_text.split('\n') if k.strip()]
    
    # Start scraping in background thread
    thread = threading.Thread(
        target=run_scraper_thread,
        args=(keywords, api_key, country, limit)
    )
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'success': True,
        'message': f'Started scraping {len(keywords)} keywords'
    })


@app.route('/api/status', methods=['GET'])
def get_status():
    """
    Get current scraping status
    """
    return jsonify(scraping_status)


@app.route('/api/stop-scraping', methods=['POST'])
def stop_scraping():
    """
    Stop scraping process (note: this is a graceful request, thread may continue)
    """
    global scraping_status
    scraping_status['is_running'] = False
    
    return jsonify({
        'success': True,
        'message': 'Scraping stopped'
    })


@app.route('/api/results', methods=['GET'])
def get_results():
    """
    Get list of result folders
    """
    data_dir = Path.cwd() / "data"
    
    if not data_dir.exists():
        return jsonify({
            'success': True,
            'results': []
        })
    
    results = []
    for folder in data_dir.iterdir():
        if folder.is_dir():
            # Get files in folder
            files = []
            for file in folder.iterdir():
                if file.is_file() and file.suffix == '.txt':
                    files.append({
                        'name': file.name,
                        'size': file.stat().st_size,
                        'path': str(file.relative_to(Path.cwd()))
                    })
            
            results.append({
                'keyword': folder.name,
                'path': str(folder.relative_to(Path.cwd())),
                'file_count': len(files),
                'files': files
            })
    
    return jsonify({
        'success': True,
        'results': results
    })


@app.route('/api/download/<path:filepath>', methods=['GET'])
def download_file(filepath):
    """
    Download a specific file
    """
    try:
        file_path = Path.cwd() / filepath
        if file_path.exists() and file_path.is_file():
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({
                'success': False,
                'message': 'File not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/download-all/<keyword>', methods=['GET'])
def download_all(keyword):
    """
    Download all files for a keyword as ZIP
    """
    try:
        data_dir = Path.cwd() / "data" / keyword
        
        if not data_dir.exists():
            return jsonify({
                'success': False,
                'message': 'Folder not found'
            }), 404
        
        # Create ZIP file in memory
        memory_file = io.BytesIO()
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file in data_dir.rglob('*.txt'):
                arcname = file.relative_to(data_dir)
                zf.write(file, arcname)
        
        memory_file.seek(0)
        
        return send_file(
            memory_file,
            mimetype='application/zip',
            as_attachment=True,
            download_name=f'{keyword}_results.zip'
        )
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


def main():
    """
    Start Flask web server
    """
    import sys
    
    # Disable SSL warnings
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    print("\n" + "="*60)
    print("SERP Scraper Web GUI")
    print("="*60)
    print("\nStarting web server...")
    print("\nOpen your browser and navigate to:")
    print("  → http://localhost:5000")
    print("\nPress Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)


if __name__ == "__main__":
    main()

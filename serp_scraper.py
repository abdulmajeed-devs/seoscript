#!/usr/bin/env python3
"""
SERP Scraper for NLP Entities Extraction
Scrapes Google SERP data and extracts competitor articles for NLP analysis
"""

import http.client
import json
import os
import re
import time
from urllib.parse import urlparse
from pathlib import Path
import ssl

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Required packages not installed. Please run: pip install requests beautifulsoup4")
    exit(1)


class SERPScraper:
    def __init__(self, api_key="653b90312dmsh9219d00db599bf4p1e3706jsn8f0ba5f7b11b", 
                 country="US", limit=10):
        """
        Initialize SERP Scraper
        
        Args:
            api_key: RapidAPI key for Google Search API
            country: Target country code (e.g., US, GB, CA)
            limit: Number of results to fetch per keyword (allowed: 10, 20, 30, 40, 50, 100)
        """
        self.api_key = api_key
        self.country = country.upper()
        # Validate limit - must be one of the allowed values
        valid_limits = [10, 20, 30, 40, 50, 100]
        if limit not in valid_limits:
            print(f"Warning: Invalid limit {limit}. Using 10 instead.")
            limit = 10
        self.limit = limit
        self.api_host = "google-search116.p.rapidapi.com"
        self.root_dir = Path.cwd()
        self.data_dir = self.root_dir / "data"
        
    def read_keywords(self, filename="kw.txt"):
        """
        Read keywords from text file
        
        Args:
            filename: Name of the keyword file
            
        Returns:
            List of keywords
        """
        filepath = self.root_dir / filename
        
        if not filepath.exists():
            print(f"Error: {filename} not found in root directory")
            print(f"Please create {filepath} with one keyword per line")
            return []
        
        with open(filepath, 'r', encoding='utf-8') as f:
            keywords = [line.strip() for line in f if line.strip()]
        
        print(f"Loaded {len(keywords)} keywords from {filename}")
        return keywords
    
    def search_serp(self, query):
        """
        Search Google SERP using RapidAPI
        
        Args:
            query: Search keyword
            
        Returns:
            Dictionary containing search results
        """
        print(f"Searching SERP for: {query}")
        
        try:
            # Create SSL context that doesn't verify certificates (for compatibility)
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            conn = http.client.HTTPSConnection(self.api_host, context=context)
            
            headers = {
                'x-rapidapi-key': self.api_key,
                'x-rapidapi-host': self.api_host
            }
            
            # Build query parameters according to API docs
            # API endpoint is / not /search
            params = f"query={requests.utils.quote(query)}&country={self.country.lower()}&limit={self.limit}"
            endpoint = f"/?{params}"
            
            conn.request("GET", endpoint, headers=headers)
            res = conn.getresponse()
            data = res.read()
            
            # Parse JSON response
            results = json.loads(data.decode("utf-8"))
            
            if "results" in results:
                print(f"Found {len(results['results'])} results")
                return results
            else:
                print(f"No results found or API error: {results}")
                return {"results": []}
                
        except Exception as e:
            print(f"Error searching SERP: {e}")
            return {"results": []}
        finally:
            conn.close()
    
    def extract_article_content(self, url):
        """
        Extract article content from URL
        
        Args:
            url: Article URL
            
        Returns:
            Extracted text content
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10, verify=False)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "header", "footer", "aside"]):
                script.decompose()
            
            # Extract text from paragraphs and main content
            text_elements = []
            
            # Try to find main content area
            main_content = soup.find('main') or soup.find('article') or soup.find('div', class_=re.compile('content|article|post'))
            
            if main_content:
                paragraphs = main_content.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            else:
                paragraphs = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            
            for elem in paragraphs:
                text = elem.get_text(strip=True)
                if text and len(text) > 20:  # Filter out short snippets
                    text_elements.append(text)
            
            content = '\n\n'.join(text_elements)
            
            # Fallback to all text if nothing found
            if not content or len(content) < 500:
                content = soup.get_text(separator='\n\n', strip=True)
            
            return content
            
        except requests.exceptions.Timeout:
            print(f"Timeout extracting content from {url}")
            return ""
        except requests.exceptions.RequestException as e:
            print(f"Error extracting content from {url}: {e}")
            return ""
        except Exception as e:
            print(f"Unexpected error extracting content from {url}: {e}")
            return ""
    
    def sanitize_filename(self, name):
        """
        Sanitize string to be used as filename
        
        Args:
            name: String to sanitize
            
        Returns:
            Sanitized filename string
        """
        # Remove or replace invalid characters
        name = re.sub(r'[<>:"/\\|?*]', '_', name)
        # Remove leading/trailing spaces and dots
        name = name.strip('. ')
        # Limit length
        if len(name) > 100:
            name = name[:100]
        return name
    
    def extract_domain_name(self, url):
        """
        Extract domain name from URL without extension
        
        Args:
            url: Full URL
            
        Returns:
            Domain name without extension
        """
        parsed = urlparse(url)
        domain = parsed.netloc
        
        # Remove www.
        domain = domain.replace('www.', '')
        
        # Remove TLD
        domain = domain.split('.')[0]
        
        return self.sanitize_filename(domain)
    
    def create_folder_structure(self, keyword):
        """
        Create folder structure for keyword
        
        Args:
            keyword: Search keyword
            
        Returns:
            Tuple of (keyword_folder_path, single_articles_folder_path)
        """
        # Create data directory if it doesn't exist
        self.data_dir.mkdir(exist_ok=True)
        
        # Create keyword folder
        keyword_folder_name = self.sanitize_filename(keyword)
        keyword_folder = self.data_dir / keyword_folder_name
        keyword_folder.mkdir(exist_ok=True)
        
        # Create single articles subfolder
        single_articles_folder = keyword_folder / "single_article_files"
        single_articles_folder.mkdir(exist_ok=True)
        
        return keyword_folder, single_articles_folder
    
    def process_keyword(self, keyword):
        """
        Process a single keyword: search SERP and extract articles
        
        Args:
            keyword: Search keyword
        """
        print(f"\n{'='*60}")
        print(f"Processing keyword: {keyword}")
        print(f"{'='*60}")
        
        # Search SERP
        search_results = self.search_serp(keyword)
        
        if not search_results.get('results'):
            print(f"No results found for '{keyword}', skipping...")
            return
        
        # Create folder structure
        keyword_folder, single_articles_folder = self.create_folder_structure(keyword)
        
        # Combined content for all articles
        combined_content = []
        combined_content.append(f"Combined Articles for Keyword: {keyword}")
        combined_content.append(f"Country: {self.country}")
        combined_content.append(f"Total Results: {len(search_results['results'])}")
        combined_content.append(f"{'='*80}\n")
        
        # Process each search result
        for idx, result in enumerate(search_results['results'], 1):
            url = result.get('url', '')
            title = result.get('title', 'No Title')
            position = result.get('position', idx)
            
            if not url:
                continue
            
            print(f"\n[{idx}/{len(search_results['results'])}] Extracting: {title}")
            print(f"URL: {url}")
            
            # Extract article content
            content = self.extract_article_content(url)
            
            if content:
                # Get domain name for filename
                domain_name = self.extract_domain_name(url)
                
                # Add to combined content
                combined_content.append(f"\n{'='*80}")
                combined_content.append(f"Article {idx} - Position: {position}")
                combined_content.append(f"Title: {title}")
                combined_content.append(f"URL: {url}")
                combined_content.append(f"Domain: {domain_name}")
                combined_content.append(f"{'='*80}\n")
                combined_content.append(content)
                combined_content.append(f"\n{'='*80}\n")
                
                # Save individual article file
                individual_filename = f"{domain_name}_{position}.txt"
                individual_filepath = single_articles_folder / individual_filename
                
                try:
                    with open(individual_filepath, 'w', encoding='utf-8') as f:
                        f.write(f"Title: {title}\n")
                        f.write(f"URL: {url}\n")
                        f.write(f"Position: {position}\n")
                        f.write(f"Keyword: {keyword}\n")
                        f.write(f"{'='*80}\n\n")
                        f.write(content)
                    
                    print(f"[OK] Saved to: {individual_filename}")
                except Exception as e:
                    print(f"[ERROR] Error saving individual file: {e}")
            else:
                print(f"[ERROR] Could not extract content")
            
            # Be respectful with requests
            time.sleep(1)
        
        # Save combined file
        combined_filename = f"{self.sanitize_filename(keyword)}_combined.txt"
        combined_filepath = keyword_folder / combined_filename
        
        try:
            with open(combined_filepath, 'w', encoding='utf-8') as f:
                f.write('\n'.join(combined_content))
            
            print(f"\n[OK] Combined file saved: {combined_filename}")
            print(f"[OK] Folder location: {keyword_folder}")
            print(f"[OK] Individual articles: {single_articles_folder}")
        except Exception as e:
            print(f"[ERROR] Error saving combined file: {e}")
    
    def run(self):
        """
        Main execution method
        """
        print("\n" + "="*60)
        print("SERP Scraper for NLP Entities Extraction")
        print("="*60 + "\n")
        
        # Read keywords
        keywords = self.read_keywords()
        
        if not keywords:
            return
        
        print(f"Target Country: {self.country}")
        print(f"Results per keyword: {self.limit}")
        print(f"Total keywords to process: {len(keywords)}\n")
        
        # Process each keyword
        for idx, keyword in enumerate(keywords, 1):
            try:
                self.process_keyword(keyword)
            except Exception as e:
                print(f"Error processing keyword '{keyword}': {e}")
                continue
        
        print("\n" + "="*60)
        print("Scraping Complete!")
        print("="*60)
        print(f"\nAll data saved to: {self.data_dir}")
        print("\nNext Steps:")
        print("1. Check the combined text files for NLP analysis")
        print("2. Review individual article files in 'single_article_files' folders")
        print("3. Extract NLP entities and integrate into your content")


def main():
    """
    Main entry point for CLI usage
    """
    import argparse
    
    parser = argparse.ArgumentParser(
        description="SERP Scraper for NLP Entities Extraction"
    )
    parser.add_argument(
        '--api-key',
        default="653b90312dmsh9219d00db599bf4p1e3706jsn8f0ba5f7b11b",
        help="RapidAPI key for Google Search API"
    )
    parser.add_argument(
        '--country',
        default="US",
        help="Target country code (e.g., US, GB, CA, DE)"
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=10,
        choices=[10, 20, 30, 40, 50, 100],
        help="Number of results to fetch per keyword"
    )
    parser.add_argument(
        '--keywords-file',
        default="kw.txt",
        help="Path to keywords file (default: kw.txt)"
    )
    
    args = parser.parse_args()
    
    # Disable SSL warnings
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    # Create scraper instance
    scraper = SERPScraper(
        api_key=args.api_key,
        country=args.country,
        limit=args.limit
    )
    
    # Override keywords file if specified
    if args.keywords_file != "kw.txt":
        scraper.root_dir = Path.cwd()
    
    # Run scraper
    scraper.run()


if __name__ == "__main__":
    main()

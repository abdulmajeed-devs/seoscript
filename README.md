# SERP Scraper for NLP Entities Extraction

A powerful Python tool for scraping Google Search Engine Results Pages (SERP) to extract competitor articles and analyze NLP entities. Perfect for SEO professionals, content marketers, and anyone looking to integrate competitive NLP entities into their content strategy.

## Key Features

- Keyword-Based Scraping: Read keywords from a text file and process them automatically
- Geo-Targeting: Search in specific countries (US, GB, CA, AU, DE, FR, IN, JP, BR, etc.)
- Multiple Results: Extract 10-100 competitor articles per keyword
- Organized Output: Automatic folder structure creation with keyword-based organization
- Combined & Individual Files: Get both a combined analysis file and individual competitor articles 
- Professional Web GUI: Clean, responsive web interface for easy operation
- Real-Time Progress: Track scraping progress with live updates
- Easy Downloads: Download individual files or entire keyword results as ZIP collections

## Benefits and Use Cases

- NLP Entity Extraction: Analyze competitor content to identify common entities, terms, and topics to match algorithm preferences.
- Content Gap Analysis: Discover what subtopics your competitors are writing about that you might be missing.
- SEO Research: Understand top-ranking content structure, themes, and word counts.
- Content Strategy: Integrate competitive insights directly into your content planning and strategy map.
- Topic Modeling: Build comprehensive topic models from top-ranking pages to establish topical authority.

## Requirements

- Python 3.7 or higher
- RapidAPI account with Google Search API access
- Internet connection

## Installation

1. Clone or download this repository locally.

2. Install the necessary dependencies:
pip install -r requirements.txt

3. Obtain your RapidAPI key:
- Sign up at RapidAPI
- Subscribe to the Google Search API (ScraperLink)
- Copy your API key from the dashboard

## Usage

### Method 1: Web GUI (Recommended)

1. Start the web server:
python web_gui.py

2. Open your browser and navigate to:
http://localhost:5000

3. Configure and run:
- Enter your keywords (one per line)
- Paste your RapidAPI key
- Select the target country
- Choose the number of results per keyword
- Click 'Start Scraping'
- Monitor progress in real-time
- Download results when complete in either individual or bulk ZIP format

### Method 2: Command Line Interface

1. Create a keywords file:
Create a file named kw.txt in the root directory with your keywords (one per line):
best running shoes for marathon
nike air max review
content marketing strategies 2024

2. Run the scraper:
python serp_scraper.py

Available advanced options:
- --api-key: Your RapidAPI key
- --country: Target country code (default: US)
- --limit: Results per keyword (10, 20, 30, 40, 50, or 100, default: 10)
- --keywords-file: Path to keywords file (default: kw.txt)

Example with custom options:
python serp_scraper.py --api-key YOUR_API_KEY --country GB --limit 20

## Output Structure

The scraper creates the following folder structure:

data/
├── keyword_name/
│   ├── keyword_name_combined.txt
│   └── single_article_files/
│       ├── domain1_1.txt
│       ├── domain2_2.txt
│       └── domain3_3.txt

Combined File format includes:
- Keyword and country information
- Total number of results
- All competitor articles with metadata (title, URL, position) sequentially combined for quick NLP tool importing

Individual Files format include:
- Article title and URL
- Search position
- Keyword used
- Full extracted content

## Advanced Features and Configuration

- Batch Processing Multiple Keyword Lists: You can specify different keyword text files per run.
- Multi-Country Analysis: Run the same keywords across different countries to track location-specific rankings.
- Deep Competitor Analysis: Get maximum results (limit 100) for a comprehensive overview of the entire landscape.
- Programmatic Integration: You can import the SERPScraper class in your own Python scripts to extend functionality.

## Best Practices

- Keyword Selection: Start with specific, targeted commercial long-tail keywords. Test with 2-3 before running large lists.
- API Usage: Monitor your quota and start on the free tier to familiarize yourself with the service. Rate limits are built-in.
- Data Quality: Always do a quick manual check of the extracted content before running it through NLP modeling tools. Keep data organized by campaign.

## Troubleshooting

- Required packages not installed: Run 'pip install --upgrade pip' followed by 'pip install -r requirements.txt'.
- kw.txt not found: Create the file in the root directory and ensure it has at least one keyword.
- API key invalid or expired: Verify your key in the RapidAPI dashboard, check quota, and ensure there are no copy-paste errors.
- Timeout extracting content: Some target websites might be unusually slow or blocking requests. The script will continue to the next one automatically.
- Port 5000 already in use: Stop other services using the port or manually change the port assignment in the web_gui.py file.
- SSL Certificate Error: Standard warnings are disabled, but local secure network configs may interfere.

## API Information and Security

This tool utilizes the Google Search API from RapidAPI:
- Supplies real-time Google SERP data with geo-targeted results and proper proxy handling.
- Never commit your API key to version control or share it publicly.
- Store keys inside environment variables or .env files for production workloads.
- The default placeholder keys in code are strictly for demonstration.

## License

This project is provided as-is for educational and commercial use.

## Contributing and Support

Contributions, issues, and feature requests are welcome.
For issues or questions:
1. Check the troubleshooting section.
2. Review the RapidAPI documentation.
3. Open an issue in the repository.

Acknowledgments to Google Search API by ScraperLink, the Flask web framework, Beautiful Soup, and the larger Python community.

# SERP Scraper Configuration
# Copy this file to config.py and customize as needed

# RapidAPI Configuration
RAPIDAPI_KEY = "653b90312dmsh9219d00db599bf4p1e3706jsn8f0ba5f7b11b"
RAPIDAPI_HOST = "google-search116.p.rapidapi.com"

# Default Search Settings
DEFAULT_COUNTRY = "US"  # US, GB, CA, AU, DE, FR, IN, JP, BR, etc.
DEFAULT_LIMIT = 10      # 10, 20, 30, 40, 50, or 100

# File Settings
KEYWORDS_FILE = "kw.txt"
OUTPUT_DIRECTORY = "data"

# Web GUI Settings
WEB_HOST = "0.0.0.0"
WEB_PORT = 5000
WEB_DEBUG = False

# Request Settings
REQUEST_TIMEOUT = 10    # seconds
REQUEST_DELAY = 1       # seconds between requests (be respectful)

# Content Extraction Settings
MIN_CONTENT_LENGTH = 500    # minimum content length in characters
MIN_PARAGRAPH_LENGTH = 20   # minimum paragraph length

# Supported Countries (ISO 3166 A-2)
SUPPORTED_COUNTRIES = [
    "US", "GB", "CA", "AU", "DE", "FR", "IN", "JP", "BR",
    "IT", "ES", "MX", "AR", "NL", "SE", "CH", "AT", "BE",
    "PL", "TR", "RU", "ZA", "KR", "TW", "SG", "MY", "TH",
    "ID", "PH", "VN", "AE", "SA", "EG", "NG", "KE"
]

# Supported Result Limits
SUPPORTED_LIMITS = [10, 20, 30, 40, 50, 100]

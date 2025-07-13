class ScraperConfig:
    # Website settings
    BASE_URL = "https://elpais.com"
    OPINION_URL = f"{BASE_URL}/opinion/"
    MAX_ARTICLES = 5

    # File settings
    DOWNLOAD_FOLDER = "article_images"

    # Translation settings
    SOURCE_LANG = 'es'
    TARGET_LANG = 'en'
    TRANSLATION_RETRIES = 3

    # Browser settings
    BROWSER_OPTIONS = ["--start-maximized"]

    # Headers
    DEFAULT_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8'
    }
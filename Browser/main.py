from selenium.webdriver.common.by import By
from config.settings import ScraperConfig
from utils.translator import Translator
from utils.analyzer import TextAnalyzer
from utils.file_handler import FileHandler
from scraper.web_scraper import *
import time

class ElPaisScraper:
    def __init__(self, driver):
        self.config = ScraperConfig()
        self.translator = Translator(
            source_lang=self.config.SOURCE_LANG,
            target_lang=self.config.TARGET_LANG,
            max_retries=self.config.TRANSLATION_RETRIES
        )
        self.analyzer = TextAnalyzer(min_repetitions=2)
        self.file_handler = FileHandler(self.config.DOWNLOAD_FOLDER)

        # Always use the injected BrowserStack driver
        self.scraper = WebScraper(driver=driver, config=self.config)

    def process_articles(self):
        articles = []
        translated_titles = []

        try:
            self.scraper.driver.get(self.config.OPINION_URL)

            article_elements = self.scraper.get_articles(
                "//div[@class='z z-hi']/section[1]//div/article",
                self.config.MAX_ARTICLES
            )

            for idx, element in enumerate(article_elements, 1):
                try:
                    title = element.find_element(By.XPATH, ".//h2/a").get_attribute("innerText").strip()
                    url = element.find_element(By.XPATH, ".//h2/a").get_attribute("href")
                    translated = self.translator.translate(title)
                    translated_titles.append(translated)

                    content = self.scraper.get_article_content(url)

                    image_url = self.scraper.get_image_url(element)
                    image_path = self.file_handler.download_image(
                        image_url, title,
                        headers=self.config.DEFAULT_HEADERS
                    ) if image_url else None

                    article = scraper.web_scraper.Article(
                        title=title,
                        url=url,
                        content=content,
                        image_path=image_path,
                        translated_title=translated
                    )
                    articles.append(article)

                    self._print_article_info(idx, article)
                    time.sleep(1.5)

                except Exception as e:
                    print(f"Error processing article {idx}: {e}")

            self._analyze_translations(translated_titles)

        finally:
            self.scraper.close()

        return articles

    def _print_article_info(self, idx, article):
        print(f"\nArticle {idx}:")
        print("=" * 50)
        print(f"Title: {article.title}")
        print(f"Translated: {article.translated_title}")
        print(f"content:{article.content}")
        print(f"URL: {article.url}")
        if article.image_path:
            print(f"Image: {article.image_path}")
        print("=" * 50)

    def _analyze_translations(self, translated_titles):
        repeated_words = self.analyzer.analyze_repeated_words(translated_titles)
        if repeated_words:
            print("\nRepeated words in translations:")
            for word, count in repeated_words.items():
                print(f"'{word}' appears {count} times")
        else:
            print("\nNo words repeated more than twice in translations")


# This will be used by parallel_test.py or test_run_scraper.py
def run_scraper(driver):
    scraper = ElPaisScraper(driver)
    articles = scraper.process_articles()
    print(f"\nProcessed {len(articles)} articles")
    print(f"Images saved in '{ScraperConfig.DOWNLOAD_FOLDER}' folder")

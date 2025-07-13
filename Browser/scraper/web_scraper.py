from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests

class Article:
    def __init__(self, title, url, content=None, image_path=None, translated_title=None):
        self.title = title
        self.url = url
        self.content = content
        self.image_path = image_path
        self.translated_title = translated_title

    def to_dict(self):
        return {
            "title": self.title,
            "translated_title": self.translated_title,
            "content": self.content,
            "url": self.url,
            "image_path": self.image_path
        }

class WebScraper:
    def __init__(self, service=None, options=None, config=None, driver=None):
        self.config = config

        if driver:
            self.driver = driver
        else:
            self.driver = webdriver.Firefox(service=service, options=options)

        self.wait = WebDriverWait(self.driver, 10)

    def get_article_content(self, url):
        try:
            response = requests.get(url, headers=self.config.DEFAULT_HEADERS)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Try to find content with different possible selectors
            content = soup.find('div', class_='a_c clearfix')
            if not content:
                content = soup.find('div', class_='article_body')
            if not content:
                content = soup.find('div', attrs={'data-dtm-region': 'articulo_cuerpo'})

            if content:
                # Get text content and clean it up
                text_content = content.get_text(separator=' ', strip=True)
                return text_content
            else:
                return "Content not found"

        except Exception as e:
            return f"Error retrieving content: {str(e)}"

    def get_image_url(self, article):
        image_xpath_options = [
            ".//div[contains(@class,'a_e_m')]//img",
            ".//img[contains(@class,'_re')]",
            ".//img[contains(@class,'a_m-h')]",
            ".//img"
        ]

        for xpath in image_xpath_options:
            try:
                image_element = article.find_element(By.XPATH, xpath)
                if image_element:
                    srcset = image_element.get_attribute("srcset")
                    if srcset:
                        return srcset.split(',')[-1].strip().split(' ')[0]
                    return image_element.get_attribute("src")
            except:
                continue
        return None

    def get_articles(self, xpath_pattern, count):
        return [
            self.wait.until(EC.presence_of_element_located(
                (By.XPATH, f"{xpath_pattern}[{i}]")))
            for i in range(1, count + 1)
        ]

    def close(self):
        self.driver.quit()

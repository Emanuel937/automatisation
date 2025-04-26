# fetcher.py
from playwright.sync_api import sync_playwright

class PlaywrightFetcher:
    def __init__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.firefox.launch(headless=True)  # Firefox en mode headless
        self.context = self.browser.new_context()

    def fetch_html(self, url, css_selector):
        try:
            page = self.context.new_page()
            page.goto(url)
            page.wait_for_selector(css_selector, timeout=10000)  # 4s max pour trouver l’élément
            element = page.query_selector(css_selector)
            html_content = element.inner_html() if element else None
            page.close()  # Ferme la page mais garde le contexte
            return html_content
        except Exception as error:
            print(f"Erreur pour {url} : {error}")
            return None

    def close(self):
        self.context.close()
        self.browser.close()
        self.playwright.stop()
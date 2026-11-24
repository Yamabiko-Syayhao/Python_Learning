from bs4 import BeautifulSoup
from htm import html
import html2text

class HTMLProcessor:
    NOISE_TAGS = ['ul', 'li', 'header', 'nav', 'p']

    def clean_dom(self, soup):
        for tag in soup(self.NOISE_TAGS):
            tag.decompose()
        return soup

    def extract_tables(self, soup):
        tables = []
        for table in soup.find_all("table"):
            rows = []
            for tr in table.find_all("tr"):
                cells = tr.find_all(["th", "td"])
                rows.append([c.get_text(strip=True) for c in cells])
            tables.append(rows)
        return tables

    def to_markdown(self, html_str):
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        h.body_width = 0 # 关闭自动换行
        return h.handle(html_str)

    def process(self, html_str):
        soup = BeautifulSoup(html_str, "lxml")
        soup = self.clean_dom(soup)
        tables = self.extract_tables(soup)
        markdown = self.to_markdown(str(soup))
        return {
            "markdown": markdown,
            "tables": tables,
        }

pro = HTMLProcessor()
result = pro.process(html)
print(result["markdown"])
print(result["tables"])
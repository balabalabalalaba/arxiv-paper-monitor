import requests
from datetime import datetime, timedelta
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class PRLFetcher:
    BASE_URL = "https://journals.aps.org/feeds/rss.xml"

    def __init__(self, keywords):
        self.keywords = keywords

    def fetch_recent_papers(self, days_back: int = 1) -> List[Dict]:
        try:
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=days_back)

            params = {
                "journal": "PRL",
                "search": " OR ".join(self.keywords),
            }

            response = requests.get(self.BASE_URL, params=params, timeout=20)
            response.raise_for_status()

            return self._parse_rss(response.text, start_date)

        except Exception as e:
            logger.error(f"PRL 获取失败: {e}")
            return []

    def _parse_rss(self, xml_text, start_date):
        import feedparser

        feed = feedparser.parse(xml_text)
        papers = []

        for entry in feed.entries:
            pub_time = datetime(*entry.published_parsed[:6])

            if pub_time < start_date:
                continue

            paper = {
                'id': entry.id,
                'title': entry.title,
                'authors': [a.name for a in entry.authors] if hasattr(entry, 'authors') else [],
                'abstract': entry.summary,
                'pdf_url': entry.links[0].href.replace('abstract', 'pdf'),
                'published': pub_time.strftime('%Y-%m-%d %H:%M'),
                'primary_category': 'PRL',
                'categories': ['PRL'],
                'arxiv_url': entry.link,
            }

            papers.append(paper)

        return papers

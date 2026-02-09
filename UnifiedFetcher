class UnifiedPaperFetcher:
    def __init__(self):
        self.arxiv = ArxivFetcher()
        self.prl = PRLFetcher(Config.SEARCH_KEYWORDS)

    def fetch_all(self, days_back=1):
        arxiv_papers = self.arxiv.fetch_recent_papers(days_back)
        prl_papers = self.prl.fetch_recent_papers(days_back)

        all_papers = arxiv_papers + prl_papers

        # 基于 title 去重
        seen = set()
        unique = []
        for p in all_papers:
            t = p['title'].lower().strip()
            if t not in seen:
                seen.add(t)
                unique.append(p)

        return unique

    def generate_summary(self, paper):
        return self.arxiv.generate_summary(paper)

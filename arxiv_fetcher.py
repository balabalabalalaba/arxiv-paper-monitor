import arxiv
from datetime import datetime, timedelta
from typing import List, Dict
import logging
from config import Config

logger = logging.getLogger(__name__)

class ArxivFetcher:
    def __init__(self):
        self.client = arxiv.Client()
        self.keywords = Config.SEARCH_KEYWORDS
        
    def fetch_recent_papers(self, days_back: int = 1) -> List[Dict]:
        """
        获取最近几天的论文
        
        Args:
            days_back: 回溯天数，默认为1（获取昨天的）
        """
        try:
            days_back = 3
            # 计算日期范围
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)
            
            # 构建查询
            date_range = f"[{start_date.strftime('%Y%m%d')} TO {end_date.strftime('%Y%m%d')}]"
            keyword_query = " OR ".join([f'abs:"{kw.strip()}"' for kw in self.keywords])
            query = f"({keyword_query}) AND submittedDate:{date_range}"
            
            logger.info(f"搜索查询: {query}")
            
            # 搜索论文
            search = arxiv.Search(
                query=query,
                max_results=Config.MAX_RESULTS,
                sort_by=arxiv.SortCriterion.SubmittedDate,
                sort_order=arxiv.SortOrder.Descending
            )
            
            papers = []
            for result in self.client.results(search):
                paper = {
                    'id': result.get_short_id(),
                    'title': result.title,
                    'authors': [author.name for author in result.authors],
                    'abstract': result.summary,
                    'pdf_url': result.pdf_url,
                    'published': result.published.strftime('%Y-%m-%d %H:%M'),
                    'primary_category': result.primary_category,
                    'categories': result.categories,
                    'arxiv_url': result.entry_id,
                }
                papers.append(paper)
                logger.info(f"找到论文: {paper['title'][:50]}...")
            
            logger.info(f"共找到 {len(papers)} 篇相关论文")
            return papers
            
        except Exception as e:
            logger.error(f"获取论文失败: {e}")
            return []
    
    def generate_summary(self, paper: Dict) -> str:
        """生成论文的中文摘要"""
        title = paper['title']
        abstract = paper['abstract']
        
        # 简单总结逻辑（后续可以接入AI）
        summary_lines = [
            "=" * 60,
            f"📄 标题: {title}",
            "",
            f"👥 作者: {', '.join(paper['authors'][:3])}{'等' if len(paper['authors']) > 3 else ''}",
            f"📅 发布时间: {paper['published']}",
            f"📚 分类: {paper['primary_category']}",
            "",
            "📝 摘要摘要:",
            self._truncate_text(abstract, 800) + ("..." if len(abstract) > 800 else ""),
            "",
            "🔗 链接:",
            f"PDF: {paper['pdf_url']}",
            f"Arxiv: {paper['arxiv_url']}",
            "=" * 60,
            ""
        ]
        
        return "\n".join(summary_lines)
    
    def _truncate_text(self, text: str, max_length: int) -> str:
        """截断文本"""
        if len(text) <= max_length:
            return text
        return text[:max_length].rsplit(' ', 1)[0]  # 在最后一个空格处截断

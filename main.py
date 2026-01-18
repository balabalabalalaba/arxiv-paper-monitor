# main.py - 适配GitHub Actions的版本
import time
import os
from datetime import datetime
import logging

from config import Config
from arxiv_fetcher import ArxivFetcher
from email_sender import EmailSender

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ArxivDailyDigest:
    def __init__(self):
        self.fetcher = ArxivFetcher()
        self.email_sender = EmailSender()
        
    def run(self, test_mode=False):
        """运行一次任务"""
        logger.info("=" * 60)
        logger.info(f"开始执行Arxiv论文抓取任务 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            # 1. 获取论文
            days_back = 0 if test_mode else 1
            papers = self.fetcher.fetch_recent_papers(days_back=days_back)
            
            # 2. 生成摘要
            summaries = []
            if papers:
                summaries = [self.fetcher.generate_summary(paper) for paper in papers]
                logger.info(f"找到 {len(papers)} 篇相关论文")
            else:
                logger.info("今日没有找到相关论文，将发送『无新论文』通知")
            
            # 3. 总是发送邮件（无论有无论文）
            success = self.email_sender.send_digest(papers, summaries)
            
            if success:
                if papers:
                    logger.info(f"✅ 任务完成！成功发送 {len(papers)} 篇论文摘要")
                else:
                    logger.info("✅ 任务完成！已发送『今日无新论文』通知")
            else:
                logger.error("邮件发送失败")
                
        except Exception as e:
            logger.exception(f"任务执行失败: {e}")
        
        logger.info("=" * 60)
    
    def run_once(self, test_mode=False):
        """
        单次运行模式 - 用于GitHub Actions
        执行一次任务后立即返回
        """
        logger.info("🚀 启动单次任务模式（适配GitHub Actions）")
        self.run(test_mode=test_mode)
        logger.info("📤 单次任务执行完毕，进程将退出")

def main():
    """主函数 - 根据环境变量决定运行模式"""
    # 验证配置
    try:
        Config.validate()
    except ValueError as e:
        logger.error(f"配置错误: {e}")
        logger.info("请检查环境变量是否配置正确")
        return
    
    # 创建实例
    digest = ArxivDailyDigest()
    
    # 判断运行模式
    # 如果在GitHub Actions中，使用单次运行模式
    # 可以通过环境变量 RUN_IN_CI 或直接判断 GITHUB_ACTIONS 环境变量
    if os.getenv('GITHUB_ACTIONS') == 'true' or os.getenv('RUN_MODE') == 'ci':
        logger.info("检测到CI/CD环境，使用单次运行模式")
        # 在GitHub Actions中，TEST_MODE应该为False
        digest.run_once(test_mode=False)
    else:
        # 本地环境：根据配置决定运行模式
        if Config.TEST_MODE:
            logger.info("运行本地测试模式...")
            digest.run(test_mode=True)
        else:
            # 本地定时模式 - 如果需要的话
            # 注意：这里需要导入schedule库，但为了清晰我建议创建另一个文件
            logger.info("本地环境请使用原来的定时运行模式")
            logger.info("提示：请运行原来的版本或创建新的本地运行脚本")
            # 或者可以选择直接运行一次
            logger.info("本次直接运行一次任务...")
            digest.run_once(test_mode=False)

if __name__ == "__main__":
    main()

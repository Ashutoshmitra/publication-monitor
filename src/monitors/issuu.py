import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict, Any
import logging
from .base import BaseMonitor
import os
from ..utils.date_utils import parse_date
from ...issuu_scraper import IssuuScraper

class IssuuMonitor(BaseMonitor):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.scraper = IssuuScraper()
        self.min_date = parse_date(config["min_date"])

    def check_new_publications(self) -> List[Dict[str, Any]]:
        new_publications = []
        
        for publisher in self.config["publishers"]:
            try:
                pub_urls = self.scraper.get_publications(publisher, 10)  # Check last 10 publications
                
                for url in pub_urls:
                    doc_data = self.scraper.get_document_data(url)
                    if not doc_data:
                        continue
                        
                    pub_date = datetime.strptime(
                        doc_data.get("originalPublishDateInISOString", "").split("T")[0],
                        "%Y-%m-%d"
                    )
                    
                    if pub_date > self.min_date:
                        new_publications.append({
                            "title": doc_data["title"],
                            "publisher": publisher,
                            "url": url,
                            "date": pub_date.isoformat(),
                            "publication_id": doc_data["publication_id"],
                            "page_count": doc_data["page_count"]
                        })
                        
            except Exception as e:
                logging.error(f"Error checking publications for {publisher}: {str(e)}")
                
        return new_publications

    def download_publication(self, publication: Dict[str, Any], output_path: str) -> bool:
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            return self.scraper.scrape_publication(
                publication["publisher"],
                publication["url"],
                lambda *args: None  # Empty callback
            )
        except Exception as e:
            logging.error(f"Error downloading publication {publication['title']}: {str(e)}")
            return False

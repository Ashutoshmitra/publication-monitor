from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict, Any

class BaseMonitor(ABC):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    @abstractmethod
    def check_new_publications(self) -> List[Dict[str, Any]]:
        """Check for new publications and return a list of publication metadata"""
        pass
        
    @abstractmethod
    def download_publication(self, publication: Dict[str, Any], output_path: str) -> bool:
        """Download a specific publication to the given path"""
        pass

from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseNotifier(ABC):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    @abstractmethod
    def notify(self, publications: List[Dict[str, Any]]) -> bool:
        """Send notification about new publications"""
        pass

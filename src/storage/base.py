from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseStorage(ABC):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    @abstractmethod
    def upload_file(self, local_path: str, remote_name: str) -> str:
        """Upload a file and return its remote URL or ID"""
        pass
        
    @abstractmethod
    def list_files(self) -> List[Dict[str, Any]]:
        """List existing files in the storage"""
        pass

from abc import ABC, abstractmethod
from typing import List


class EmbeddingProvider(ABC):

    @abstractmethod
    def generate(self, text: str) -> List[float]:
        ...

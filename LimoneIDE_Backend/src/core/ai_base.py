from abc import ABC, abstractmethod

class BaseAIHandler(ABC):
    @abstractmethod
    def is_available(self) -> bool:
        pass

    @abstractmethod
    async def generate_response(self, prompt: str) -> str:
        pass 
from abc import ABC, abstractmethod

class Agent(ABC):
    @abstractmethod
    async def run(self, user_input: str, session_id: str | None = None) -> tuple[str, list[str]]:
        """
        Returns:
          - answer (str)
          - tool_calls (list[str])  # simple trace of what tools were used
        """
        raise NotImplementedError

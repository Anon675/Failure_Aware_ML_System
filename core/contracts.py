from typing import Any, Dict, Tuple


class ModelContract:
    """
    Every domain model MUST follow this contract.
    """

    def predict(self, input_data: Any) -> Tuple[Any, float]:
        """
        Returns:
        - prediction: Any
        - confidence: float (0 to 1)
        """
        raise NotImplementedError


class DomainSignalsContract:
    """
    Domain-specific safety signals.
    """

    def extract_signals(self, output: Any) -> Dict[str, bool]:
        """
        Returns:
        - signal_name -> True/False
        """
        raise NotImplementedError

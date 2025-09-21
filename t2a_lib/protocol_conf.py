from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class ProtocolConfig:
    sample_rate: int = 44100
    frequency_high: int = 2000
    frequency_low: int = 1000
    bit_duration: float = 0.1
    silence_duration: float = 0.05
    start_marker: str = "11111111"
    end_marker: str = "00000000"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "sample_rate": self.sample_rate,
            "frequency_high": self.frequency_high,
            "frequency_low": self.frequency_low,
            "bit_duration": self.bit_duration,
            "silence_duration": self.silence_duration,
            "start_marker": self.start_marker,
            "end_marker": self.end_marker
        }
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> "ProtocolConfig":
        return cls(**config_dict)

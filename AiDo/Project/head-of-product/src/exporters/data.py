from dataclasses import dataclass


@dataclass(kw_only=True)
class Data:
    text: str
    date: str

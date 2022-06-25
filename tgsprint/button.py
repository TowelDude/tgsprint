from dataclasses import dataclass
from typing import Any, Callable, List
from emoji import emojize


@dataclass
class MenuButton(object):
    label: str
    callback: Callable
    new_row: bool = False
    callback_args: List = None

    def __init__(self, label: str, callback: Callable, new_row: bool = False, callback_args: List = None) -> None:
        self.callback = callback
        self.new_row = new_row
        self.label = emojize(label, use_aliases=True)
        self.callback_args = callback_args

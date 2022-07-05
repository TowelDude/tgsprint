from typing import Any, Callable, List, Optional
import typing
from emoji import emojize
import attr

if typing.TYPE_CHECKING:
    from telegram import Update
    from tgsprint.state import BaseState
    from tgsprint.utils import TGContext

@attr.s(auto_attribs=True)
class MenuButton(object):
    label: str = attr.field(converter=emojize)
    callback: Callable[["Update", "TGContext"], Optional["BaseState"]]
    new_row: bool = False
    callback_args: List = attr.Factory(list)

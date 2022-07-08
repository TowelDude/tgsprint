from typing import Callable, Optional

from telegram import Update
from tgsprint.menu import BaseMenu
import attr

from tgsprint.utils import TGContext


@attr.s(auto_attribs=True)
class BaseState(object):
    current_menu: BaseMenu


@attr.s(auto_attribs=True)
class UserInputState(BaseState):
    response_callback: Callable[[Update, TGContext], Optional[BaseState]]

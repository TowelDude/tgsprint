import typing
from telegram.ext import CallbackContext

if typing.TYPE_CHECKING:
    from tgsprint.menu import BaseMenu
    from tgsprint.state import BaseState


class TGContext(object):
    TG_STATE_KEY = '_tgstate'
    TG_MENU_STACK_KEY = '_tgstack'
    TG_INVALIDATE_KEYBOARD = '_tginvalidatekeyboard'

    def __init__(self, context: CallbackContext) -> None:
        self.context: CallbackContext = context
        if self.TG_MENU_STACK_KEY not in self.context.user_data:
            self.context.user_data[self.TG_MENU_STACK_KEY] = list()

        if self.TG_INVALIDATE_KEYBOARD not in self.context.user_data:
            self.context.user_data[self.TG_INVALIDATE_KEYBOARD] = False

    def get_user_data(self, key: str) -> object:
        return self.context.user_data[key]

    def set_user_data(self, key: str, value: object):
        self.context.user_data[key] = value

    def set_state(self, state: "BaseState"):
        self.set_user_data(self.TG_STATE_KEY, state)

    def get_state(self) -> "BaseState":
        return self.get_user_data(self.TG_STATE_KEY)

    def get_menu_stack(self) -> list:
        return self.get_user_data(self.TG_MENU_STACK_KEY)

    def push_menu(self, menu: "BaseMenu"):
        stack: list = self.get_menu_stack()
        stack.append(menu)

    def clear_menu_stack(self):
        self.context.user_data[self.TG_MENU_STACK_KEY] = []

    def get_current_menu(self) -> "BaseMenu":
        stack = self.get_menu_stack()
        return stack[-1]

    def set_current_menu(self, menu: "BaseMenu"):
        raise NotImplemented()

    def set_invalidate_keyboard(self, flag: bool):
        '''
        forces the keyboard to be resent instead of edited the next time
        '''
        self.context.user_data[self.TG_INVALIDATE_KEYBOARD] = flag

    def get_invalidate_keyboard(self) -> bool:
        return self.context.user_data[self.TG_INVALIDATE_KEYBOARD]

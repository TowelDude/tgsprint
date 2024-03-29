import attr
from typing import List
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from tgsprint.button import MenuButton
from tgsprint.utils import emojize

@attr.s(auto_attribs=True)
class BaseMenu(object):
    name: str
    prompt: str = attr.field(converter=emojize)
    buttons: List[MenuButton] = attr.Factory(list)
    inline: bool = False

    def add_button(self, button: MenuButton):
        if self.buttons is None:
            self.buttons = list()
        self.buttons.append(button)

    def to_keyboard(self) -> object:
        keyboard = []
        row = []
        for button in self.buttons:
            if button.new_row:
                keyboard.append(row)
                row = []
            if self.inline:
                row.append(InlineKeyboardButton(
                    button.label, callback_data=[self.name, button.label]))
            else:
                raise NotImplementedError()
        keyboard.append(row)
        if self.inline:
            return InlineKeyboardMarkup(keyboard)
        raise NotImplementedError()

    def find_button(self, identifier: object) -> MenuButton:
        if self.inline:
            if isinstance(identifier, list):
                name, button_label = identifier
                if name == self.name:
                    button = list(filter(lambda b: b.label == button_label, self.buttons))
                    if button:
                        return button[0]
            return None
        else:
            raise NotImplementedError()


@attr.s(auto_attribs=True)
class InlineMenu(BaseMenu):
    inline: bool = True

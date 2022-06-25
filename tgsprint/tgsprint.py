from typing import List
from tgsprint.button import MenuButton
from tgsprint.menu import BaseMenu
from telegram.ext import Updater
from telegram.ext import CallbackQueryHandler, CommandHandler, Dispatcher, MessageHandler, CallbackContext
from telegram import Update
from emoji import emojize

class TGSprint(object):
    def __init__(self, api_key: str) -> None:
        self.updater = Updater(api_key, arbitrary_callback_data=True)
        self.bot = self.updater.bot
        self.start_menu: BaseMenu = None

        self.updater.dispatcher.add_handler(
            CommandHandler('start', self._handle_start_command))
        self.updater.dispatcher.add_handler(
            CallbackQueryHandler(self._handle_callback_query))

    def start(self, start_menu: BaseMenu):
        self.start_menu = start_menu
        self.updater.start_polling()
        self.updater.idle()

    def _handle_callback_query(self, update: Update, context: CallbackContext):
        """
        This function handles all callback queries. 
        It will only search for buttons in the current menu in the menu stack
        """
        stack: list = context.user_data['menu_stack']
        current_menu: BaseMenu = stack[-1]  # last item in the stack
        update.callback_query.answer()
        query_data = update.callback_query.data

        button: MenuButton = current_menu.find_button(query_data)
        if button:
            if button.callback_args:
                button.callback(update, context, *button.callback_args)
            else:
                button.callback(update, context)

    def _handle_start_command(self, update: Update, context: CallbackContext):
        self.go_home(update, context)

    def goto_menu(self, update: Update, context: CallbackContext, menu: BaseMenu):
        stack: list = context.user_data['menu_stack']
        stack.append(menu)
        keyboard = menu.to_keyboard()
        if menu.inline:
            if update.callback_query is None or not menu.edit_message:
                context.bot.send_message(
                    update.effective_chat.id, emojize(menu.prompt), reply_markup=keyboard
                )
            else:
                context.bot.edit_message_text(emojize(menu.prompt), 
                    chat_id=update.callback_query.message.chat_id,
                    message_id=update.callback_query.message.message_id,
                    reply_markup=keyboard
                )

    def go_back(self, update: Update, context: CallbackContext):
        '''
        goes to the previous menu in the stack
        '''
        stack: list = context.user_data['menu_stack']
        if len(stack) > 1:
            stack.pop()  # remove current menu
            previous_menu = stack.pop()  # get the one before
            self.goto_menu(update, context, previous_menu)

    def go_home(self, update: Update, context: CallbackContext):
        '''
        goes to `start_menu` and clears the menu stack
        '''
        context.user_data['menu_stack'] = []
        self.goto_menu(update, context, self.start_menu)

from typing import List, Callable
from tgsprint.button import MenuButton
from tgsprint.menu import BaseMenu
from telegram.ext import Updater, InvalidCallbackData
from telegram.ext import CallbackQueryHandler, CommandHandler, Dispatcher, MessageHandler, CallbackContext, Filters
from telegram import Update
from tgsprint.utils import emojize

from tgsprint.state import BaseState, UserInputState
from tgsprint.utils import TGContext


class TGSprint(object):
    def __init__(self, api_key: str) -> None:
        self.updater = Updater(api_key, arbitrary_callback_data=True)
        self.bot = self.updater.bot
        self.start_menu: BaseMenu = None

        self.updater.dispatcher.add_handler(
            CommandHandler('start', self._handle_start_command))
        self.updater.dispatcher.add_handler(
            CallbackQueryHandler(self._handle_callback_query))
        self.updater.dispatcher.add_handler(
            MessageHandler(Filters.text, self._handle_message))

        self._pre_message_hooks = list()

    def add_premessage_hook(self, hook: Callable[[Update, TGContext], bool]):
        '''
        Adds a callback to the premessage chain
        Each callback will be executed (by order of insertion). 
        The first callback to return False will stop further hooks and message processing
        '''
        self._pre_message_hooks.append(hook)

    def start(self, start_menu: BaseMenu):
        self.start_menu = start_menu
        self.updater.start_polling()
        self.updater.idle()

    def _run_premessage_hooks(self, update: Update, context: TGContext) -> bool:
        for hook in self._pre_message_hooks:
            result = hook(update, context)
            if not result:
                return False
        return True

    def _handle_message(self, update: Update, context: CallbackContext):
        tgcontext = TGContext(context)
        state: BaseState = tgcontext.get_state()
        
        should_continue = self._run_premessage_hooks(update, tgcontext)
        if not should_continue:
            return

        if type(state) is BaseState:
            if state.current_menu.inline:
                return
            else:
                raise NotImplementedError()

        if type(state) is UserInputState:
            message = update.message.text
            retval = state.response_callback(update, tgcontext, message)

            if issubclass(type(retval), BaseState):
                tgcontext.set_state(retval)

    def _handle_callback_query(self, update: Update, context: CallbackContext):
        """
        This function handles all callback queries. 
        It will only search for buttons in the current menu in the menu stack
        """
        if type(update.callback_query.data) is InvalidCallbackData:
            return

        tgcontext = TGContext(context)
        update.callback_query.answer()

        should_continue = self._run_premessage_hooks(update, tgcontext)
        if not should_continue:
            return

        current_menu = tgcontext.get_current_menu()
        query_data = update.callback_query.data

        button: MenuButton = current_menu.find_button(query_data)

        if button:
            retval = button.callback(update, tgcontext, *button.callback_args)
            if issubclass(type(retval), BaseState):
                tgcontext.set_state(retval)

    def _handle_start_command(self, update: Update, context: CallbackContext):
        tgcontext = TGContext(context)
        should_continue = self._run_premessage_hooks(update, tgcontext)
        if not should_continue:
            return

        self.go_home(update, tgcontext)

    def _send_menu(self, update: Update, context: TGContext, menu: BaseMenu):
        keyboard = menu.to_keyboard()
        context.set_state(BaseState(menu))

        if menu.inline:
            invalidated = context.get_invalidate_keyboard()
            if update.callback_query is None or invalidated:
                if invalidated:
                    context.set_invalidate_keyboard(False)

                context.context.bot.send_message(
                    update.effective_chat.id, emojize(menu.prompt), reply_markup=keyboard
                )
            else:
                context.context.bot.edit_message_text(emojize(menu.prompt),
                                                      chat_id=update.callback_query.message.chat_id,
                                                      message_id=update.callback_query.message.message_id,
                                                      reply_markup=keyboard
                                                      )

    def resend_menu(self, update: Update, context: TGContext):
        '''
        resends current menu, forces invalidation
        '''
        current_menu = context.get_current_menu()
        context.set_invalidate_keyboard(True)
        self._send_menu(update, context, current_menu)

    def goto_menu(self, update: Update, context: TGContext, menu: BaseMenu):
        context.push_menu(menu)
        self._send_menu(update, context, menu)

    def go_back(self, update: Update, context: TGContext):
        '''
        goes to the previous menu in the stack
        '''
        stack: list = context.get_menu_stack()
        if len(stack) > 1:
            stack.pop()  # remove current menu
            previous_menu = stack.pop()  # get the one before
            self.goto_menu(update, context, previous_menu)

    def go_home(self, update: Update, context: TGContext):
        '''
        goes to `start_menu` and clears the menu stack
        '''
        context.clear_menu_stack()
        self.goto_menu(update, context, self.start_menu)

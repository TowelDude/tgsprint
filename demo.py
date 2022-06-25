from telegram import Update
from telegram.ext import CallbackContext
from tgsprint.tgsprint import TGSprint
from tgsprint.menu import InlineMenu, MenuButton
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

tg = TGSprint('APIKEY')

def null(update: Update, context: CallbackContext):
    context.bot.send_message(update.effective_chat.id, 'Hello!')

menu2 = InlineMenu('menu2', 'Menu 2! :red_heart:')
menu2.add_button(MenuButton('button 1 :red_heart:', null))
menu2.add_button(MenuButton('button 2 :red_heart:', null))
menu2.add_button(MenuButton('button 3 :red_heart:', null))
menu2.add_button(MenuButton('go back :red_heart:', callback=tg.go_back, new_row=True))

start_menu = InlineMenu('start', 'Welcome to my bot! :red_heart:')
start_menu.add_button(MenuButton('goto menu2 :red_heart:', callback=tg.goto_menu, callback_args=[menu2]))

tg.start(start_menu)

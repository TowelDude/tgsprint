from pathlib import Path
import os
from telegram import Update
from telegram.ext import CallbackContext
from tgsprint.state import *
from tgsprint.tgsprint import TGSprint
from tgsprint.menu import InlineMenu, MenuButton
from tgsprint.utils import TGContext
import logging


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

apikey = open(os.path.join(Path.home(), '.tgsprint', 'api.txt'), 'r').read().strip()
tg = TGSprint(apikey)

def sample_hook(update: Update, context: TGContext):
    context.context.bot.send_message(update.effective_chat.id, 'hook!')
    return True

def null(update: Update, context: TGContext):
    context.context.bot.send_message(update.effective_chat.id, 'Hello!')

def respond_echo(update: Update, context: TGContext, message: str):
    context.context.bot.send_message(update.effective_chat.id, f'You said: {message}')
    tg.resend_menu(update, context)
    
    return BaseState(context.get_current_menu())

def echo(update: Update, context: TGContext):
    context.context.bot.send_message(update.effective_chat.id, 'Write a message, i will echo it back at ya')
    return UserInputState(context.get_current_menu(), respond_echo)

menu2 = InlineMenu('menu2', 'Menu 2! :red_heart:')
menu2.add_button(MenuButton('button 1 :red_heart:', null))
menu2.add_button(MenuButton('echo button', echo))
menu2.add_button(MenuButton('go back :red_heart:',
                 callback=tg.go_back, new_row=True))

start_menu = InlineMenu('start', 'Welcome to my bot! :red_heart:')
start_menu.add_button(MenuButton('goto menu2 :red_heart:',
                      callback=tg.goto_menu, callback_args=[menu2]))

tg.add_premessage_hook(sample_hook)
tg.start(start_menu)

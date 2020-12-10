import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, updater
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, update
import logging
import sqlite3
from tabulate import tabulate
from Config import TOKEN
from TelegramBot import TelegramBot


def main():

    bot = TelegramBot()
    bot.execute()

main()
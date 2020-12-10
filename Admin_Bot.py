import os
import urllib.request

import telegram
from wix_store import dataWixStore
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, keyboardbutton, ReplyKeyboardMarkup
import logging
from Config import TOKEN_ADMINBOT, TELEGRAM_CHANNELL_ID_PUBLIC, LINK_TABLE_ORDERS, URL_STORE_BOT, ADMIN_PASSWORD, INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD
from time import sleep
from InstagramAPI import InstagramAPI


class TelegramAdminBot:
    def __init__(self):
        self.bot = telegram.Bot(token=TOKEN_ADMINBOT)
        self.updater = Updater(token=TOKEN_ADMINBOT)

        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        self.store = dataWixStore()

        self.outgoing_message_text = None

        self.PASSWORD, self.MENU, self.CODE, self.INSTA, self.INSTATWO, self.STRING = range(6)

    def user_data(self):
        self.first_name = None
        self.last_name = None
        self.chat_id = None

    def start(self, bot, update):
        self.user_data()
        self.first_name = str(update.message.from_user.first_name)
        self.last_name = str(update.message.from_user.last_name)
        self.username = str(update.message.from_user.username)
        self.chat_id = update.message.from_user.id
        self.query_insta = None
        self.instaCode = None
        print(self.chat_id)
        self.logo_link = "https://video.wixstatic.com/video/07e3fe_9cbe39267f7c418eb749fe2a45af084c/1080p/mp4/file.mp4"
        self.outgoing_message_text = "Hello {} {}, welcome to <b>Mubbylab Store Admin Dashboard</b> 🤖 \n " \
                                     "Insert the Admin Password".format(
            self.first_name,
            self.last_name)
        self.bot.send_animation(chat_id=update.message.chat_id, animation=self.logo_link,
                                caption=self.outgoing_message_text,
                                parse_mode=telegram.ParseMode.HTML)
        return self.PASSWORD

    def check_password(self, bot, update):
        query_data = update.message.text
        password_insert = str(query_data)
        if password_insert == ADMIN_PASSWORD:
            self.outgoing_message_text = "Password Accepted :), Welcome Admin"
            bot.sendMessage(chat_id=update.effective_user.id, text=self.outgoing_message_text,
                            parse_mode=telegram.ParseMode.HTML)
            self.main_menu(bot, update)
            return self.MENU
        else:
            self.outgoing_message_text = "Password not Accepted :)\n <b>Please Try Again</b>"
            bot.sendMessage(chat_id=update.effective_user.id, text=self.outgoing_message_text,
                            parse_mode=telegram.ParseMode.HTML)
            return self.PASSWORD

    def main_menu(self, bot, update):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Public all item in database', callback_data='allitem'),
             InlineKeyboardButton(text='Public a specific Item', callback_data='specificitem')],
            [InlineKeyboardButton(text='Insert String Order', callback_data='string')],
            [InlineKeyboardButton(text='Print Last 50 Items on DB', callback_data='last')],
            [InlineKeyboardButton(text='Pubblish Product to Instagram', callback_data='insta')],
            [InlineKeyboardButton(text='Check Table Order', callback_data='web')]
        ])
        bot.sendMessage(chat_id=update.effective_user.id, text='What do you want to do?', reply_markup=keyboard)
        return self.MENU

    def on_callback_query_menu(self, bot, update):
        query_data = update.callback_query.data
        print(query_data)
        print(update.effective_user.id)
        if query_data == 'allitem':
            try:
                print("pubblishing all the product")
                CodeId_list = self.get_allCode()
                print(CodeId_list)
                for x in CodeId_list:
                    codeID_prov = str(x)
                    codeID = codeID_prov.replace("\n", "")
                    print(codeID)
                    if codeID is not None and len(codeID) == 8:
                        self.store.id_code = codeID
                        self.store.init_requestDataforCode()
                        print(self.store.get_urlPic())
                        self.bot.send_chat_action(chat_id=TELEGRAM_CHANNELL_ID_PUBLIC,
                                                  action=telegram.ChatAction.TYPING)
                        if (self.store.get_priceProduct() == self.store.get_discountedPrice()):
                            self.bot.send_photo(chat_id=TELEGRAM_CHANNELL_ID_PUBLIC, photo=self.store.get_urlPic(),
                                                caption="👟 Product : <b> {} </b> \n\n💴PRICE: --> <b>{}"
                                                        "$</b>\n\n#️⃣ID_Product: <b>{}</b>".format(
                                                    self.store.get_nameProduct(),
                                                    self.store.get_priceProduct(), codeID),
                                                reply_markup=self.get_botButton(self.store.get_URL()),
                                                parse_mode=telegram.ParseMode.HTML)
                        else:
                            self.bot.send_photo(chat_id=TELEGRAM_CHANNELL_ID_PUBLIC, photo=self.store.get_urlPic(),
                                                caption="👟 Product : <b> {} </b> \n\n<b>{}% DISCOUNT</b>\n\n💴PRICE: "
                                                        "--> <b><s>{}$</s> {}$</b>\n\n#️⃣ID_Product: <b>{}</b>\n\n "
                                                        "<a href={}>Get more details on our website</a>".format(
                                                    self.store.get_nameProduct(),
                                                    self.store.get_discountValue(),
                                                    self.store.get_priceProduct(), self.store.get_discountedPrice(),
                                                    codeID,
                                                    self.store.get_URL()),
                                                reply_markup=self.get_botButton(self.store.get_URL()),
                                                parse_mode=telegram.ParseMode.HTML)
                        sleep(0.3)
            except telegram.error.TimedOut:
                print("Error Restarting")
                self.start(bot, update)

        elif query_data == 'specificitem':
            print("Publish a specific product")
            self.outgoing_message_text = "<b>⌨️Enter the code of the product you want yo Pubblish:⌨️</b>"
            bot.sendMessage(chat_id=update.effective_user.id, text=self.outgoing_message_text,
                            parse_mode=telegram.ParseMode.HTML)
            return self.CODE

        elif query_data == 'web':
            self.outgoing_message_text = "All the order done in telegram bot are available here\n{}".format(
                LINK_TABLE_ORDERS)
            self.bot.sendMessage(chat_id=update.effective_user.id, text=self.outgoing_message_text,
                                 parse_mode=telegram.ParseMode.HTML)
            self.main_menu(bot, update)
            return self.MENU

        elif query_data == 'string':
            print("Publish a specific product")
            self.outgoing_message_text = "<b>⌨️Enter the string_code of the product you want yo Pubblish:⌨️</b>"
            bot.sendMessage(chat_id=update.effective_user.id, text=self.outgoing_message_text,
                            parse_mode=telegram.ParseMode.HTML)
            return self.STRING

        elif query_data == 'last':
            print("Pubblishing last 50 Item")
            self.outgoing_message_text = "<b>⌨️Pubblishing last 50 Items in DB:⌨️</b>"
            bot.sendMessage(chat_id=update.effective_user.id, text=self.outgoing_message_text,
                            parse_mode=telegram.ParseMode.HTML)
            self.last_item(bot, update)
            return self.MENU

        elif query_data == 'insta':
            self.outgoing_message_text = "<b>⌨️Insert id of a Product⌨️</b>"
            bot.sendMessage(chat_id=update.effective_user.id, text=self.outgoing_message_text,
                            parse_mode=telegram.ParseMode.HTML)
            return self.INSTA


    def photo_instagram(self, bot, update):
        try:
            codeID = str(update.message.text)
            print(codeID)
            if codeID is not None and len(codeID) == 8:
                self.store.id_code = codeID
                self.store.init_requestDataforCode()
                print(self.store.get_urlPic())
                self.bot.send_chat_action(chat_id=update.effective_user.id, action=telegram.ChatAction.TYPING)
                if (self.store.get_priceProduct() == self.store.get_discountedPrice()):
                    self.bot.send_photo(chat_id=update.effective_user.id, photo=self.store.get_urlPic(),
                                        caption="👟 Product : <b> {} </b> \n\n💴PRICE: --> <b>{}$</b>\n\n#️⃣ID_Product: <b>{}</b>".format(
                                            self.store.get_nameProduct(),
                                            self.store.get_priceProduct(), codeID),
                                         reply_markup=self.keyboard_confim(),
                                        parse_mode=telegram.ParseMode.HTML)
                    return self.INSTA
                else:
                    self.bot.send_photo(chat_id=update.effective_user.id, photo=self.store.get_urlPic(),
                                        caption="👟 Product : <b> {} </b> \n\n<b>{}% DISCOUNT</b>\n\n💴PRICE: --> <b><s>{}$</s> {}$</b>\n\n#️⃣ID_Product: <b>{}</b>\n\n".format(
                                            self.store.get_nameProduct(),
                                            self.store.get_discountValue(),
                                            self.store.get_priceProduct(), self.store.get_discountedPrice(),
                                            codeID),
                                        reply_markup=self.keyboard_confim(),
                                        parse_mode=telegram.ParseMode.HTML)
                    return self.INSTA
        except telegram.error.TimedOut:
            print('Restarting')
            self.main_menu(bot, update)
            return self.MENU

    def keyboard_confim(self):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Confirm? ✈️', callback_data='continue')],
            [InlineKeyboardButton(text='Cancel ❌', callback_data='goback')]
        ])
        return keyboard

    def product_instaConfirmed(self, bot, update):
        query_data = update.callback_query.data

        if query_data == 'continue':
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='1 Photo for Product', callback_data='one')],
                [InlineKeyboardButton(text='3 Photo for Product', callback_data='three')]
            ])
            bot.sendMessage(chat_id=update.effective_user.id, text='How many photo of the product do you wanna pubblish', reply_markup=keyboard)
            return self.INSTA

        elif query_data == 'goback':
            return self.main_menu(bot, update)

        elif query_data == 'one':
            bot.sendMessage(chat_id=update.effective_user.id, text='Write the caption of the photo...\n Type None if you want the standart format')
            self.query_insta = 1
            return self.INSTATWO
        elif query_data == 'three':
            bot.sendMessage(chat_id=update.effective_user.id, text='Write the caption of the photo...\n Type None if you want the standart format')
            self.query_insta = 3
            return self.INSTATWO


    def put_photoOnInsta(self, bot ,update):
        Caption = str(update.message.text)

        print("AFTER LOGIN")
        Hashtags = "#shoes #fashion #style #sneakers #moda #nike #shopping #love #heels #shoesaddict #boots #instagood" \
                  " #bags #ootd #like #outfit #adidas #dress #fashionblogger #instafashion #model #clothes #" \
                  "zapatos #stylish #photooftheday #footwear #fashionista #bag #beauty #bhfyp"
        if self.query_insta == 1:
            if Caption != 'None':
                bot.sendPhoto(chat_id=update.effective_user.id, photo=self.store.get_urlPic(), caption=Caption)
            elif Caption == 'None':
                if self.store.get_priceProduct() == self.store.get_discountedPrice():
                    Caption = "👟 Product: {}\n💴PRICE: --> {}$\n#️⃣ID_Product for Telegram Bot: {}\n\n{}".format(
                                  self.store.get_nameProduct(),
                                  self.store.get_priceProduct(), self.store.id_code(), Hashtags)
                    bot.sendPhoto(chat_id=update.effective_user.id, photo=self.store.get_urlPic(), caption=Caption)
                else:
                    Caption = "👟 Product: {}\n{}% DISCOUNT\n💴PRICE: -->{} -{}  {}$\n#️⃣ID_Product: {}\n\n{}".format(
                        self.store.get_nameProduct(),
                        self.store.get_discountValue(),
                        self.store.get_priceProduct(), self.store.get_discountValue(), self.store.get_discountedPrice(),
                        self.store.id_code, Hashtags)
                    bot.sendPhoto(chat_id=update.effective_user.id, photo=self.store.get_urlPic(), caption=Caption)
            bot.sendMessage(chat_id=update.effective_user.id,
                        text='Process Complete, Check Instagram Profile')
            return self.main_menu(bot, update)

        elif self.query_insta == 3:

            if Caption != 'None':
                for x in self.store.get_listUrlPic():
                    bot.sendPhoto(chat_id=update.effective_user.id, photo=x)
                bot.sendMessage(chat_id=update.effective_user.id, text=Caption, parse_mode=telegram.ParseMode.HTML)
            elif Caption == 'None':

                if self.store.get_priceProduct() == self.store.get_discountedPrice():
                    Caption = "👟 Product: {}\n💴PRICE: --> {}$\n#️⃣ID_Product for Telegram Bot: {}\n\n{}".format(
                        self.store.get_nameProduct(),
                        self.store.get_priceProduct(), self.store.id_code(), Hashtags)
                    for x in self.store.get_listUrlPic():
                        bot.sendPhoto(chat_id=update.effective_user.id, photo=x)
                    bot.sendMessage(chat_id=update.effective_user.id, text=Caption, parse_mode=telegram.ParseMode.HTML)

                else:
                    Caption = "👟 Product: {}\n{}% DISCOUNT\n💴PRICE: -->{} -{}  {}$\n#️⃣ID_Product: {}\n\n{}".format(
                        self.store.get_nameProduct(),
                        self.store.get_discountValue(),
                        self.store.get_priceProduct(), self.store.get_discountValue(), self.store.get_discountedPrice(),
                        self.store.id_code, Hashtags)
                    for x in self.store.get_listUrlPic():
                        print('im here')
                        bot.sendPhoto(chat_id=update.effective_user.id, photo=x)
                    bot.sendMessage(chat_id=update.effective_user.id, text=Caption, parse_mode=telegram.ParseMode.HTML)

            return self.main_menu(bot, update)

    def publish_itemArrayMessage(self, bot, update):
        try:
            StringIn = str(update.message.text)
            Code_list = StringIn.split("\n")
            for x in Code_list:
                codeID = str(x)
                print(codeID)
                if codeID is not None and len(codeID) == 8:
                    self.store.id_code = codeID
                    self.store.init_requestDataforCode()
                    print(self.store.get_urlPic())
                    self.bot.send_chat_action(chat_id=TELEGRAM_CHANNELL_ID_PUBLIC, action=telegram.ChatAction.TYPING)
                    if (self.store.get_priceProduct() == self.store.get_discountedPrice()):
                        self.bot.send_photo(chat_id=TELEGRAM_CHANNELL_ID_PUBLIC, photo=self.store.get_urlPic(),
                                            caption="👟 Product : <b> {} </b> \n\n💴PRICE: --> <b>{}$</b>\n\n#️⃣ID_Product: <b>{}</b>".format(
                                                self.store.get_nameProduct(),
                                                self.store.get_priceProduct(), codeID),
                                            reply_markup=self.get_botButton(self.store.get_URL()),
                                            parse_mode=telegram.ParseMode.HTML)
                    else:
                        self.bot.send_photo(chat_id=TELEGRAM_CHANNELL_ID_PUBLIC, photo=self.store.get_urlPic(),
                                            caption="👟 Product : <b> {} </b> \n\n<b>{}% DISCOUNT</b>\n\n💴PRICE: --> <b><s>{}$</s> {}$</b>\n\n#️⃣ID_Product: <b>{}</b>\n\n".format(
                                                self.store.get_nameProduct(),
                                                self.store.get_discountValue(),
                                                self.store.get_priceProduct(), self.store.get_discountedPrice(),
                                                codeID),
                                            reply_markup=self.get_botButton(self.store.get_URL()),
                                            parse_mode=telegram.ParseMode.HTML)
            sleep(0.5)
        except telegram.error.TimedOut:
            print('Restarting')
            self.main_menu(bot, update)
            return self.MENU

    def publish_specificProduct(self, bot, update):
        print("Sono qui")
        codeID = str(update.message.text)
        self.store.id_code = codeID
        self.store.init_requestDataforCode()
        print(self.store.get_urlPic())
        if (self.store.get_priceProduct() == self.store.get_discountedPrice()):
            self.bot.send_photo(chat_id=TELEGRAM_CHANNELL_ID_PUBLIC, photo=self.store.get_urlPic(),
                                caption="👟 Product : <b> {} </b> \n\n💴PRICE: --> <b>{}$</b>\n\n#️⃣ID_Product: <b>{}</b>".format(
                                    self.store.get_nameProduct(),
                                    self.store.get_priceProduct(), codeID),
                                reply_markup=self.get_botButton(self.store.get_URL()),
                                parse_mode=telegram.ParseMode.HTML)
        else:
            self.bot.send_photo(chat_id=TELEGRAM_CHANNELL_ID_PUBLIC, photo=self.store.get_urlPic(),
                                caption="👟 Product : <b> {} </b> \n\n<b>{}% DISCOUNT</b>\n\n💴PRICE: --> <b><s>{}$</s> {}$</b>\n\n#️⃣ID_Product: <b>{}</b>".format(
                                    self.store.get_nameProduct(),
                                    self.store.get_discountValue(),
                                    self.store.get_priceProduct(), self.store.get_discountedPrice(), codeID),
                                reply_markup=self.get_botButton(self.store.get_URL()),
                                parse_mode=telegram.ParseMode.HTML)
        self.main_menu(bot, update)
        return self.MENU


    def last_item(self, bot, update):
        try:
            List_Code, List_Message = self.store.get_lastItems()
            self.outgoing_message_text = "<b>⌨️Pubblishing last 50 Items in DB:⌨\n{}</b>".format(List_Code)
            bot.sendMessage(chat_id=update.effective_user.id, text=self.outgoing_message_text,
                            parse_mode=telegram.ParseMode.HTML)
            for x in List_Code:
                codeID = str(x)
                print(codeID)
                if codeID is not None and len(codeID) == 8:
                    self.store.id_code = codeID
                    self.store.init_requestDataforCode()
                    print(self.store.get_urlPic())
                    self.bot.send_chat_action(chat_id=TELEGRAM_CHANNELL_ID_PUBLIC, action=telegram.ChatAction.TYPING)
                    if (self.store.get_priceProduct() == self.store.get_discountedPrice()):
                        self.bot.send_photo(chat_id=TELEGRAM_CHANNELL_ID_PUBLIC, photo=self.store.get_urlPic(),
                                            caption="👟 Product : <b> {} </b> \n\n💴PRICE: --> <b>{}$</b>\n\n#️⃣ID_Product: <b>{}</b>".format(
                                                self.store.get_nameProduct(),
                                                self.store.get_priceProduct(), codeID),
                                            reply_markup=self.get_botButton(self.store.get_URL()),
                                            parse_mode=telegram.ParseMode.HTML)
                    else:
                        self.bot.send_photo(chat_id=TELEGRAM_CHANNELL_ID_PUBLIC, photo=self.store.get_urlPic(),
                                            caption="👟 Product : <b> {} </b> \n\n<b>{}% DISCOUNT</b>\n\n💴PRICE: --> <b><s>{}$</s> {}$</b>\n\n#️⃣ID_Product: <b>{}</b>\n\n".format(
                                                self.store.get_nameProduct(),
                                                self.store.get_discountValue(),
                                                self.store.get_priceProduct(), self.store.get_discountedPrice(),
                                                codeID),
                                            reply_markup=self.get_botButton(self.store.get_URL()),
                                            parse_mode=telegram.ParseMode.HTML)
            sleep(0.5)
        except telegram.error.TimedOut:
            print("Error Restarting")
            self.main_menu(bot, update)
            return self.MENU

    def get_botButton(self, url):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='🤖 STORE BOT 🤖', url=URL_STORE_BOT)],
            [InlineKeyboardButton(text='➡️Product Page⬅️', url=url)]
        ])
        return keyboard

    def get_allCode(self):
        f = open("CodeShoes.txt", "r")
        CodeID_list = f.readlines()
        return CodeID_list

    def done(self, bot, update):
        return ConversationHandler.END

    def execute(self):
        dp = self.updater.dispatcher

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', self.start)],
            states={
                self.PASSWORD: [MessageHandler(Filters.text, self.check_password)
                                ],
                self.MENU: [CallbackQueryHandler(self.on_callback_query_menu)
                            ],
                self.CODE: [
                    MessageHandler(Filters.text, self.publish_specificProduct)
                ],
                self.INSTA: [
                    MessageHandler(Filters.text, self.photo_instagram),
                    CallbackQueryHandler(self.product_instaConfirmed)
                ],
                self.INSTATWO: [
                    MessageHandler(Filters.text, self.put_photoOnInsta)
                ],
                self.STRING: [
                    MessageHandler(Filters.text, self.publish_itemArrayMessage)
                ],
            },
            fallbacks=[MessageHandler(Filters.regex('^Done$'), self.done)]
        )
        dp.add_handler(conv_handler)

        self.updater.start_polling()


prov = TelegramAdminBot()
prov.execute()

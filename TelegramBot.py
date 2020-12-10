#-*- coding: UTF-8 -*-
import telegram
from wix_store import dataWixStore
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
import logging
import sqlite3
from tabulate import tabulate
from Config import TOKEN, TELEGRAM_CHANNELL_ID, LINK_TABLE_ORDERS
from newOrder import new_Order
from time import sleep


class TelegramBot:
    def __init__(self):
        self.bot = telegram.Bot(token=TOKEN)
        self.updater = Updater(token=TOKEN)

        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        self.prov = dataWixStore()

        self.outgoing_message_text = None

        self.MENU, self.CODE, self.SIZE, self.NAME, self.ADDRESS, self.DETAILS, self.PAYMENT, self.FINALS, self.END = range(
            9)

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
        print(self.chat_id)
        self.logo_link = "https://video.wixstatic.com/video/07e3fe_9cbe39267f7c418eb749fe2a45af084c/1080p/mp4/file.mp4"
        self.outgoing_message_text = "Hello {} {}, welcome to <b>Mubbylab Store</b> 🤖 ".format(self.first_name,
                                                                                                self.last_name)
        bot.send_animation(chat_id=update.message.chat_id, animation=self.logo_link, caption=self.outgoing_message_text,
                           parse_mode=telegram.ParseMode.HTML)
        self.outgoing_message_text = 'New Visitors:\nUsername: {}\nName: {}\nSurname: {}\nChat_id: {}' \
            .format(self.username, self.first_name, self.last_name, str(self.chat_id))
        bot.sendMessage(chat_id=TELEGRAM_CHANNELL_ID, text=self.outgoing_message_text,
                        parse_mode=telegram.ParseMode.HTML)
        self.main_menu(bot, update)
        return self.MENU

    def start_again(self, bot, update):
        self.user_data()
        self.first_name = str(update.effective_user.first_name)
        self.last_name = str(update.effective_user.last_name)
        self.chat_id = update.effective_user.id
        print(self.chat_id)
        self.logo_link = "https://video.wixstatic.com/video/07e3fe_9cbe39267f7c418eb749fe2a45af084c/1080p/mp4/file.mp4"
        self.outgoing_message_text = "Hello {} {}, welcome to <b>Mubbylab Store</b> 🤖 ".format(self.first_name,
                                                                                                self.last_name)

        bot.send_photo(chat_id=update.effective_user.id, photo=self.logo_link, caption=self.outgoing_message_text,
                       parse_mode=telegram.ParseMode.HTML)
        self.main_menu(bot, update)
        return self.MENU

    def main_menu(self, bot, update):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Buy an Items', callback_data='buy'),
             InlineKeyboardButton(text='Payments', callback_data='pay')],
            [InlineKeyboardButton(text='Website', callback_data='web')]
        ])
        bot.sendMessage(chat_id=update.effective_user.id, text='What do you want to do?', reply_markup=keyboard)

    def on_callback_query_menu(self, bot, update):
        query_data = update.callback_query.data
        print(query_data)
        print(update.effective_user.id)
        if query_data == 'buy':
            print("Let's Buy something")

            return self.enter_Code(bot, update)

        elif query_data == 'pay':
            self.mother_link = "https://www.mubbylab.xyz/payment"
            self.outgoing_message_text = "Open our website to read all the information about the payment: {}".format(
                self.mother_link)
            bot.sendMessage(chat_id=update.effective_user.id, text=self.outgoing_message_text)
            self.goback_button(bot, update)
            return self.MENU

        elif query_data == 'web':
            self.mother_link = "https://www.mubbylab.xyz/"
            self.outgoing_message_text = "Our website {}".format(self.mother_link)
            self.bot.sendMessage(chat_id=update.effective_user.id, text=self.outgoing_message_text)
            self.goback_button(bot, update)
            return self.MENU

        elif query_data == 'goback':
            print("Start Again")
            self.start_again(bot, update)

    def enter_Code(self, bot, update):
        self.outgoing_message_text = "<b>⌨️Enter the code of the product you want yo buy:⌨️</b>"
        bot.sendMessage(chat_id=update.effective_user.id, text=self.outgoing_message_text,
                        parse_mode=telegram.ParseMode.HTML)
        self.cancel_button(bot, update)
        return self.CODE

    def on_callback_query_cancel(self, bot, update):
        query_data = update.callback_query.data
        if query_data == 'goback':
            print("Deleting Order..")
            self.outgoing_message_text = "❌❌❌Deleting Order...❌❌❌r"
            bot.sendMessage(chat_id=update.effective_user.id, text=self.outgoing_message_text)
            return self.start_again(bot, update)

    def goback_button(self, bot, update):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Menu 🤖', callback_data='goback')]
        ])
        self.bot.sendMessage(chat_id=update.effective_user.id, text="Do you wanna go back?", reply_markup=keyboard)

    def cancel_button(self, bot, update):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Cancel ❌', callback_data='goback')]
        ])
        self.bot.sendMessage(chat_id=update.effective_user.id, text="Do you wanna go back?", reply_markup=keyboard)

    def buyItems(self, bot, update):
        codeID = str(update.message.text)
        if codeID is not None and len(codeID) == 8:
            print(codeID)
            self.prov.id_code = codeID
            self.prov.init_requestDataforCode()
            self.bot.send_chat_action(chat_id=update.effective_user.id, action=telegram.ChatAction.TYPING)
            if (self.prov.get_priceProduct() == self.prov.get_discountedPrice()):
                self.bot.send_photo(chat_id=update.effective_user.id, photo=self.prov.get_urlPic(),
                                    caption=" ID: {} \nProduct : <b> {} </b> \nPRICE: --> <b>{}$</b>".format(codeID,
                                                                                                             self.prov.get_nameProduct(),
                                                                                                             self.prov.get_priceProduct()),
                                    parse_mode=telegram.ParseMode.HTML)
            else:
                self.bot.send_photo(chat_id=update.effective_user.id, photo=self.prov.get_urlPic(),
                                    caption=" ID: {} \nProduct : <b> {} </b> \nPRICE:  <b>{}% Discount</b>\n <b><s>{}$</s> --> {}$</b>".format(
                                        codeID,
                                        self.prov.get_nameProduct(),
                                        self.prov.get_discountValue(),
                                        self.prov.get_priceProduct(),
                                        self.prov.get_discountedPrice()),
                                    parse_mode=telegram.ParseMode.HTML)

            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Yes ✅', callback_data='yes')],
                [InlineKeyboardButton(text='Nope ❌', callback_data='goback')]
            ])
            bot.sendMessage(chat_id=update.effective_user.id, text='Do you wanna continue ?', reply_markup=keyboard)
            return self.CODE
        else:
            self.outgoing_message_text = "Product not Found 😱, check if you put the correct code...."
            self.bot.sendMessage(chat_id=update.effective_user.id, text=self.outgoing_message_text)
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Retry 👟', callback_data='buy')],
                [InlineKeyboardButton(text='Menu 🤖', callback_data='goback')]
            ])
            self.bot.sendMessage(chat_id=update.effective_user.id, text="What do you wanna do ?", reply_markup=keyboard)
            return self.CODE

    def query_istheRightOrder(self, bot, update):
        query_data = update.callback_query.data
        print(query_data)
        if query_data == 'goback':
            print("Start Again")
            return self.start_again(bot, update)

        elif query_data == 'buy':
            return self.enter_Code()

        elif query_data == 'yes':
            self.outgoing_message_text = "Nice Choice 👍: \nNow put the size of the item that you want --> \nExamples:<b>\n( UK: " \
                                         "10, EU: 44.5, US: 9\n Uk: 6, EU 39.5, US: 10 \nor XL, L, M, S, XS)</b> "
            bot.sendMessage(chat_id=update.effective_user.id, text=self.outgoing_message_text,
                            parse_mode=telegram.ParseMode.HTML)
            self.cancel_button(bot, update)
            return self.SIZE

    def init_order(self, bot, update):
        self.order = new_Order(chat_id=update.effective_user.id)

        if self.prov.check_size(str(update.message.text)):
            self.order.ItemsName = self.prov.get_nameProduct()
            self.order.Price = self.prov.get_discountedPrice()
            self.order.Discount = self.prov.get_discountValue()
            print(self.order.Discount)
            self.order.Qty = 1
            self.order.ShippingCost = 0
            size = str(update.message.text)
            print("Size: {}".format(size))
            self.order.ItemsSize = size
            self.outgoing_message_text = "Now your Name and Surname on this format:\n<b>Name Surname</b>\n<b>⚠ BE CAREFUL " \
                                         "⚠\n</b>Those data are going to be the shipping details "
            self.bot.sendMessage(chat_id=update.effective_user.id, text=self.outgoing_message_text,
                                 parse_mode=telegram.ParseMode.HTML)
            self.cancel_button(bot, update)
            return self.NAME
        else:
            self.outgoing_message_text = "The size you've enterd is not correct:\n<b>⚠ Try Again⚠ </b>\n<b>Have a look to the Examples:\n(UK: " \
                                         "10, EU: 44.5, US: 9 )\nor \n(XL, L, M, S, XS)</b>"
            self.bot.sendMessage(chat_id=update.effective_user.id, text=self.outgoing_message_text,
                                 parse_mode=telegram.ParseMode.HTML)
            self.cancel_button(bot, update)
            return self.SIZE

    def insert_PersonalDetails(self, bot, update):
        if self.prov.check_nameSurname(str(update.message.text)):
            prov = str(update.message.text)
            print(prov)
            self.order.D_Costumer = prov
            self.outgoing_message_text = "Move on, now the delivery details in this format 🌍\n <b>Country, State, City, " \
                                         "Street name and number, zipcode/postcode/cap</b>\nEx.(USA, Texas, Dallas, " \
                                         "501 Jefferson Blvd, TX 75203\nUK, England, London, 206 Aldersgate St, " \
                                         "EC1A 4HD\nItaly, Lombardia, Milano, Via Col Moschin 8, 20136) "
            self.bot.sendMessage(chat_id=update.effective_user.id, text=self.outgoing_message_text,
                                 parse_mode=telegram.ParseMode.HTML)
            self.cancel_button(bot, update)
            return self.ADDRESS
        else:
            self.outgoing_message_text = "The Name and Surname you've enterd is not on the correct format:\n<b>⚠ Try Again⚠ </b>\nThe format is:<b>\n" \
                                         "Name Surname </b>\nEx. (John Smith, Mario Rossi)"
            self.bot.sendMessage(chat_id=update.effective_user.id, text=self.outgoing_message_text,
                                 parse_mode=telegram.ParseMode.HTML)
            self.cancel_button(bot, update)
            return self.NAME

    def insert_address(self, bot, update):
        prov = str(update.message.text)
        if self.order.insert_address(prov):
            self.outgoing_message_text = "And now last but not the least your contact details\nOn this format:\n<b>Email, Telephone Number</b>"
            self.bot.sendMessage(chat_id=update.effective_user.id, text=self.outgoing_message_text,
                                 parse_mode=telegram.ParseMode.HTML)
            self.cancel_button(bot, update)
            return self.DETAILS
        elif not self.order.insert_address(prov):
            self.outgoing_message_text = "Please retry 😱, put your address in right format\nRemember:\n " \
                                         "<b>Country, State, City, Street name and number, zipcode/postcode/cap</b> " \
                                         "🌍\nEx.(USA, Texas, Dallas, 501 Jefferson Blvd, TX 75203\nUK, England, " \
                                         "London, 206 Aldersgate)"
            self.bot.sendMessage(chat_id=update.effective_user.id, text=self.outgoing_message_text,
                                 parse_mode=telegram.ParseMode.HTML)
            self.cancel_button(bot, update)
            return self.ADDRESS

    def insert_contactDetails(self, bot, update):
        prov = str(update.message.text)
        if self.order.insert_contactDetails(prov):
            self.outgoing_message_text = "If you want to add any note or message 📑\nto your order write your message below and send it <b>if not press continue:</b>"
            self.bot.sendMessage(chat_id=update.effective_user.id, text=self.outgoing_message_text,
                                 parse_mode=telegram.ParseMode.HTML)

            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Continue ✈️', callback_data='continue')],
                [InlineKeyboardButton(text='Cancel ❌', callback_data='goback')]
            ])
            self.bot.sendMessage(chat_id=update.effective_user.id, text="What do you wanna do?", reply_markup=keyboard)
            return self.PAYMENT
        elif not self.order.insert_address(prov):
            self.outgoing_message_text = "Please retry 😱, put your address in the right format.\nRemember " \
                                         "this format:\n<b>Email, Telephone Number</b> "
            self.bot.sendMessage(chat_id=update.effective_user.id, text=self.outgoing_message_text,
                                 parse_mode=telegram.ParseMode.HTML)
            self.cancel_button(bot, update)
            return self.DETAILS

    def insert_note(self, bot, update):
        flag = True
        try:
            self.order.Notes = str(update.message.text)
            flag = False
        except AttributeError:
            if flag is True: self.order.Notes = "No notes"
            self.outgoing_message_text = "<b>💵Choose the payment type:💵</b>" \
                                         "\nIf you want more information about how to do the payment" \
                                         "please go back and visit our section payment do get all the information"
            self.bot.sendMessage(chat_id=update.effective_user.id, text=self.outgoing_message_text,
                                 parse_mode=telegram.ParseMode.HTML)
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='PayPal', callback_data='paypal')],
                [InlineKeyboardButton(text='Western Union %5 Discount', callback_data='westu')],
                [InlineKeyboardButton(text='Bitcoin %10 Discount', callback_data='bitcoin')],
                [InlineKeyboardButton(text='Cancel ❌', callback_data='goback')],
            ])
            bot.sendMessage(chat_id=update.effective_user.id, text="Select the payment:", reply_markup=keyboard)
            return self.FINALS

    def finalize_order(self, bot, update):
        print("Finalizzo Ordine")
        self.order.Order_n = "After sending the order"
        List_Order1, List_Order2 = self.order.get_orderDetails()
        self.outgoing_message_text = "Do you confirm the data entered?\n {} ".format(
            List_Order1)
        self.bot.sendMessage(chat_id=update.effective_user.id, text=self.outgoing_message_text,
                             parse_mode=telegram.ParseMode.HTML)
        self.outgoing_message_text = " {}\n<b>👍Do you confirm the data entered and the Order👍?</b>".format(
            List_Order2)
        self.bot.sendMessage(chat_id=update.effective_user.id, text=self.outgoing_message_text,
                             parse_mode=telegram.ParseMode.HTML)
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Send Order 🚀', callback_data='finish')],
            [InlineKeyboardButton(text='Cancel Order ❌', callback_data='goback')],
        ])
        self.bot.sendMessage(chat_id=update.effective_user.id, text="Final question", reply_markup=keyboard)
        return self.END

    def contanctforPayment(self):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Contact Mubby', url='https://t.me/buffy00')],
            [InlineKeyboardButton(text='Contatct Mubby_2', url='https://t.me/mubbyy')],
        ])
        return keyboard

    def send_Order(self, bot, update):
        if self.order.order_finished(update.effective_user.id) is True:
            list_Order1, list_Order2 = self.order.get_orderDetails()
            self.outgoing_message_text = "🥰Thank you for your order🥰\n {} \n ".format(
                list_Order1)
            self.bot.sendMessage(chat_id=update.effective_user.id, text=self.outgoing_message_text,
                                 parse_mode=telegram.ParseMode.HTML)
            self.outgoing_message_text = "{}\n<b>⚠...Save those details to contact us and made the payment." \
                                         "...⚠️\n\n...Restarting in 5s...</b>".format(
                list_Order2)
            self.bot.sendMessage(chat_id=update.effective_user.id, text=self.outgoing_message_text,
                                 parse_mode=telegram.ParseMode.HTML)
            self.outgoing_message_text = "🥰NEW ORDER FOR MUBBYLAB🥰\n {} \n ".format(
                list_Order1)
            self.bot.sendMessage(chat_id=TELEGRAM_CHANNELL_ID, text=self.outgoing_message_text,
                                 parse_mode=telegram.ParseMode.HTML)
            self.outgoing_message_text = "{}\n<b>⚠...Save those details and contact the buyer for the payment....⚠️" \
                                         "</b>\nCheck The link for more details\n\{}".format(
                list_Order2, LINK_TABLE_ORDERS)
            self.bot.sendMessage(chat_id=TELEGRAM_CHANNELL_ID, text=self.outgoing_message_text,
                                 parse_mode=telegram.ParseMode.HTML)
            self.bot.sendMessage(chat_id=update.effective_user.id, text="Now contact us to set-up the payment\n"
                                                                        "Click Below to open a chat with our Costumer "
                                                                        "Service",
                                 reply_markup=self.contanctforPayment(),
                                 parse_mode=telegram.ParseMode.HTML)
            return self.done(bot, update)
        else:
            self.outgoing_message_text = "Error, Order Cancelled, Please redo the order\n\n Wait 5s..resetting"
            self.bot.sendMessage(chat_id=update.effective_user.id, text=self.outgoing_message_text,
                                 parse_mode=telegram.ParseMode.HTML)
            return self.done(bot, update)

    def done(self, bot, update):
        sleep(5)
        return self.start_again(bot, update)

    def on_callback_query_payment(self, bot, update):
        query_data = update.callback_query.data
        print("SONO QUI")
        print(query_data)
        if query_data == 'paypal':
            print("Paypal")
            self.order.PaymentMethod = "Paypal"
            self.order.Discount = self.order.Discount + 0
            return self.finalize_order(bot, update)

        elif query_data == 'westu':
            self.order.PaymentMethod = "Wester Union"
            self.order.Discount = self.order.Discount + 5
            return self.finalize_order(bot, update)

        elif query_data == 'bitcoin':
            self.order.PaymentMethod = "Bitcoin"
            self.order.Discount = self.order.Discount + 10
            return self.finalize_order(bot, update)

        elif query_data == 'goback':
            print("Deleting Order..")
            self.outgoing_message_text = "❌❌❌Deleting Order...❌❌❌"
            bot.sendMessage(chat_id=update.effective_user.id, text=self.outgoing_message_text)
            return self.start_again(bot, update)

    def on_last_callbackQuery(self, bot, update):
        query_data = update.callback_query.data
        print(query_data)
        if query_data == 'goback':
            print("Deleting Order..")
            self.outgoing_message_text = "❌❌❌Deleting Order...❌❌❌"
            bot.sendMessage(chat_id=update.effective_user.id, text=self.outgoing_message_text)
            return self.start_again(bot, update)

        elif query_data == 'finish':
            return self.send_Order(bot, update)

    def on_continue_callbackQuery(self, bot, update):
        query_data = update.callback_query.data
        print(query_data)
        if query_data == 'goback':
            print("Deleting Order..")
            self.outgoing_message_text = "❌❌❌Deleting Order...❌❌❌"
            bot.sendMessage(chat_id=update.effective_user.id, text=self.outgoing_message_text)
            return self.start_again(bot, update)

        elif query_data == 'continue':
            return self.insert_note(bot, update)

    def endFall(self, bot, update):
        return ConversationHandler.END

    def execute(self):

        dp = self.updater.dispatcher

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', self.start)],
            states={
                self.MENU: [CallbackQueryHandler(self.on_callback_query_menu),
                            ],
                self.CODE: [CallbackQueryHandler(self.query_istheRightOrder),
                            MessageHandler(Filters.text, self.buyItems)
                            ],
                self.SIZE: [CallbackQueryHandler(self.on_callback_query_cancel),
                            MessageHandler(Filters.text, self.init_order)
                            ],
                self.NAME: [CallbackQueryHandler(self.on_callback_query_cancel),
                            MessageHandler(Filters.text, self.insert_PersonalDetails)
                            ],
                self.ADDRESS: [CallbackQueryHandler(self.on_callback_query_cancel),
                               MessageHandler(Filters.text, self.insert_address)
                               ],
                self.DETAILS: [CallbackQueryHandler(self.on_callback_query_cancel),
                               MessageHandler(Filters.text, self.insert_contactDetails)
                               ],
                self.PAYMENT: [CallbackQueryHandler(self.on_continue_callbackQuery),
                               MessageHandler(Filters.text, self.insert_note)
                               ],
                self.FINALS: [CallbackQueryHandler(self.on_callback_query_payment)
                              ],
                self.END: [CallbackQueryHandler(self.on_last_callbackQuery)
                           ],

            },
            fallbacks=[MessageHandler(Filters.regex('^Done$'), self.endFall)]
        )
        dp.add_handler(conv_handler)

        self.updater.start_polling()

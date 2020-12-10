
from tabulate import tabulate

from google_file import googleSheets
from datetime import date, datetime


class new_Order:
    def __init__(self, chat_id):
        self.Order_n = None
        self.Date = None
        self.Time = None
        self.D_Costumer = None
        self.D_State = None
        self.D_Country = None
        self.D_City = None
        self.D_StreetNameNumber = None
        self.D_ZipCode = None
        self.Telephone = None
        self.Email = None
        self.ItemsName = None
        self.ItemsSize = None
        self.Qty = None
        self.Price = None
        self.Notes = None
        self.Discount = None
        self.ShippingCost = None
        self.Total = None
        self.PaymentMethod = None
        if chat_id is None:
            print("You need to pass the chat_id in order to start an order")
        self.Chat_ID = chat_id

        self.data = googleSheets()

    def order_finished(self, chat_id):
        if self.Chat_ID == chat_id:
            self.Order_n = str(self.data.newRow + 40000)
            self.Date = str(date.today())
            self.Time = str(datetime.now().time())
            self.Total = float(self.Price) + float(self.ShippingCost)
            raw = [self.Order_n, self.Date, self.Time, self.D_Costumer, self.D_Country, self.D_State, self.D_City,
                   self.D_StreetNameNumber, self.D_ZipCode, self.Telephone, self.Email, "Standart Shipping", self.ItemsName,
                   self.ItemsSize, self.Qty, self.Price, self.Notes, self.Discount, self.ShippingCost, self.Total, "$",
                   self.PaymentMethod,
                   "notPaid", "notShipped"]
            print(raw)
            self.data.insert_Order(raw)
            return True
        else:
            return False

    def insert_address(self, string_address):
        list_address = string_address.split(", ")
        if len(list_address) != 5 or list_address is None:
            print('ADDRESS NOT FUNCTION')
            return False
        else:
            print(list_address)
            self.D_Country = list_address[0]
            self.D_State = list_address[1]
            self.D_City = list_address[2]
            self.D_StreetNameNumber = list_address[3]
            self.D_ZipCode = list_address[4]
            return True

    def insert_contactDetails(self, string_contact):
        list_contact = string_contact.split(",")
        if len(list_contact) != 2 or list_contact is None:
            return False
        else:
            print(list_contact)
            self.Email = list_contact[0]
            self.Telephone = list_contact[1]
            return True

    def get_orderDetails(self):
        self.Total = self.Price + self.ShippingCost - (((self.Discount - 30) / 100) * self.Price)
        print(self.Discount)
        Order_n_prov = "after confirming the order"
        labels = ["Order n : ", "Name Surname : ", "Country : ", "State : ", "City :", "Street name and number : ",
                  "Post Code : ", "Telephone : "]
        labels_2 = ["Email : ", "Shipping : ", " Items name : ", "Items size : ",
                    "Quantity", "Shipping cost : ", "Payment Method : ", "Discount : ", "Total : ", "Notes : "]

        raw = ["\n<b>{}</b>".format(self.Order_n), "\n<b>{}</b>".format(self.D_Costumer),
               "\n<b>{}</b>".format(self.D_Country), "\n<b>{}</b>".format(self.D_State),
               "\n<b>{}</b>".format(self.D_City),
               "\n<b>{}</b>".format(self.D_StreetNameNumber), "\n<b>{}</b>".format(self.D_ZipCode),
               "\n<b>{}</b>".format(self.Telephone)]
        raw2 = ["\n<b>{}</b>".format(self.Email), "\n<b>Standart Shipping</b>",
               "\n<b>{}</b>".format(self.ItemsName),
               "\n<b>{}</b>".format(self.ItemsSize), "\n<b>{}</b>".format(self.Qty),
               "\n<b>{}$</b>".format(str(self.ShippingCost)), "\n<b>{}</b>".format(self.PaymentMethod),
                "\n<b>{}%</b>".format(str(self.Discount)), "\n<b>{}$</b>".format(self.Total),
               "\n<b>{}</b>".format(self.Notes)]
        table = zip(labels, raw)
        table2 = zip(labels_2, raw2)
        list = tabulate(table, tablefmt="grid")
        list2 = tabulate(table2, tablefmt="grid")
        print(list)
        print(list2)
        return list, list2

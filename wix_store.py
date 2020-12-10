import re

import urllib3
import json

from tabulate import tabulate

from conf_wix_store import wixStore


class dataWixStore:
    def __init__(self):
        self.id_product = None
        self.id_code = None

        self.id_list = None
        self.imageId = None
        self.name_product = None
        self.price_product = None
        self.discountedPrice = None
        self.discountValue = None
        self.url = None
        self.data = None
        self.http = None
        self.req = None
        self.product = wixStore()

    def init_requestDataforID(self):
        try:
            self.product.id_product = self.id_product
            print(self.product.get_wixProductId())
            self.http = urllib3.PoolManager()
            self.req = self.http.request('GET', self.product.get_wixProductId())
            self.data = json.loads(self.req.data.decode('utf-8'))
        except ValueError:
            return False

    def init_requestDataforCode(self):
        try:
            self.product.id_code = self.id_code
            print(self.product.get_ProductByCode())
            self.http = urllib3.PoolManager()
            self.req = self.http.request('GET', self.product.get_ProductByCode())
            self.data = json.loads(self.req.data.decode('utf-8'))
            return True
        except ValueError:
            return False

    def get_nameProduct(self):
        for p in self.data['items']:
            self.name_product = p['name']
        return self.name_product

    def get_priceProduct(self):
        for p in self.data['items']:
            self.discountedPrice = p['price']
        return self.discountedPrice

    def get_discountedPrice(self):
        for p in self.data['items']:
            self.price_product = p['discountedPrice']
        return self.price_product

    def get_URL(self):
        for p in self.data['items']:
            self.url = p['productPageUrl']
        return_value = "https://www.mubbylab.xyz{}".format(self.url)
        return return_value

    def get_discountValue(self):
        for p in self.data['items']:
            self.discountValue = p['discount']
        return self.discountValue['value']

    def get_urlPic(self):
        for p in self.data['items']:
            for x in p['mediaItems']:
                self.imageId = x['id']
                break
        self.product.id_imageProduct = self.imageId
        return self.product.get_imageProductUrl()

    def get_listUrlPic(self):
        return_list = []
        i = 0
        for p in self.data['items']:
            for x in p['mediaItems']:
                self.product.id_imageProduct = x['id']
                return_list.append(self.product.get_imageProductUrl())
                i = i + 1
                if i == 3: break

        print(return_list)

        return return_list

    def check_size(self, stringToCheck):
        res = re.findall('\d*\.?\d+', stringToCheck)
        if res is not None and len(res) == 1:
            print("Numeric Size Found{}".format(re.findall('\d*\.?\d+', stringToCheck)))
            return True
        elif stringToCheck.find("XS") != -1 or stringToCheck.find("S") != -1 or stringToCheck.find(
                "M") != -1 or stringToCheck.find("L") != -1 \
                or stringToCheck.find("XL") != -1:
            print("Size Found")
            return True
        else:
            print(False)
            return False

    def check_nameSurname(self, stringToCheck):
        if stringToCheck.find(" ") != -1 and stringToCheck is not None:
            print("Format Accepted")
            return True
        else:
            print("Format name NOT Accepted")
            return False

    def get_lastItems(self):
        self.http = urllib3.PoolManager()
        self.req = self.http.request('GET', self.product.get_AllProduct())
        self.data = json.loads(self.req.data.decode('utf-8'))
        id_list = []
        name_list = []
        controlvar = 0
        for p in self.data['items']:
            var_string = p['_id']
            var_list = var_string.split("-", 1)
            id_list.append(var_list[0])
            name_list.append(p['name'])
            controlvar = controlvar + 1
        print(id_list)
        print(name_list)
        print("ci sono {} elementi".format(controlvar))
        table = zip(id_list, name_list)
        list_message = tabulate(table, tablefmt="grid")
        return id_list, list_message

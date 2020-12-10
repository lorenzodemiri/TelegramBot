import requests
import urllib3
import json

BASE_WIXSTORE_URL = 'https://www.mubbylab.xyz/_functions'
BASE_WIXSTOREIMAGE_URL = 'https://static.wixstatic.com/media/{}'


class wixStore:
    def __init__(self):
        self.id_product = None
        self.name_product = None
        self.id_imageProduct = None
        self.id_code = None
    def get_wixProductName(self):
        WIXSTORE_GETBYNAME = '{}/nameofproduct?name={}'.format(BASE_WIXSTORE_URL, self.name_product.replace(" ", "%20"))
        return WIXSTORE_GETBYNAME

    def get_wixProductId(self):
        WIXSTORE_GETBYID = '{}/productId?id={}'.format(BASE_WIXSTORE_URL, self.id_product)
        return WIXSTORE_GETBYID

    def get_imageProductUrl(self):
        return BASE_WIXSTOREIMAGE_URL.format(self.id_imageProduct)

    def get_AllProduct(self):
        WIXSTORE_GETALLPRODUCTS = '{}/AllProduct'.format(BASE_WIXSTORE_URL)
        return WIXSTORE_GETALLPRODUCTS

    def get_ProductByCode(self):
        WISTORE_GETPRODUCTBYCODE = '{}/productCode?id={}'.format(BASE_WIXSTORE_URL, self.id_code)
        return WISTORE_GETPRODUCTBYCODE
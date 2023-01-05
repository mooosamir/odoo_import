# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name": "All in one Advance Product Bundle(Sale/POS/Website/Purchase) App",
    "version": '16.0.0.0',
    "category": 'Sales',
    "summary": 'App website product pack website product kit pos product bundle pos product pack  website product combo pos bundle product bundle product pack kit all in one product bundle pack all in one bundle product pack shop product pack ecommerce product bundle pack',
    "description": """ This odoo app helps user to create and sale different product as bundle pack in sales order, purchase order , shop and point of sales order, User also have option for product pack stock management and to show product pack bundle and items on invoices. """,
    "author": "BrowseInfo",
    "website": "https://www.browseinfo.in",
    "price": 50,
    "currency": 'EUR',
    "depends": ['sale', 'product', 'stock', 'sale_stock', 'sale_management', 
        'purchase', 'product_bundle_all'],
    "data": [
        'views/config_inherit.xml',
        'views/product_inherit.xml',
    ],
    "license":'OPL-1',
    "installable": True,
    "application": True,
    "auto_install": False,
    "live_test_url":'https://youtu.be/vx7qqyCxYpM',
    "images":['static/description/Banner.gif'],

}

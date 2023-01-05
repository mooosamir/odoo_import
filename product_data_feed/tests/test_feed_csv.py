# Copyright © 2020 Garazd Creation (https://garazd.biz)
# @author: Yurii Razumovskyi (support@garazd.biz)
# @author: Iryna Razumovska (support@garazd.biz)
# License OPL-1 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

import csv
import logging

from odoo.tests import tagged
from odoo.tools.float_utils import float_compare

from .common import TestProductDataFeedCommon

_logger = logging.getLogger(__name__)


@tagged('post_install', '-at_install', 'product_data_feed')
class TestProductDataFeedCSV(TestProductDataFeedCommon):

    def setUp(self):
        super(TestProductDataFeedCSV, self).setUp()

    def test_get_csv_feed(self):
        _logger.info('Feed URL: %s', self.feed.url)
        r = self.url_open(self.feed.url)
        self.assertEqual(r.status_code, 200,
                         "The product data feed should return code 200")

        for row in [line for line in csv.DictReader(r.text.splitlines())]:
            if row['id'] == self.product_desk.id:
                self.assertEqual(
                    row['id'], str(self.product_desk.id),
                    "Field value should be correct.")
                self.assertEqual(
                    row['price'].split(' ')[1],  # Separate currency from price
                    '199.90',
                    "Product price should be with format '%.2f'.")
                self.assertEqual(
                    len(row['option']), 10,
                    "Value should be limited to 10 symbols.")
                self.assertEqual(
                    row['condition'], 'new',
                    'Column with the type "value" '
                    'should have a related value.')

                # Special columns
                self.assertEqual(
                    row['special_price'].split(' ')[1], '199.9',
                    "Product price should be without format.")

                product_r = self.url_open(row['link'])
                self.assertEqual(product_r.status_code, 200,
                                 "The product link should return code 200.")
                image_r = self.url_open(row['image_link'])
                self.assertEqual(image_r.status_code, 200,
                                 "The product image link should return code "
                                 "200.")

                # Availability
                self.assertEqual(
                    row['availability'], 'stock_in',
                    "Product should be in stock.")
                self.assertEqual(
                    float_compare(
                        float(row['qty']), 15.0, precision_digits=2
                    ), 0,
                    "15 pcs of the product should be in stock.")

    def test_get_csv_feed_pricelist(self):
        self.feed.pricelist_id = self.pricelist.id
        r = self.url_open(self.feed.url)
        self.assertEqual(r.status_code, 200,
                         "The product data feed should return code 200")

        for row in [line for line in csv.DictReader(r.text.splitlines())]:
            if row['id'] == self.product_desk.id:
                self.assertEqual(
                    row['price'].split(' ')[1],
                    '155.55',
                    "Product price should be with format '%.2f'.")
                self.assertEqual(
                    row['special_price'].split(' ')[1],
                    '155.55',
                    "Product price should be without format.")

    def test_get_csv_feed_availability_stock_out(self):
        self.feed.out_of_stock_mode = 'out_of_stock'
        r = self.url_open(self.feed.url)
        self.assertEqual(r.status_code, 200,
                         "The product data feed should return code 200")

        for row in [line for line in csv.DictReader(r.text.splitlines())]:
            if row['id'] == self.product_paper.id:
                self.assertEqual(
                    row['availability'], 'stock_out',
                    "Product should not be in stock.")
                self.assertEqual(
                    float_compare(float(row['qty']), 0, precision_digits=2), 0,
                    "Product qty in stock should be equal 0.")

    def test_get_csv_feed_availability_to_order(self):
        self.feed.out_of_stock_mode = 'order'
        r = self.url_open(self.feed.url)
        self.assertEqual(r.status_code, 200,
                         "The product data feed should return code 200")

        for row in [line for line in csv.DictReader(r.text.splitlines())]:
            if row['id'] == self.product_paper.id:
                self.assertEqual(
                    row['availability'], 'to_order',
                    "Product should be available to order.")
                self.assertEqual(
                    float_compare(float(row['qty']), 0, precision_digits=2), 0,
                    "Product qty in stock should be equal 0.")

    def test_get_csv_feed_stock_qty_type_virtual_available(self):
        self.feed.availability_type = 'virtual_available'
        self.env['stock.quant'].create({
            'product_id': self.product_desk.product_variant_id.id,
            'location_id': self.location.id,
            'reserved_quantity': 3.0,
        })
        r = self.url_open(self.feed.url)
        self.assertEqual(r.status_code, 200,
                         "The product data feed should return code 200")

        for row in [line for line in csv.DictReader(r.text.splitlines())]:
            if row['id'] == self.product_desk.id:
                self.assertEqual(
                    float_compare(
                        float(row['qty']), 12.0, precision_digits=2
                    ), 0,
                    "12 pcs of the product should be available in stock "
                    "(15 - 3 reserved).")

    def test_get_csv_feed_stock_qty_type_free_qty(self):
        self.feed.availability_type = 'free_qty'
        self.env['stock.quant'].create({
            'product_id': self.product_desk.product_variant_id.id,
            'location_id': self.location.id,
            'reserved_quantity': 10.0,
        })
        r = self.url_open(self.feed.url)
        self.assertEqual(r.status_code, 200,
                         "The product data feed should return code 200")

        for row in [line for line in csv.DictReader(r.text.splitlines())]:
            if row['id'] == self.product_desk.id:
                self.assertEqual(
                    float_compare(float(row['qty']), 5.0, precision_digits=2),
                    0,
                    "5 pcs of the product should be free in stock "
                    "(15 - 10 reserved).")

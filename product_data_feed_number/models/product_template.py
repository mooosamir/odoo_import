# Copyright © 2022 Garazd Creation (<https://garazd.biz>)
# @author: Yurii Razumovskyi (<support@garazd.biz>)
# @author: Iryna Razumovska (<support@garazd.biz>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    feed_gtin = fields.Char(
        string='GTIN',
        compute='_compute_feed_gtin',
        inverse='_inverse_feed_gtin',
        store=True,
    )
    feed_mpn = fields.Char(
        string='MPN',
        compute='_compute_feed_mpn',
        inverse='_inverse_feed_mpn',
        store=True,
    )

    @api.depends('product_variant_ids', 'product_variant_ids.feed_gtin')
    def _compute_feed_gtin(self):
        unique_variants = self.filtered(lambda tmpl: len(tmpl.product_variant_ids) == 1)
        for template in unique_variants:
            template.feed_gtin = template.product_variant_ids.feed_gtin
        for template in (self - unique_variants):
            template.feed_gtin = False

    def _inverse_feed_gtin(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.feed_gtin = template.feed_gtin

    @api.depends('product_variant_ids', 'product_variant_ids.feed_mpn')
    def _compute_feed_mpn(self):
        unique_variants = self.filtered(lambda tmpl: len(tmpl.product_variant_ids) == 1)
        for template in unique_variants:
            template.feed_mpn = template.product_variant_ids.feed_mpn
        for template in (self - unique_variants):
            template.feed_mpn = False

    def _inverse_feed_mpn(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.feed_mpn = template.feed_mpn

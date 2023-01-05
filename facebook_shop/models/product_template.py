# Copyright © 2022 Garazd Creation (<https://garazd.biz>)
# @author: Yurii Razumovskyi (<support@garazd.biz>)
# @author: Iryna Razumovska (<support@garazd.biz>)
# License OPL-1 (https://www.odoo.com/documentation/14.0/legal/licenses.html).

from odoo import api, fields, models
from .product_product import FB_AGE_GROUPS, FB_STATUSES


class ProductTemplate(models.Model):
    _inherit = "product.template"

    feed_fb_rich_text_description = fields.Html(
        string='HTML Description',
    )
    feed_fb_age_group = fields.Selection(
        selection=FB_AGE_GROUPS,
        string='Age Group',
        compute='_compute_feed_fb_age_group',
        inverse='_inverse_feed_fb_age_group',
        store=True,
    )
    feed_fb_status = fields.Selection(
        selection=FB_STATUSES,
        string='Status',
        compute='_compute_feed_fb_status',
        inverse='_inverse_feed_fb_status',
        store=True,
    )
    feed_fb_disabled_capability_ids = fields.Many2many(
        comodel_name='product.data.feed.fb_capability',
        string='Disabled Capabilities',
        compute='_compute_feed_fb_disabled_capability_ids',
        inverse='_inverse_feed_fb_disabled_capability_ids',
        store=True,
    )

    @api.depends('product_variant_ids', 'product_variant_ids.feed_fb_age_group')
    def _compute_feed_fb_age_group(self):
        unique_variants = self.filtered(lambda tmpl: len(tmpl.product_variant_ids) == 1)
        for template in unique_variants:
            template.feed_fb_age_group = template.product_variant_ids.feed_fb_age_group
        for template in (self - unique_variants):
            template.feed_fb_age_group = False

    def _inverse_feed_fb_age_group(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.feed_fb_age_group = \
                    template.feed_fb_age_group

    @api.depends('product_variant_ids', 'product_variant_ids.feed_fb_status')
    def _compute_feed_fb_status(self):
        unique_variants = self.filtered(lambda tmpl: len(tmpl.product_variant_ids) == 1)
        for template in unique_variants:
            template.feed_fb_status = template.product_variant_ids.feed_fb_status
        for template in (self - unique_variants):
            template.feed_fb_status = False

    def _inverse_feed_fb_status(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.feed_fb_status = \
                    template.feed_fb_status

    @api.depends('product_variant_ids',
                 'product_variant_ids.feed_fb_disabled_capability_ids')
    def _compute_feed_fb_disabled_capability_ids(self):
        unique_variants = self.filtered(lambda tmpl: len(tmpl.product_variant_ids) == 1)
        for template in unique_variants:
            template.feed_fb_disabled_capability_ids = \
                [(6, 0,
                  template.product_variant_ids.feed_fb_disabled_capability_ids.ids)]
        for template in (self - unique_variants):
            template.feed_fb_disabled_capability_ids = [(5, )]

    def _inverse_feed_fb_disabled_capability_ids(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.feed_fb_disabled_capability_ids = \
                    [(6, 0, template.feed_fb_disabled_capability_ids.ids)]


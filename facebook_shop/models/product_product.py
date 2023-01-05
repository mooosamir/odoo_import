# Copyright © 2022 Garazd Creation (<https://garazd.biz>)
# @author: Yurii Razumovskyi (<support@garazd.biz>)
# @author: Iryna Razumovska (<support@garazd.biz>)
# License OPL-1 (https://www.odoo.com/documentation/14.0/legal/licenses.html).

from odoo import fields, models

FB_AGE_GROUPS = [
    ('all ages', 'All Ages'),
    ('adult', 'Adult'),
    ('teen', 'Teen'),
    ('kids', 'Kids'),
    ('infant', 'Infant'),
    ('newborn', 'Newborn'),
]
FB_STATUSES = [
    ('active', 'Active'),
    ('archived', 'Archived'),
]


class ProductProduct(models.Model):
    _inherit = "product.product"

    feed_fb_age_group = fields.Selection(
        selection=FB_AGE_GROUPS,
        string='Age Group',
    )
    feed_fb_status = fields.Selection(
        selection=FB_STATUSES,
        default='active',
        string='Status',
    )
    feed_fb_disabled_capability_ids = fields.Many2many(
        comodel_name='product.data.feed.fb_capability',
        string='Disabled Capabilities',
    )

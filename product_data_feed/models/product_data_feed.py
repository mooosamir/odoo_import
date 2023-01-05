# Copyright © 2020 Garazd Creation (<https://garazd.biz>)
# @author: Yurii Razumovskyi (<support@garazd.biz>)
# @author: Iryna Razumovska (<support@garazd.biz>)
# License OPL-1 (https://www.odoo.com/documentation/14.0/legal/licenses.html#odoo-apps).

import uuid

from odoo.addons.base.models.res_partner import _lang_get, _tz_get
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import safe_eval

from odoo import _, api, fields, models


class ProductDataFeed(models.Model):
    _name = "product.data.feed"
    _inherit = ['mail.thread']
    _description = 'Product Data Feed'

    @api.model
    def _get_default_model_domain(self):
        return [('is_published', '=', True)]

    @api.model
    def _default_filename(self):
        return 'feed-%s' % str(uuid.uuid4())[:4]

    name = fields.Char(
        string='Name',
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )
    recipient_id = fields.Many2one(
        comodel_name='product.data.feed.recipient',
        string='Recipient',
        ondelete='cascade',
        required=True,
    )
    website_ids = fields.Many2many(
        comodel_name='website',
        string='Websites',
        help='Allow this data feed for selected websites. '
             'Allow for all if not set.',
    )
    url = fields.Char(
        string='Feed URL',
        readonly=True,
        compute='_compute_url',
    )
    use_token = fields.Boolean()
    access_token = fields.Char(
        string='Access Token',
        readonly=True,
    )
    file_type = fields.Selection(
        selection=[
            ('csv', 'CSV'),
            ('tsv', 'TSV'),
            ('xml', 'XML'),
        ],
        string='File Format',
        default='csv',
    )
    use_filename = fields.Boolean(
        string='Use a custom file name.',
        help='Use a custom file name for the feed.',
    )
    filename = fields.Char(
        string='File Name',
        default=_default_filename,
    )
    model_id = fields.Many2one(
        comodel_name='ir.model',
        string='Model',
        domain=[('model', 'in', ['product.product', 'product.template'])],
        ondelete='cascade',
        required=True,
        default=lambda self: self.env.ref('product.model_product_template'),
    )
    model_name = fields.Char(
        related='model_id.model',
        string='Model Name',
    )
    column_ids = fields.One2many(
        comodel_name='product.data.feed.column',
        inverse_name='feed_id',
        string='Columns',
        readonly=True,
    )
    column_count = fields.Integer(compute='_compute_column_count')
    item_count = fields.Integer(compute='_compute_item_count')
    model_domain = fields.Char(
        string='Model domain',
        help='The model domain for the feed.',
        default=_get_default_model_domain,
    )
    availability_type = fields.Selection(
        selection=[
            ('qty_available', 'Quantity On Hand'),
            ('virtual_available', 'Forecast Quantity'),
            ('free_qty', 'Free To Use Quantity'),
        ],
        string='Availability Type',
        help='Determine which stock measurement to use to calculate the stock '
             'of products.',
        default='qty_available',
        required=True,
    )
    stock_location_ids = fields.Many2many(
        comodel_name='stock.location',
        string='Stock Locations',
        domain=[('usage', '=', 'internal')],
        help='Get products only from these stock locations. Get products '
             'from all internal locations if not set.',
    )
    out_of_stock_mode = fields.Selection(
        selection=[
            ('order', 'Available for order'),
            ('out_of_stock', 'Out of stock'),
        ],
        string='Out of stock mode',
        help='Define which availability status should be used for products '
             'that are out of stock.',
        default='out_of_stock',
        required=True,
    )
    pricelist_id = fields.Many2one(
        comodel_name='product.pricelist',
        string='Pricelist',
        ondelete='set null',
    )
    sale_pricelist_id = fields.Many2one(
        comodel_name='product.pricelist',
        string='Sale Pricelist',
        help="Price list with discounted prices.",
        ondelete='set null',
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        default=lambda self: self.env.user.company_id.currency_id,
        required=True,
    )
    currency_position = fields.Selection(
        selection=[
            ('default', 'By default'),
            ('before', 'Before price'),
            ('after', 'After price'),
            ('none', 'Without currency code'),
        ],
        default='default',
        required=True,
    )
    product_root_category = fields.Char(
        help='Specify a custom root category for the "product_category" columns.',
    )
    image_resolution = fields.Selection(
        selection=[
            ('1920', 'Up to 1920 px'),
            ('1024', 'Up to 1024 px'),
            ('512', 'Up to 512 px'),
            ('256', 'Up to 256 px'),
            ('128', 'Up to 128 px'),
        ],
        default='1920',
    )
    lang = fields.Selection(
        selection=_lang_get,
        string='Language',
        default=lambda self: self.env.ref('base.default_user').lang,
        help="The language that will be used to translate all feed text values.",
    )
    tz = fields.Selection(
        selection=_tz_get,
        string='Timezone',
        default='UTC',
        required=True,
    )

    @api.constrains('access_token')
    def _check_access_token(self):
        for feed in self:
            if self.search_count([
                    ('access_token', '=', feed.access_token)]) > 1:
                raise ValidationError(_('The access token must be unique.'))

    @api.constrains('use_filename', 'filename')
    def _check_filename_unique(self):
        for feed in self:
            if self.search_count([('filename', '=', feed.filename),
                                  ('use_filename', '=', True)]) > 1:
                raise ValidationError(_('The filename must be unique.'))

    @api.depends('column_ids')
    def _compute_column_count(self):
        for feed in self:
            feed.column_count = len(feed.column_ids)

    def _compute_item_count(self):
        for feed in self:
            feed.item_count = len(feed._get_items())

    @api.onchange('use_token', 'access_token')
    def _onchange_use_token(self):
        for feed in self:
            if feed.use_token and not feed.access_token:
                feed.access_token = feed._generate_access_token()

    @api.model
    def _generate_access_token(self):
        return str(uuid.uuid4())

    def _get_base_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param(
            'web.base.url', default='')
        for feed in self.filtered('website_ids'):
            # Operate with a website domain only for the first website
            if feed.website_ids[0].domain:
                base_url = feed.website_ids[0]._get_http_domain()
        return base_url

    @api.depends('use_token', 'access_token')
    def _compute_url(self):
        for feed in self:
            # flake8: noqa: E501
            if feed.use_filename and feed.filename:
                feed_path = f'product_data/{feed.filename}.xml'
            else:
                feed_path = f'product_data/{feed._origin.id}/feed.{feed.file_type if feed.file_type != "tsv" else "csv"}'
            token = "?access_token=%s" % feed.access_token if feed.use_token else ""
            feed.url = f'{feed._get_base_url()}/{feed_path}{token}'

    def _get_availability_value(self, qty, column):
        self.ensure_one()
        value = ''
        if column.type == 'special' and column.special_type == 'availability':
            if qty <= 0:
                if self.out_of_stock_mode == 'order':
                    value = self.recipient_id.special_avail_order \
                            or 'available for order'
                else:
                    value = self.recipient_id.special_avail_out \
                            or 'out of stock'
            else:
                value = self.recipient_id.special_avail_in or 'in stock'
        return value

    def _get_items(self):
        """Get feed products."""
        self.ensure_one()
        items = self.env[self.model_name].search(safe_eval(self.model_domain))
        return items.with_context(lang=self.lang)

    def _get_product_qty(self, product) -> float:
        self.ensure_one()
        # PATCH to fix 'product.template' object has no attribute 'free_qty'
        products = product if self.model_name == 'product.product' \
            else product.product_variant_ids

        if not self.stock_location_ids:
            qty = sum(getattr(pv, self.availability_type)
                      for pv in products)
        else:
            qty = sum(getattr(pv.with_context(
                location=self.stock_location_ids.ids),
                self.availability_type) for pv in products)
        return qty

    def generate_data_file(self):
        """ Generate data feed file """
        self.ensure_one()
        rows = []

        if self.file_type == 'tsv':
            separator = '\t'
        else:
            separator = ','

        # Add file header
        columns = self.column_ids.mapped('name')
        rows.append(separator.join('"%s"' % name for name in columns))

        # Generate file rows
        for product in self._get_items():
            row = []
            # Clear column warnings
            self.column_ids.write({'feed_warning': None})
            for column in self.column_ids:
                row.append(column._get_value(product))
            rows.append(separator.join('"%s"' % value.replace('"', '')
                                       if value else '' for value in row))

        return '\n'.join(rows)

    def action_generate_token(self):
        self.ensure_one()
        self.access_token = self._generate_access_token()

    def action_record_list(self):
        self.ensure_one()
        return {
            'name': _('Feed Items'),
            'type': 'ir.actions.act_window',
            'res_model': self.model_name,
            'view_mode': 'tree,form',
            'domain': self.model_domain,
        }

    def action_download(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': '%s' % self.url,
            'target': 'self',
        }

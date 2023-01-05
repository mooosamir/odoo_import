from odoo import fields, models


class ProductDataFeed(models.Model):
    _inherit = "product.data.feed"

    file_type = fields.Selection(
        selection_add=[('xml', 'XML')],
        ondelete={'xml': 'set null'},
    )

    def generate_data_file_xml(self):
        """ Generate data feed XML file. Method declaration to inherit."""
        self.ensure_one()
        # Clear column warnings
        self.column_ids.write({'feed_warning': None})
        return ''

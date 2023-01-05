# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, _

class company(models.Model):
    _inherit = 'res.company'

    invoice_option_pack = fields.Selection([\
        ('main_pack','Only main Bundle product Pack'), 
        ('bundle_items','Only Bundle Pack On Invoice Lines'),
        ('main_budle_items','Main Bundle With Pack Item On Invoice Line')], 
        string="Invoice Option For Pack Item.", default="main_pack")

    stock_option_pack = fields.Selection([
        ('bundle_items','Deduct Stock Of Only Bundle Items'),
        ('both','Deduct Stock of Main Bundle and Bundle Items Both')],
        string="Stock Management For Bundle Product Pack." , default="bundle_items" )


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    invoice_option_pack = fields.Selection(string="Invoice Option For Pack Item.", 
        related="company_id.invoice_option_pack", readonly=False)

    stock_option_pack = fields.Selection(string="Stock Management For Bundle Product Pack.", 
        related="company_id.stock_option_pack", readonly=False)












# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo import SUPERUSER_ID



class ProcurementRule(models.Model):
	_inherit = 'stock.rule'

	def _get_stock_move_values(self, product_id, product_qty, product_uom, location_id, name, origin, values, group_id):
		result = super(ProcurementRule, self)._get_stock_move_values(product_id, product_qty, product_uom, location_id, name, origin, values, group_id)
		res_company = self.env.user.company_id

		if  product_id.pack_ids:
			for item in product_id.pack_ids:
				result.update({
					'product_id': item.product_id.id,
					'product_uom': item.uom_id and item.uom_id.id,
					'product_uom_qty': item.qty_uom,
					'origin': origin,
					})
		if product_id.is_pack== True :
			if res_company.stock_option_pack == 'both' :
				result.update({
						'product_id': product_id.id,
						'product_uom': product_uom.id,
						'product_uom_qty': product_qty,
						'origin': origin,
						})
		return result


class SaleOrderLine(models.Model):
	_inherit = 'sale.order.line'

	@api.depends('invoice_lines.move_id.state', 'invoice_lines.quantity')
	def _get_invoice_qty(self):
		"""
		Compute the quantity invoiced. If case of a refund, the quantity invoiced is decreased. Note
		that this is the case only if the refund is generated from the SO and that is intentional: if
		a refund made would automatically decrease the invoiced quantity, then there is a risk of reinvoicing
		it automatically, which may not be wanted at all. That's why the refund has to be created from the SO
		"""
		res_company = self.order_id.company_id
		for line in self:
			qty_invoiced = 0.0
			quan = 0
			for invoice_line in line.invoice_lines.filtered(lambda line : line.move_id.state != 'cancel' and line.move_id.move_type == 'out_invoice'):
				qty_invoiced += invoice_line.product_uom_id._compute_quantity(invoice_line.quantity, line.product_uom)
				if res_company.invoice_option_pack == 'bundle_items':
					if invoice_line.product_id.is_pack == False:
						for rec in invoice_line.sale_line_ids:
							quantity = []
							for record in rec.product_id.pack_ids:
								quantity.append(record.qty_uom)
							quan += qty_invoiced
							if sum(quantity):
								qty = quan//sum(quantity)
								qty_invoiced = int(qty)
				elif invoice_line.move_id.move_type == 'out_refund':
					qty_invoiced -= invoice_line.product_uom_id._compute_quantity(invoice_line.quantity, line.product_uom)
			line.qty_invoiced = qty_invoiced

	def _prepare_procurement_values(self, group_id):
		res = super(SaleOrderLine, self)._prepare_procurement_values(group_id=group_id)
		values = []
		if  self.product_id.pack_ids:
			for item in self.product_id.pack_ids:
				line_route_ids = self.env['stock.route'].browse(self.route_id.id)
				values.append({
					'name': item.product_id.name,
					'origin': self.order_id.name,
					'product_id': item.product_id.id,
					'product_qty': item.qty_uom * abs(self.product_uom_qty),
					'product_uom': item.uom_id and item.uom_id.id,
					'company_id': self.order_id.company_id,
					'group_id': group_id,
					'sale_line_id': self.id,
					'warehouse_id' : self.order_id.warehouse_id and self.order_id.warehouse_id,
					'location_id': self.order_id.partner_shipping_id.property_stock_customer.id,
					'route_ids': self.route_id and line_route_ids or [],
					'partner_dest_id': self.order_id.partner_shipping_id,
					'partner_id': self.order_id.partner_id.id
				})
			return values
		else:
			res.update({
			'company_id': self.order_id.company_id,
			'group_id': group_id,
			'sale_line_id': self.id,
			'route_ids': self.route_id,
			'warehouse_id': self.order_id.warehouse_id or False,
			'partner_dest_id': self.order_id.partner_shipping_id
		})    
		return res



class Sale_order(models.Model):
	_inherit = 'sale.order'

	def _create_invoices(self, grouped=False, final=False, date=None):
		res = super(Sale_order,self)._create_invoices(grouped,final,date)
		for inv in res :
			invoice = inv
			res_company = self.env.user.company_id
			values = []
			invoice_lines = self.env['account.move.line']
			if res_company.invoice_option_pack == 'bundle_items' :
				for line in invoice.invoice_line_ids :
					if line.product_id.is_pack == True :
						for pack in line.product_id.pack_ids :
							vals = {'product_id' : pack.product_id.id, 
									'quantity' : line.quantity * pack.qty_uom,
									 'price_unit' :pack.product_id.lst_price ,
									 'name': pack.product_id.name,
									 'move_id' : inv.id,
									 'account_id': line.account_id.id,
									 'product_uom_id':  pack.product_id.uom_id.id,
									 'tax_ids' :line.tax_ids.ids,
									 'sale_line_ids': [(6,0,line.sale_line_ids.ids)],
									  }            
							values.append((0,0,vals))   
						invoice.write({'invoice_line_ids': [(2,line.id,0)]})
				invoice.write({'invoice_line_ids' :values })

			if res_company.invoice_option_pack == 'main_budle_items' :
				for line in invoice.invoice_line_ids :
					if line.product_id.is_pack == True :
						for pack in line.product_id.pack_ids :
							vals = {	
								'product_id' : pack.product_id.id, 
								'quantity' : line.quantity * pack.qty_uom,
								'price_unit' :pack.product_id.lst_price ,
								'name': pack.product_id.name,
								'move_id' : inv.id,
								'account_id': line.account_id.id,
								'product_uom_id':  pack.product_id.uom_id.id,
								'tax_ids' :line.tax_ids.ids 
							}
							values.append((0,0,vals))
				invoice.write({'invoice_line_ids' :values })
		return res

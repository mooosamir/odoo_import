# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
##############################################################################

import math
from odoo import api, fields, models, _
from odoo.tools.float_utils import float_round

class ProductProduct(models.Model):
	_inherit = 'product.product'

	quantity = fields.Float('quantity')

	def _count_product_qty(self, quants_res):
		qty_available = 0.0
		incoming_qty = 0.0
		outgoing_qty = 0.0
		virtual_available = 0.0
		product_id = self.id
		for pid in self.pack_ids.filtered(lambda x: x.product_id.type == 'product'):
			if not pid.qty_uom == 0.0:
				temp_avail = math.floor(
					pid.product_id.qty_available / pid.qty_uom)
				if qty_available == 0.0:
					qty_available = temp_avail
				elif qty_available < temp_avail:
					qty_available = qty_available
				elif temp_avail < qty_available:
					qty_available = temp_avail

				temp_incoming = math.floor(
					pid.product_id.incoming_qty / pid.qty_uom)
				if incoming_qty == 0.0:
					incoming_qty = temp_incoming
				elif incoming_qty < temp_incoming:
					incoming_qty = incoming_qty
				elif temp_incoming < incoming_qty:
					incoming_qty = temp_incoming

				temp_outgoing = math.floor(
					pid.product_id.outgoing_qty / pid.qty_uom)
				if outgoing_qty == 0.0:
					outgoing_qty = temp_outgoing
				elif outgoing_qty < temp_outgoing:
					outgoing_qty = outgoing_qty
				elif temp_outgoing < outgoing_qty:
					outgoing_qty = temp_outgoing

				temp_virtual = math.floor(
					pid.product_id.virtual_available / pid.qty_uom)
				if virtual_available == 0.0:
					virtual_available = temp_virtual
				elif virtual_available < temp_virtual:
					virtual_available = virtual_available
				elif temp_virtual < virtual_available:
					virtual_available = temp_virtual
			else:
				qty_available = 0.0
				incoming_qty = 0.0
				outgoing_qty = 0.0
				virtual_available = 0.0

		qty_available = qty_available
		incoming_qty = incoming_qty
		outgoing_qty = outgoing_qty
		virtual_available = virtual_available
		reserved_quantity = quants_res.get(product_id, [False, 0.0])[1]
		return [qty_available, incoming_qty, outgoing_qty, virtual_available, reserved_quantity]

	def _compute_quantities_dict(self, lot_id, owner_id, package_id, from_date=False, to_date=False):
		domain_quant_loc, domain_move_in_loc, domain_move_out_loc = self._get_domain_locations()
		domain_quant = [('product_id', 'in', self.ids)] + domain_quant_loc
		dates_in_the_past = False
		# only to_date as to_date will correspond to qty_available
		to_date = fields.Datetime.to_datetime(to_date)
		if to_date and to_date < fields.Datetime.now():
			dates_in_the_past = True

		domain_move_in = [('product_id', 'in', self.ids)] + domain_move_in_loc
		domain_move_out = [('product_id', 'in', self.ids)] + domain_move_out_loc
		if lot_id is not None:
			domain_quant += [('lot_id', '=', lot_id)]
		if owner_id is not None:
			domain_quant += [('owner_id', '=', owner_id)]
			domain_move_in += [('restrict_partner_id', '=', owner_id)]
			domain_move_out += [('restrict_partner_id', '=', owner_id)]
		if package_id is not None:
			domain_quant += [('package_id', '=', package_id)]
		if dates_in_the_past:
			domain_move_in_done = list(domain_move_in)
			domain_move_out_done = list(domain_move_out)
		if from_date:
			date_date_expected_domain_from = [('date', '<=', from_date)]
			domain_move_in += date_date_expected_domain_from
			domain_move_out += date_date_expected_domain_from
		if to_date:
			date_date_expected_domain_to = [('date', '<=', to_date)]
			domain_move_in += date_date_expected_domain_to
			domain_move_out += date_date_expected_domain_to

		Move = self.env['stock.move'].with_context(active_test=False)
		Quant = self.env['stock.quant'].with_context(active_test=False)
		domain_move_in_todo = [('state', 'in',
								('waiting', 'confirmed', 'assigned', 'partially_available'))] + domain_move_in
		domain_move_out_todo = [('state', 'in',
								 ('waiting', 'confirmed', 'assigned', 'partially_available'))] + domain_move_out
		moves_in_res = dict((item['product_id'][0], item['product_qty']) for item in
							Move.read_group(domain_move_in_todo, ['product_id', 'product_qty'], ['product_id'],
											orderby='id'))
		moves_out_res = dict((item['product_id'][0], item['product_qty']) for item in
							 Move.read_group(domain_move_out_todo, ['product_id', 'product_qty'], ['product_id'],
											 orderby='id'))
		quants_res = dict((item['product_id'][0], (item['quantity'], item['reserved_quantity'])) for item in
						  Quant.read_group(domain_quant, ['product_id', 'quantity', 'reserved_quantity'],
										   ['product_id'], orderby='id'))
		if dates_in_the_past:
			# Calculate the moves that were done before now to calculate back in time (as most questions will be recent ones)
			domain_move_in_done = [('state', '=', 'done'), ('date', '>', to_date)] + domain_move_in_done
			domain_move_out_done = [('state', '=', 'done'), ('date', '>', to_date)] + domain_move_out_done
			moves_in_res_past = dict((item['product_id'][0], item['product_qty']) for item in
									 Move.read_group(domain_move_in_done, ['product_id', 'product_qty'], ['product_id'],
													 orderby='id'))
			moves_out_res_past = dict((item['product_id'][0], item['product_qty']) for item in
									  Move.read_group(domain_move_out_done, ['product_id', 'product_qty'],
													  ['product_id'], orderby='id'))

		res = dict()
		for product in self.with_context(prefetch_fields=False):
			product_id = product.id
			if not product_id:
				res[product_id] = dict.fromkeys(
					['qty_available', 'free_qty', 'incoming_qty', 'outgoing_qty', 'virtual_available'],
					0.0,
				)
				continue
			rounding = product.uom_id.rounding
			res[product_id] = {}
			config = self.env.user.company_id
			if product.is_pack == True and config.stock_option_pack == 'both':
				qty_available, incoming_qty, outgoing_qty, virtual_available, reserved_quantity = product._count_product_qty(quants_res)
				product.update({'quantity': float_round(qty_available, precision_rounding=product.uom_id.rounding)})
				res[product.id]['qty_available'] = float_round(qty_available, precision_rounding=product.uom_id.rounding)
				res[product_id]['free_qty'] = float_round(qty_available - reserved_quantity, precision_rounding=rounding)
				res[product.id]['incoming_qty'] = float_round(incoming_qty, precision_rounding=product.uom_id.rounding)
				res[product.id]['outgoing_qty'] = float_round(outgoing_qty, precision_rounding=product.uom_id.rounding)
				res[product.id]['virtual_available'] = float_round(virtual_available, precision_rounding=product.uom_id.rounding)

			elif product.is_pack == True and config.stock_option_pack == 'bundle_items':
				if product.quantity == 0:
					qty_available, incoming_qty, outgoing_qty, virtual_available, reserved_quantity = product._count_product_qty(quants_res)
					product.update({'quantity': float_round(qty_available, precision_rounding=product.uom_id.rounding)})
					res[product.id]['qty_available'] = float_round(qty_available, precision_rounding=product.uom_id.rounding)
					res[product_id]['free_qty'] = float_round(qty_available - reserved_quantity, precision_rounding=rounding)
					res[product.id]['incoming_qty'] = float_round(incoming_qty, precision_rounding=product.uom_id.rounding)
					res[product.id]['outgoing_qty'] = float_round(outgoing_qty, precision_rounding=product.uom_id.rounding)
					res[product.id]['virtual_available'] = float_round(virtual_available, precision_rounding=product.uom_id.rounding)
				else:
					origin_product_id = product._origin.id
					product_id = product.id
					if not origin_product_id:
						res[product_id] = dict.fromkeys(
							['qty_available', 'free_qty', 'incoming_qty', 'outgoing_qty', 'virtual_available'],
							0.0,
						)
						continue
					rounding = product.uom_id.rounding
					res[product_id] = {}
					if dates_in_the_past:
						qty_available = quants_res.get(origin_product_id, [0.0])[0] - moves_in_res_past.get(origin_product_id, 0.0) + moves_out_res_past.get(origin_product_id, 0.0)
					else:
						qty_available = quants_res.get(origin_product_id, [0.0])[0]
					reserved_quantity = quants_res.get(origin_product_id, [False, 0.0])[1]
					res[product_id]['qty_available'] = float_round(qty_available, precision_rounding=rounding)
					res[product_id]['free_qty'] = float_round(qty_available - reserved_quantity, precision_rounding=rounding)
					res[product_id]['incoming_qty'] = float_round(moves_in_res.get(origin_product_id, 0.0), precision_rounding=rounding)
					res[product_id]['outgoing_qty'] = float_round(moves_out_res.get(origin_product_id, 0.0), precision_rounding=rounding)
					res[product_id]['virtual_available'] = float_round(
						qty_available + res[product_id]['incoming_qty'] - res[product_id]['outgoing_qty'],
						precision_rounding=rounding)
			else:
				origin_product_id = product._origin.id
				product_id = product.id
				if not origin_product_id:
					res[product_id] = dict.fromkeys(
						['qty_available', 'free_qty', 'incoming_qty', 'outgoing_qty', 'virtual_available'],
						0.0,
					)
					continue
				rounding = product.uom_id.rounding
				res[product_id] = {}
				if dates_in_the_past:
					qty_available = quants_res.get(origin_product_id, [0.0])[0] - moves_in_res_past.get(origin_product_id, 0.0) + moves_out_res_past.get(origin_product_id, 0.0)
				else:
					qty_available = quants_res.get(origin_product_id, [0.0])[0]
				reserved_quantity = quants_res.get(origin_product_id, [False, 0.0])[1]
				res[product_id]['qty_available'] = float_round(qty_available, precision_rounding=rounding)
				res[product_id]['free_qty'] = float_round(qty_available - reserved_quantity, precision_rounding=rounding)
				res[product_id]['incoming_qty'] = float_round(moves_in_res.get(origin_product_id, 0.0), precision_rounding=rounding)
				res[product_id]['outgoing_qty'] = float_round(moves_out_res.get(origin_product_id, 0.0), precision_rounding=rounding)
				res[product_id]['virtual_available'] = float_round(
					qty_available + res[product_id]['incoming_qty'] - res[product_id]['outgoing_qty'],
					precision_rounding=rounding)
		return res

class ProductTemplate(models.Model):
	_inherit = 'product.template'

	quantity = fields.Float('quantity')

	def _compute_quantities_dict(self):
		# TDE FIXME: why not using directly the function fields ?
		variants_available = {
            p['id']: p for p in self.product_variant_ids.read(['qty_available', 'virtual_available', 'incoming_qty', 'outgoing_qty'])
        }
		prod_available = {}

		for template in self:
			qty_available = 0
			virtual_available = 0
			incoming_qty = 0
			outgoing_qty = 0
			config = self.env.user.company_id
			if template.is_pack == True and config.stock_option_pack == 'both':
				qty_available = 0.0
				virtual_available = 0.0
				for pid in template.pack_ids.filtered(lambda x : x.product_id.type == 'product'):
					if not pid.qty_uom == 0.0:
						temp = math.floor(pid.product_id.qty_available / pid.qty_uom)
						temp2 = math.floor(pid.product_id.virtual_available/ pid.qty_uom)
						
						if qty_available == 0.0:
							qty_available = temp
						elif qty_available < temp:
							qty_available = qty_available
						elif temp < qty_available:
							qty_available = temp

						if virtual_available == 0.0:
							virtual_available = temp2
						elif virtual_available < temp2:
							virtual_available = virtual_available
						elif temp2 < virtual_available:
							virtual_available = temp2
					else:
						qty_available = 0.0
						virtual_available = 0.0

					incoming_qty += pid.product_id.incoming_qty			
					outgoing_qty += pid.product_id.outgoing_qty

				qty_available = qty_available
				virtual_available = virtual_available
				prod_available[template.id] = {
					"qty_available": qty_available,
					"virtual_available": virtual_available,
					"incoming_qty": incoming_qty,
					"outgoing_qty": outgoing_qty,
				}

			else:
				for p in template.product_variant_ids:
					qty_available += variants_available[p.id]["qty_available"]
					virtual_available += variants_available[p.id]["virtual_available"]
					incoming_qty += variants_available[p.id]["incoming_qty"]
					outgoing_qty += variants_available[p.id]["outgoing_qty"]
				prod_available[template.id] = {
				"qty_available": qty_available,
				"virtual_available": virtual_available,
				"incoming_qty": incoming_qty,
				"outgoing_qty": outgoing_qty,
			}
		return prod_available
# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

   
    @api.depends('product_variant_ids.sales_amt')
    def _compute_sales_amt(self):
        for product in self:

            product.sales_amt = sum([p.sales_amt
                                     for p in product.product_variant_ids])
            print("####",product.sales_amt)

    sales_amt = fields.Float(compute='_compute_sales_amt', string='Sales amt')


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.depends('product_tmpl_id.sales_amt')
    def _compute_sales_amt(self):
        res = {}
        amt = 0.00
        domain = [
            ('order_id.state', 'in', ['sale', 'done']),
            ('product_id', 'in', self.ids),
        ]


        order_lines = self.env['sale.order.line'].search(domain)
        for line in order_lines:
            if res.get(line.product_id.id):
               res.get(line.product_id.id).update({'amt':res.get(line.product_id.id).get('amt')+line.price_subtotal})
            else:
                res[line.product_id.id] = {'amt':line.price_subtotal}
           
        for product in self:
            product.sales_amt = 0.0 
            if res and res.get(product.id):
                product.sales_amt=res.get(product.id).get('amt',0)



    sales_amt = fields.Float(compute='_compute_sales_amt', string='# Sales amt')

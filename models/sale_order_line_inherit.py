from odoo import models, fields


class SaleOrderLineInherit(models.Model):
    _inherit = "sale.order.line"

    milestone = fields.Integer(string="Milestone")

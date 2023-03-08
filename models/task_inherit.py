from odoo import models


class SaleOrderLineInherit(models.Model):
    _inherit = "project.task"

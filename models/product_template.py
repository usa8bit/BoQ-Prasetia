from odoo import models, fields, api


class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    satuan = fields.Selection([
        ('core', 'Core'),
        ('hp', 'hp'),
        ('ls', 'Ls'),
        ('m', 'm'),
        ('pcs', 'Pcs'),
        ('site', 'site'),
        ('unit', 'Units'),
    ], string="Satuan")
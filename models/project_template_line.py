from email.policy import default

from odoo import models, fields, api


class ProjectTypeTemplateLine(models.Model):
    _name = 'project.template.line'

    project_template_id = fields.Many2one('project.template', string="Project Template")
    product_id = fields.Many2one('product.template', string="Product Code", required=True)
    unit = fields.Selection([
        ('core', 'Core'),
        ('hp', 'hp'),
        ('ls', 'Ls'),
        ('m', 'm'),
        ('pcs', 'Pcs'),
        ('site', 'site'),
        ('unit', 'Units'),
    ], string='Unit', related='product_id.satuan')
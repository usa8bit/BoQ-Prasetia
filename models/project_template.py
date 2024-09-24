from odoo import models, fields, api


class ProjectTypeTemplate(models.Model):
    _name = 'project.template'

    name = fields.Char(string="Name Project Template")
    line_ids = fields.One2many('project.template.line', 'project_template_id', string="Template Lines")
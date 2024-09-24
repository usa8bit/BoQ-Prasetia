from odoo import models, fields, api


class ProjectPrasetia(models.Model):
    _name = 'project.prasetia'

    name = fields.Char(string="Project ID", required=True)
    site_name = fields.Char(string="Site Name", required=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    area = fields.Selection([
        ('1', 'AREA 1 (SUMATRA)'),
        ('2', 'AREA 2 (JABO, JABAR & BANTEN)'),
        ('3', 'AREA 3 (JAWA TENGAH, JAWA TIMUR & BALINUSRA)'),
        ('4', 'AREA 4 (KALIMANTAN, SULAWESI, MALUKU & PAPUA)')
    ], string="Area")
from odoo import models, fields, api


class ProjectPrasetia(models.Model):
    _name = 'project.prasetia'

    name = fields.Char(string="Project ID", required=True)
    site_name = fields.Char(string="Site Name", required=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    area = fields.Selection([
        ('AREA 1 (SUMATRA)', 'AREA 1 (SUMATRA)'),
        ('AREA 2 (JABO, JABAR & BANTEN)', 'AREA 2 (JABO, JABAR & BANTEN)'),
        ('AREA 3 (JAWA TENGAH, JAWA TIMUR & BALINUSRA)', 'AREA 3 (JAWA TENGAH, JAWA TIMUR & BALINUSRA)'),
        ('AREA 4 (KALIMANTAN, SULAWESI, MALUKU & PAPUA)', 'AREA 4 (KALIMANTAN, SULAWESI, MALUKU & PAPUA)')
    ], string="Area")
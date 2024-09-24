from odoo import api, models, fields, _


class BillOfQuantity(models.Model):
    _name = 'bill.of.quantity'
    _inherit = ['mail.thread']
    _description = 'Bill of Quantity'

    name = fields.Char(string="Reference", copy=False, readonly=True, default=lambda self: _('New'))
    date = fields.Date(string="SPK Date", track_visibility='onchange')
    partner_id = fields.Many2one('res.partner', string="Vendor Name", required=True, track_visibility='onchange')
    project_id = fields.Many2one('project.prasetia', string="Project ID", track_visibility='onchange')
    site_name = fields.Char(string="Site Name", related='project_id.site_name', readonly=True)
    area = fields.Selection([
        ('1', 'AREA 1 (SUMATRA)'),
        ('2', 'AREA 2 (JABO, JABAR & BANTEN)'),
        ('3', 'AREA 3 (JAWA TENGAH, JAWA TIMUR & BALINUSRA)'),
        ('4', 'AREA 4 (KALIMANTAN, SULAWESI, MALUKU & PAPUA)')
    ], string="Area", related='project_id.area')
    project_type_id = fields.Many2one('project.template',string="Project Type", track_visibility='onchange')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    spk_id = fields.Char(string="No SPK", track_visibility='onchange')
    spk_total = fields.Monetary(string="Total SPK", currency_field='currency_id', track_visibility='onchange')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('cancel', 'Cancel'),
        ('to draft', 'Set to Draft'),
        ('confirm', 'Waiting Logistic'),
        ('logistic', 'Waiting Vendor'),
        ('vendor', 'Waiting LPM'),
        ('lead', 'Approved')],
        string='Status',
        required=True,
        readonly=True,
        copy=False,
        tracking=True,
        default='draft',
    )
    procurement_id = fields.Many2one('res.users', string="Procurement")
    logistic_id = fields.Many2one('res.users', string="Logistic")
    vendor_id = fields.Many2one('res.users', string="Vendor")
    lpm_id = fields.Many2one('res.users', string="LPM")
    standard_ids = fields.One2many('bill.of.quantity.s.line', 'boq_id', string="Standard")
    non_standard_ids = fields.One2many('bill.of.quantity.ns.line', 'boq_id', string="Non Standard")

    @api.model
    def create(self, vals_list):
        if vals_list.get('name', _('New')) == _('New'):
            vals_list['name'] = self.env['ir.sequence'].next_by_code('bill.of.quantity') or _('New')
        res = super(BillOfQuantity, self).create(vals_list)
        return res

    @api.onchange('project_type_id')
    def _onchange_project_type(self):
        if self.project_type_id:
            self.standard_ids = [(5, 0, 0)]

            lines = []
            for line in self.project_type_id.line_ids:
                # Menambahkan line sesuai dengan product yang ada di project_type
                lines.append((0, 0, {
                    'product_id': line.product_id.id,
                }))
            self.standard_ids = lines
        else:
            self.standard_ids = [(5, 0, 0)]

    def action_draft(self):
        self.write({'state': 'draft'})
        return {}

    def action_confirm(self):
        user_id = self.env.user.id
        self.write({'state': 'confirm', 'procurement_id': user_id})

    def action_cancel(self):
        self.write({'state': 'cancel'})

    def action_logistic(self):
        user_id = self.env.user.id
        self.write({'state': 'logistic', 'logistic_id': user_id})

    def action_vendor(self):
        user_id = self.env.user.id
        self.write({'state': 'vendor', 'vendor_id': user_id})

    def action_lead(self):
        user_id = self.env.user.id
        self.write({'state': 'lead', 'lpm_id': user_id})
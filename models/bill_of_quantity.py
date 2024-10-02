from odoo import api, models, fields, _


class BillOfQuantity(models.Model):
    _name = 'bill.of.quantity'
    _inherit = ['mail.thread']
    _description = 'Bill of Quantity'
    _order = 'id desc'

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
    spk_total = fields.Monetary(string="Total SPK", compute="_compute_total_contract", store=True, currency_field='currency_id', track_visibility='onchange')
    total_deal_s = fields.Monetary(string="Total Deal Standard", compute="_compute_deal_diff_s", store=True, currency_field='currency_id', track_visibility='onchange')
    total_deal_ns = fields.Monetary(string="Total Deal Non Standard", compute="_compute_deal_diff_ns", store=True, currency_field='currency_id', track_visibility='onchange')
    total_deal = fields.Monetary(string="Total Deal", compute="_compute_total_deal_diff", store=True, currency_field='currency_id', track_visibility='onchange')
    total_diff_s = fields.Monetary(string="Total Different Standard", compute="_compute_deal_diff_s", store=True, currency_field='currency_id', track_visibility='onchange')
    total_diff_ns = fields.Monetary(string="Total Different Non Standard", compute="_compute_deal_diff_ns", store=True, currency_field='currency_id', track_visibility='onchange')
    total_diff = fields.Monetary(string="Total Different", compute="_compute_total_deal_diff", store=True, currency_field='currency_id', track_visibility='onchange')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('cancel', 'Cancel'),
        ('to draft', 'Set to Draft'),
        ('confirm', 'Waiting Procurement'),
        ('level 1', 'Waiting Vendor'),
        ('level 2', 'Waiting Logistic'),
        ('level 3', 'Waiting Coordinator'),
        ('level 4', 'Waiting PM'),
        ('level 5', 'Waiting LPM'),
        ('level 6', 'Waiting Procurement'),
        ('level 7', 'Waiting GM'),
        ('level 8', 'Approved')],
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
    gm_id = fields.Many2one('res.users', string="GM")
    standard_ids = fields.One2many('bill.of.quantity.s.line', 'boq_id', string="Standard")
    non_standard_ids = fields.One2many('bill.of.quantity.ns.line', 'boq_id', string="Non Standard")
    is_engineering_group = fields.Boolean(compute='_compute_is_engineering_group')
    is_procurement_group = fields.Boolean(compute='_compute_is_procurement_group')

    def _compute_is_engineering_group(self):
        for record in self:
            record.is_engineering_group = self.env.user.has_group('bill_of_quantity_prasetia.group_engineering')

    def _compute_is_procurement_group(self):
        for record in self:
            record.is_procurement_group = self.env.user.has_group('bill_of_quantity_prasetia.group_procurement')

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
                lines.append((0, 0, {
                    'product_id': line.product_id.id,
                }))
            self.standard_ids = lines
        else:
            self.standard_ids = [(5, 0, 0)]

    @api.depends('state', 'standard_ids.total_price_contract')
    def _compute_total_contract(self):
        for record in self:
            if record.state == 'level 1':
                total = sum(line.total_price_contract for line in record.standard_ids)
                record.spk_total = total

    @api.depends('standard_ids.total_price_deal', 'standard_ids.total_price_diff')
    def _compute_deal_diff_s(self):
        for record in self:
            total_deal = sum(line.total_price_deal for line in record.standard_ids)
            total_diff = sum(line.total_price_diff for line in record.standard_ids)
            record.total_deal_s = total_deal
            record.total_diff_s = total_diff

    @api.depends('non_standard_ids.total_price_deal','non_standard_ids.total_price_diff')
    def _compute_deal_diff_ns(self):
        for record in self:
            total_deal = sum(line.total_price_deal for line in record.non_standard_ids)
            total_diff = sum(line.total_price_diff for line in record.non_standard_ids)
            record.total_deal_ns = total_deal
            record.total_diff_ns = total_diff

    @api.depends('total_deal_s', 'total_deal_ns', 'total_diff_s', 'total_diff_ns')
    def _compute_total_deal_diff(self):
        for record in self:
            record.total_deal = record.total_deal_s + record.total_deal_ns
            record.total_diff = record.total_diff_s + record.total_diff_ns

    def action_draft(self):
        self.write({'state': 'draft'})
        return {}

    def action_confirm(self):
        self.write({'state': 'confirm'})

    def action_cancel(self):
        self.write({'state': 'cancel'})

    def action_level_1(self):
        self.write({'state': 'level 1'})

    def action_level_2(self):
        user_id = self.env.user.id
        self.write({'state': 'level 2', 'vendor_id': user_id})

    def action_level_3(self):
        user_id = self.env.user.id
        self.write({'state': 'level 3', 'logistic_id': user_id})

    def action_level_4(self):
        self.write({'state': 'level 4'})

    def action_level_5(self):
        self.write({'state': 'level 5'})

    def action_level_6(self):
        user_id = self.env.user.id
        self.write({'state': 'level 6', 'logistic_id': user_id})

    def action_level_7(self):
        user_id = self.env.user.id
        self.write({'state': 'level 7', 'procurement_id': user_id})

    def action_level_8(self):
        user_id = self.env.user.id
        self.write({'state': 'level 8', 'gm_id': user_id})
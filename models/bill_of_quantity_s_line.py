from odoo import api, models, fields

class BillOfQuantitySLine(models.Model):
    _name = 'bill.of.quantity.s.line'
    _description = 'Bill Of Quantity Line (Standard)'

    product_id = fields.Many2one('product.template', string="Product Code", required=True)
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    description = fields.Char(string="Description", required=True, related='product_id.name')
    unit = fields.Selection([
        ('core', 'Core'),
        ('hp', 'hp'),
        ('ls', 'Ls'),
        ('m', 'm'),
        ('pcs', 'Pcs'),
        ('site', 'site'),
        ('unit', 'Units'),
    ], string='Unit', related='product_id.satuan')
    qty_contract = fields.Float(string="Qty (Contract)")
    unit_price = fields.Monetary(string="Unit Price (Contract)", currency_field='currency_id', compute='_compute_unit_price', inverse='_set_unit_price', store=True)
    total_price_contract = fields.Monetary(string="Total (Contract)", compute="_compute_total_price_contract", store=True, currency_field='currency_id')
    qty_in = fields.Float(string="Qty In")
    qty_out = fields.Float(string="Qty Out")
    qty_implementation = fields.Float(string="Qty (Implementation)")
    qty_proposed = fields.Float(string="Qty (Proposed)", compute="_compute_values", store=True)
    qty_deal = fields.Float(string="Qty (Deal Final)", compute="_compute_values", store=True)
    total_price_deal = fields.Monetary(string="Total (Deal Final)", compute="_compute_values", store=True, currency_field='currency_id')
    qty_diff = fields.Float(string="Qty (Contract - Final)", compute="_compute_values", store=True)
    total_price_diff = fields.Monetary(string="Total (Contract - Final)", compute="_compute_values", store=True, currency_field='currency_id')
    boq_id = fields.Many2one('bill.of.quantity', string="Bill Of Quantity Reference", ondelete='cascade')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('cancel', 'Cancel'),
        ('to draft', 'Set to Draft'),
        ('confirm', 'Waiting Procurement'),
        ('level 1', 'Waiting Vendor'),
        ('level 2', 'Waiting Logistic'),
        ('level 3', 'Waiting Kord. Waspang'),
        ('level 4', 'Waiting PM'),
        ('level 5', 'Waiting LPM'),
        ('level 7', 'Waiting GM'),
        ('level 8', 'Approved')],
        string='Status',
        related='boq_id.state',
    )
    is_engineering_group = fields.Boolean(compute='_compute_is_engineering_group')
    is_procurement_group = fields.Boolean(compute='_compute_is_procurement_group')
    is_logistic_group = fields.Boolean(compute='_compute_is_logistic_group')
    is_mitra_group = fields.Boolean(compute='_compute_is_mitra_group')

    def _compute_is_engineering_group(self):
        for record in self:
            record.is_engineering_group = self.env.user.has_group('bill_of_quantity_prasetia.group_engineering')

    def _compute_is_procurement_group(self):
        for record in self:
            record.is_procurement_group = self.env.user.has_group('bill_of_quantity_prasetia.group_procurement')

    def _compute_is_logistic_group(self):
        for record in self:
            record.is_logistic_group = self.env.user.has_group('bill_of_quantity_prasetia.group_logistic')

    def _compute_is_mitra_group(self):
        for record in self:
            record.is_mitra_group = self.env.user.has_group('bill_of_quantity_prasetia.group_mitra')

    @api.depends('product_id')
    def _compute_unit_price(self):
        for line in self:
            line.unit_price = line.product_id.list_price

    def _set_unit_price(self):
        for line in self:
            if line.product_id:
                line.product_id.list_price = line.unit_price

    @api.depends('qty_contract', 'unit_price')
    def _compute_total_price_contract(self):
        for line in self:
            line.total_price_contract = line.qty_contract * line.unit_price

    @api.depends('state', 'qty_implementation', 'unit_price', 'qty_contract', 'total_price_contract')
    def _compute_values(self):
        for line in self:
            if line.state >= 'level 7':
                line.qty_proposed = line.qty_implementation
                line.qty_deal = line.qty_implementation
                line.total_price_deal = line.qty_deal * line.unit_price
                line.qty_diff = line.qty_deal - line.qty_contract
                line.total_price_diff = line.total_price_deal - line.total_price_contract
            else:
                line.qty_proposed = 0.0
                line.qty_deal = 0.0
                line.total_price_deal = 0.0
                line.qty_diff = 0.0
                line.total_price_diff = 0.0
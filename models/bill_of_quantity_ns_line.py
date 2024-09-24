from odoo import api, models, fields

class BillOfQuantityNSLine(models.Model):
    _name = 'bill.of.quantity.ns.line'
    _description = 'Bill Of Quantity Line (Non Standard)'

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
    unit_price = fields.Monetary(string="Unit Price (Contract)", currency_field='currency_id')
    total_price_contract = fields.Monetary(compute="_compute_total_price_contract", string="Total (Contract)", store=True, currency_field='currency_id')
    qty_in = fields.Float(string="Qty In")
    qty_out = fields.Float(string="Qty Out")
    qty_implementation = fields.Float(string="Qty (Implementation)")
    qty_proposed = fields.Float(string="Qty (Proposed)")
    qty_deal = fields.Float(string="Qty (Deal Final)")
    total_price_deal = fields.Monetary(compute="_compute_total_price_deal", string="Total (Deal Final)", store=True, currency_field='currency_id')
    qty_diff = fields.Float(compute="_compute_qty_diff", string="Qty (Contract - Final)")
    total_price_diff = fields.Monetary(compute="_compute_total_price_diff", string="Total (Contract - Final)", store=True, currency_field='currency_id')
    boq_id = fields.Many2one('bill.of.quantity', string="Bill Of Quantity Reference", ondelete='cascade')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('cancel', 'Cancel'),
        ('to draft', 'Set to Draft'),
        ('confirm', 'Waiting Logistic'),
        ('logistic', 'Waiting Vendor'),
        ('vendor', 'Waiting LPM'),
        ('lead', 'Approved')],
        string='Status',
        related='boq_id.state',
    )

    @api.depends('qty_contract', 'unit_price')
    def _compute_total_price_contract(self):
        for line in self:
            line.total_price_contract = line.qty_contract * line.unit_price

    @api.depends('qty_deal', 'unit_price')
    def _compute_total_price_deal(self):
        for line in self:
            line.total_price_deal = line.qty_deal * line.unit_price

    @api.depends('qty_contract', 'qty_deal')
    def _compute_qty_diff(self):
        for line in self:
            line.qty_diff = line.qty_deal - line.qty_contract

    @api.depends('total_price_contract', 'total_price_deal')
    def _compute_total_price_diff(self):
        for line in self:
            line.total_price_diff = line.total_price_deal - line.total_price_contract
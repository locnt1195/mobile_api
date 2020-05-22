from odoo import api, fields, models


class PartnerTransaction(models.Model):
    _name = 'partner.transaction'
    _order = 'create_date DESC'

    description = fields.Text('Description')
    from_partner_id = fields.Many2one(
        'res.partner',
        'From Partner',
        required=True
    )
    to_partner_id = fields.Many2one(
        'res.partner',
        'To Partner',
        required=True
    )
    amount = fields.Float('Amount', default=0)

    @api.multi
    def update_partner_amount(self):
        self.ensure_one()
        self.from_partner_id.debit += self.amount
        self.from_partner_id.balance -= self.amount
        self.to_partner_id.credit += self.amount
        self.to_partner_id.balance += self.amount

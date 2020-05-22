from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class ResParter(models.Model):
    _inherit = 'res.partner'

    debit = fields.Float('Debit')
    credit = fields.Float('Credit')
    balance = fields.Float('Balance')
    transaction_sent_ids = fields.One2many(
        'partner.transaction',
        'from_partner_id',
        'Sent Histories'
    )
    transaction_receive_ids = fields.One2many(
        'partner.transaction',
        'to_partner_id',
        'Received Histories'
    )

    @api.multi
    def action_make_transaction(self, to_partner_id, value, description=''):
        self.check_balance(value)
        self.check_valid_partner(to_partner_id)
        return self._create_transaction(to_partner_id, value, description)

    @api.multi
    def check_valid_partner(self, to_partner_id):
        self.ensure_one()
        if to_partner_id == self.id:
            raise ValidationError(
                'Cannot make transaction to same Partner')

        partner = self.search([('id', '=', to_partner_id)], limit=1)
        if not partner:
            raise ValidationError(
                'Partner not exist with id %s.' % to_partner_id)

    @api.multi
    def check_balance(self, value):
        self.ensure_one()
        if self.balance < value:
            raise ValidationError('Not enough money.')

    @api.multi
    def _create_transaction(self, to_partner_id, value, description=''):
        self.ensure_one()
        vals = {
            'from_partner_id': self.id,
            'to_partner_id': to_partner_id,
            'amount': value
        }
        if description:
            vals['description'] = description
        transaction = self.transaction_sent_ids.create(vals)
        transaction.update_partner_amount()
        return transaction

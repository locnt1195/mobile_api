import logging
import json
from collections import OrderedDict
import werkzeug.wrappers

from odoo import _, http
from odoo.http import local_redirect, request
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons.website.controllers.main import Website
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF


class Controller(Website):

    @http.route(['/api/partner/transactions'],
                type='http', auth="user", methods=['GET'])
    def get_partner_transactions(self, from_date=None, to_date=None, limit=None):
        user = request.env['res.users'].browse(request.uid)
        partner = user.partner_id
        limit = limit and int(limit) or None
        transactions = partner.get_transactions(from_date, to_date, limit)
        data = [
            {
                'description': transaction.description or '',
                'amount': transaction.from_partner_id == partner and -transaction.amount or transaction.amount,
                'date': transaction.create_date.strftime(DTF),
                'partner': {
                    'name': transaction.from_partner_id == partner and
                    (transaction.to_partner_id.name, transaction.to_partner_id.id) or
                    (transaction.from_partner_id.name, transaction.from_partner_id.id)
                }
            }
            for transaction in transactions
        ]
        return werkzeug.wrappers.Response(
            status=200,
            content_type="application/json; charset=utf-8",
            headers=[("Cache-Control", "no-store"), ("Pragma", "no-cache")],
            response=json.dumps(
                {
                    'success': 1,
                    'data': data
                }
            ),
        )

    @http.route(['/api/partner/balance'],
                type='http', auth="user", methods=['GET'])
    def get_partner_balance(self):
        user = request.env['res.users'].browse(request.uid)
        partner = user.partner_id
        return werkzeug.wrappers.Response(
            status=200,
            content_type="application/json; charset=utf-8",
            headers=[("Cache-Control", "no-store"), ("Pragma", "no-cache")],
            response=json.dumps(
                {
                    'success': 1,
                    'data': {
                        'balance': partner.balance}
                }
            ),
        )

    @http.route(['/api/partner/sent'],
                type='http', auth="user", methods=['POST'], csrf=False)
    def make_transaction(self, **kw):
        logging.info('make transaction with' + ' %s' % kw)
        user = request.env['res.users'].browse(request.uid)
        result = {
            'success': 1
        }
        partner = user.partner_id
        try:
            to_partner_id = int(kw.get('parter_id', False))
            amount = float(kw.get('amount', 0))
        except Exception as e:
            result.update({
                'success': 0,
                'message': 'Invalid param data type.'
            })
            return werkzeug.wrappers.Response(
                status=200,
                content_type="application/json; charset=utf-8",
                headers=[("Cache-Control", "no-store"), ("Pragma", "no-cache")],
                response=json.dumps(result),
            )

        description = kw.get('description', '')
        if not to_partner_id:
            message = 'Cannot make transaction without destination Partner'
            logging.warning(message + ' %s' % kw)
            result.update({
                'success': 0,
                'message': message
            })
        elif amount < 10:
            message = 'Transaction Amount must be greater than 10'
            logging.warning(message)
            result.update({
                'success': 0,
                'message': message
            })
        else:
            try:
                transaction = partner.action_make_transaction(
                    to_partner_id, amount, description)
                result.update({
                    'message': 'Successfull Transaction',
                    'transaction_date': transaction.create_date.strftime(DTF),
                    'balance': partner.balance

                })
            except ValidationError as e:
                logging.error(e)
                result.update({
                    'success': 0,
                    'message': '%s' % e,
                    'balance': partner.balance
                })
            except Exception as e:
                logging.error(e)
                result.update({
                    'success': 0,
                    'message': 'Transaction Failed. Please try again later. '
                               'If you need more information please contact '
                               'our support',
                })

        return werkzeug.wrappers.Response(
            status=200,
            content_type="application/json; charset=utf-8",
            headers=[("Cache-Control", "no-store"), ("Pragma", "no-cache")],
            response=json.dumps(result),
        )

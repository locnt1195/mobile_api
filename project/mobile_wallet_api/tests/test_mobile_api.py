from odoo.tests.common import TransactionCase


class TestMobileApi(TransactionCase):

    def setUp(self):
        super(TestMobileApi, self).setUp()
        Users = self.env['res.users'].with_context(no_reset_password=True)

        group_user = self.env.ref('base.group_user')
        contact_creation = self.env.ref('base.group_partner_manager')
        # Create a users
        self.user_1 = Users.create({
            'name': 'User 1',
            'login': 'user1',
            'email': 'user1@example.com',
            'groups_id': [(6, 0, [group_user.id, contact_creation.id])]
        })
        # Init partner balance to sent money
        self.user_1.partner_id.balance = 1000
        self.user_2 = Users.create({
            'name': 'User 2',
            'login': 'user2',
            'email': 'user2@example.com',
            'groups_id': [(6, 0, [group_user.id, contact_creation.id])]
        })

    def test_get_user_balance(self):
        self.assertEquals(1000, self.user_1.partner_id.balance)

    def test_make_transacton(self):
        partner_1 = self.user_1.partner_id.sudo(self.user_1)
        partner_2 = self.user_2.partner_id.sudo(self.user_1)
        partner_1.action_make_transaction(
            partner_2.id, 500, 'Hello User 2'
        )
        self.assertEquals(500, partner_1.balance)
        self.assertEquals(500, partner_2.balance)

    def test_get_transactions(self):
        partner_1 = self.user_1.partner_id.sudo(self.user_1)
        partner_2 = self.user_2.partner_id.sudo(self.user_1)
        partner_1.action_make_transaction(
            partner_2.id, 500, 'Hello User 2'
        )
        self.assertEquals(500, partner_1.balance)
        self.assertEquals(500, partner_2.balance)
        self.assertEquals(1, len(partner_1.get_transactions()))

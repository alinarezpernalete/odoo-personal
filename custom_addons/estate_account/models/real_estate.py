from odoo import fields, models

class RealEstateModel(models.Model):
    _inherit = 'real_estate_model'

    def sold_property(self):
        for record in self:
            buyer = record['buyer'].id
            result = self.env['account.move'].create(
                {
                    'partner_id': buyer,
                    'move_type': 'out_invoice',
                    'journal_id': '1',
                    'currency_id': '1'
                }
            )
        # return super(RealEstateModel, self).sold_property()
        return result
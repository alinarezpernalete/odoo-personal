from odoo import fields, models, Command

class RealEstateModel(models.Model):
    _inherit = 'real_estate_model'

    def sold_property(self):
        #super().sold_property()
        for record in self:
            buyer = record['buyer'].id
            self.env['account.move'].create(
                {
                    'partner_id': buyer,
                    'move_type': 'out_invoice',
                    'journal_id': 1,
                    'invoice_line_ids': [
                        Command.create({
                            'name': '6 percent of selling price',
                            'quantity': 1,
                            'price_unit': self.selling_price * 0.06
                        })
                    ]
                }
            )        
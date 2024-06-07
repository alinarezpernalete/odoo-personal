from odoo import api, fields, models

class RealEstatePropertyType(models.Model):
    _name = "real_estate_property_type"
    _description = "Real Estate Property Type"
    _order = "name"

    name = fields.Char(required=True)
    property_ids = fields.One2many("real_estate", "property_type_id", string="Real Estate Property")
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    offer_ids = fields.One2many("real_estate_property_offer", "property_type", string="Real Estate Offer")
    offer_count = fields.Integer(compute="_compute_offer_count")

    _sql_constraints = [
        ('name', 'UNIQUE(name)',
         'The name should be unique.')
    ]

    @api.depends("offer_ids.property_type")
    def _compute_offer_count(self):
        for record in self:
            self.offer_count = self.env['real_estate_property_offer'].search_count([('property_type','=',record.name)])

    def action_view_offer(self):
        return {
            'name': ('Offers'),
            'res_model': 'real_estate_property_offer',
            'view_mode': 'list,form',
            'context': {},
            'domain': [('property_type', '=', self.name)],
            'target': 'current',
            'type': 'ir.actions.act_window'
        }
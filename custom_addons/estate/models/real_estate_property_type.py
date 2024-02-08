from odoo import api, fields, models

class RealEstatePropertyType(models.Model):
    _name = "real_estate_property_type"
    _description = "Real Estate Property Type"
    _order = "name"

    name = fields.Char(required=True)
    property_ids = fields.One2many("real_estate_model", "property_type_id", string="Real Estate Property")
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")

    _sql_constraints = [
        ('name', 'UNIQUE(name)',
         'The name should be unique.')
    ]
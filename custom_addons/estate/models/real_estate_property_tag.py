from odoo import api, fields, models

class RealEstatePropertyTag(models.Model):
    _name = "real_estate_property_tag"
    _description = "Real Estate Property Tag"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()

    _sql_constraints = [
        ('name', 'UNIQUE(name)',
         'The name should be unique.')
    ]
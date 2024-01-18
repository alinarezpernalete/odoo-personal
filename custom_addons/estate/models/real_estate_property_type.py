from odoo import api, fields, models

class RealEstatePropertyType(models.Model):
    _name = "real_estate_property_type"
    _description = "Real Estate Property Type"

    name = fields.Char(required=True)
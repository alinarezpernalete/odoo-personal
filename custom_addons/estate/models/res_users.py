from odoo import fields, models

class ResUsers(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many("real_estate", "salesperson", string="Properties related", domain="['|', ('state', '=', '1'), ('state', '=', '2')]")
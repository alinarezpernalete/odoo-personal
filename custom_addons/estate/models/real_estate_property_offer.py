from odoo import api, fields, models, exceptions
from dateutil.relativedelta import relativedelta

class RealEstatePropertyOffer(models.Model):
    _name = "real_estate_property_offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection([('1','Accepted'), ('2','Refused')], copy=False)
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("real_estate_model", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_computed_date_deadline", inverse="_computed_date_deadline_inverse")
    property_type = fields.Char(related="property_id.property_type_id.name", store=True) # Kind of INNER JOIN, which makes a union between them : real_estate_property_offer -> real_estate -> property_type_id

    @api.depends("create_date","validity","date_deadline")
    def _computed_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + relativedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)

    def _computed_date_deadline_inverse(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days
            else:
                record.validity = (record.date_deadline - fields.Date.today()).days

    def accept_action(self):
        self.status = "1"
        self.property_id.selling_price = self.price
        self.property_id.buyer = self.partner_id
        self.property_id.state = "3"

    def refuse_action(self):
        self.status = "2"
        self.property_id.buyer = 1

    def create(self, vals_list):
        # result es el registro como tal
        # vals_list es la lista de los datos dentro del registro
        result = super().create(vals_list) 
        result.property_id.state = '2'
        price = result.price

        if float(price) < float(result.property_id.best_price):
            raise exceptions.ValidationError("You cannot offer lower than: " + str(result.property_id.best_price))    
        
        return result
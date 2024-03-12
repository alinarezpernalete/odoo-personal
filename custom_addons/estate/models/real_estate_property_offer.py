from odoo import api, fields, models, http
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
        self.property_id.selling_price = 0
        self.property_id.buyer = 1

    @http.route('/my_controller/show_message', type='http', auth='user')
    def some_function(self):
        # Create a new record using the model object's create method
        # new_record = self.env['real_estate_property_offer'].create({
        #     'price': 199.00,
        #     # ... other field values
        # })
        # Do something with the newly created record (optional)
        # return new_record
        self.env.user.flash_message('Success!', "NEW")
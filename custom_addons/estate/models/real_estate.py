from odoo import api, fields, models, exceptions
from dateutil.relativedelta import relativedelta

class RealEstateModel(models.Model):
    _name = "real_estate_model"
    _description = "Real Estate Model"
    _order = "id desc"

    title = fields.Char()
    description = fields.Char(size=300, trim=True)
    postcode = fields.Char()
    expected_price = fields.Float()
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean(default=False)
    garden = fields.Boolean(default=False)
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([("1", "North"),
                                           ("2", "South"),
                                           ("3", "East"),
                                           ("4", "West")])
    available_from = fields.Date(default=fields.Date.today() + relativedelta(months=3), copy=False)
    active = fields.Boolean(default=True)
    state = fields.Selection([("1", "New"), 
                              ("2", "Offer Received"),
                              ("3", "Offer Accepted"),
                              ("4", "Sold"),
                              ("5", "Canceled")], default="1", required=True, copy=False)
    property_type_id = fields.Many2one(comodel_name='real_estate_property_type', string="Real Estate Property Type")
    salesperson = fields.Many2one('res.users', string='Salesperson', index=True, default=lambda self: self.env.user)
    buyer = fields.Many2one('res.partner', string='Buyer', index=True, copy=False)
    tag_ids = fields.Many2many("real_estate_property_tag", string="Real Estate Property Tag")
    offer_ids = fields.One2many("real_estate_property_offer", "property_id", string="Real Estate Property Offer")
    total_area = fields.Integer(compute="_compute_area")
    best_price = fields.Float(compute="_compute_best_price")
    _sql_constraints = [
        ('expected_price', 'CHECK(expected_price > 0.00)','The expected price should be major than 0.'),
        ('selling_price', 'CHECK(selling_price > 0.00)','The selling price should be major than 0.')
    ]

    @api.depends("living_area", "garden_area")
    def _compute_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    
    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if len(record.offer_ids) > 0:
                self.best_price = max(record.offer_ids.mapped('price')) 
            else:
                self.best_price = 0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden == True:
            self.garden_area = 10
            self.garden_orientation = "1"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    def sold_property(self):
        if self.state != "5":
            if self.state != "4":
                self.state = "4"
            else:
                raise exceptions.UserError("The property is already sold.")
        else:
            raise exceptions.UserError("A canceled property cannot be set as sold, and a sold property cannot be canceled.")
    
    def cancel_property(self):
        if self.state != "4":
            if self.state != "5":
                self.state = "5"
            else:
                raise exceptions.UserError("The property is already canceled.")
        else:
            raise exceptions.UserError("A canceled property cannot be set as sold, and a sold property cannot be canceled.")

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for selling_price in self:
            if self.state != "5":
                if (self.selling_price < (self.expected_price * (90 / 100))) and (self.selling_price > 0):
                    raise exceptions.UserError("The selling price cannot be lower than 90 percent of the expected price.")
            else:
                raise exceptions.UserError("This property sale is canceled.")
            
    # @api.model
    # def get_real_estate_info(self):
    #     real_estate = self.browse(2)
    #     return {
    #         'title': real_estate.title,
    #         'description': real_estate.description,
    #     }

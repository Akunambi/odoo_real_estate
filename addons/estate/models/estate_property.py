from odoo import models, fields, api, exceptions
from odoo.tools.float_utils import float_compare, float_is_zero

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real estate property model"
    _sql_constraints = [('check_expected_price', 'CHECK(expected_price>0)', 'A property expected price must be strictly positive'),('check_selling_price', 'CHECK(selling_price>0)', 'A property selling price must be strictly positive')]
    _order = "id desc"

    name = fields.Char(string='Title', required=True, default='New Property')
    description = fields.Text(placeholder="Property description")
    postcode = fields.Char(default="00000")
    date_availability = fields.Date(string="Available From" ,copy=False, default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    living_area = fields.Integer(string='Living Area(sqm)')
    garden_orientation = fields.Selection(
        selection=[('north','North'),('south','South'),('east','East'),('west','West')],
        help="The direction the garden is facing")
    active = fields.Boolean(default=True)
    state = fields.Selection(
        default='new',
        selection= [('new' , 'New'),('offerReceived' , 'Offer Received'), ('offerAccepted' , 'Offer Accepted'),('sold' , 'Sold'),('canceled' , 'Canceled')]
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    seller_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Integer(compute="_compute_total_area")
    best_offer = fields.Float(compute="_compute_best_price")

    @api.depends("living_area","garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped("price")
            record.best_offer = max(prices, default=0)
    @api.onchange("garden")
    def _onchange_garden(self):
        self.garden_area = 10 if self.garden else 0
        self.garden_orientation = "north" if self.garden else ""
        
    
    def update_status_canceled(self):
        for record in self:
            if record.state != "sold":
                record.state = "canceled"
            else:
                return exceptions.UserError("sold properties cannot be canceled")
        return True
    
    def update_status_sold(self):
        for record in self:
            if record.state != "canceled":
                record.state = "sold"
            else:
                raise exceptions.UserError("Canceled properties cannot be sold")
        return True
    
    @api.constrains('selling_price')
    def verify_selling_price(self):
        for record in self:
            comparison = record.expected_price * 0.9
            if float_compare(record.selling_price, comparison, precision_rounding=2) < 0:
                raise exceptions.ValidationError("Selling price is lower than 90 percent of the expected price")
            
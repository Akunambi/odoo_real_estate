from odoo import models,fields,api
from datetime import timedelta,date

class EstatePropertyOffer(models.Model):
    _name="estate.property.offer"
    _description="offers made from buyers for specific properties"
    _sql_constraints = [('check_offer_price', 'CHECK(offer_price>0)', 'A property offer price must be strictly positive')]
    _order="price desc"

    price = fields.Float()
    status = fields.Selection(
        selection=[('accepted','Accepted'),('rejected','Rejected')],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7, string="Validity(days)")
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")


    @api.depends("create_date","validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)
            else:
                record.date_deadline = date.today() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
            for record in self:
                if record.date_deadline and record.create_date:
                    record.validity = (record.date_deadline - record.create_date.date()).days
                elif not record.create_date:
                    record.validity = 0 
                    
    def set_status_accepted(self):
        for record in self:
            record.status = "accepted"
            record.property_id.selling_price= record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = "offerAccepted"
        
        return True
    def set_status_rejected(self):
        for record in self:
            record.status = "rejected"
            record.property_id.buyer_id = ""

        
        return True
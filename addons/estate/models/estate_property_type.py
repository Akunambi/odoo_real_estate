from odoo import models,fields

class EstatePropertyType(models.Model):

    _name = "estate.property.type"
    _description = "Property type i.e House, Apartment etc"
    _sql_constraints = [('unique_name', 'UNIQUE(name)', 'A property type name must be unique')]
    _order = "sequence, name"


    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property', "property_type_id")
    sequence = fields.Integer()
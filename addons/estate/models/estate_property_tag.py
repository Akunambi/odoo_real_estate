from odoo import fields,models

class EstatePropertyTag(models.Model):
    _name="estate.property.tag"
    _description="Tags for properties i.e Cozy, Renovated"
    _sql_constraints = [('unique_name', 'UNIQUE(name)', 'A property tag name must be unique')]
    _order = "name"

    name=fields.Char(required=True)
    color=fields.Integer()
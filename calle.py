# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class SalaCalle(models.Model):
    _name = 'sala.calle'
    _description = 'Gestión Gobierno - calles de Gobierno'
    _rec_name = 'nombre'
    _order = 'nombre'
  
    name = fields.Char(string='Nro.', required=True, copy=False, readonly=True,
                       default=lambda self: _('New'))

    nombre = fields.Char('Calle', required = True)

    direccion_id = fields.Many2one('sala.direccion', string='Dirección', store=True)
    territorio_id = fields.Many2one(string='Territorio', related='direccion_id.territorio_id', tracking=True, store=True)
   
    estado_id = fields.Many2one(string='Estado', related='territorio_id.estado_id', tracking=True, store=True)
    municipio_id = fields.Many2one(string='Municipio', related='territorio_id.municipio_id', tracking=True, store=True)
    parroquia_id = fields.Many2one(string='Parroquia', related='territorio_id.parroquia_id', tracking=True, store=True)
    comuna_id = fields.Many2one(string='Comuna', related='territorio_id.comuna_id', tracking=True, store=True)
    comunidad_id = fields.Many2one(string='Comunidad', related='territorio_id.comunidad_id', tracking=True, store=True)
   
    tipo = fields.Selection([
        ('calle', 'CALLE'),
        ('avenida', 'AVENIDA'),
        ('manzana', 'MANZANA'),
        ('vereda', 'VEREDA'),
        ('callejon', 'CALLEJON'),
        ('otro', 'OTRO'),
        ], required=True, tracking=True) 
   
    direccion = fields.Char('Direcciòn adicional')

    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Favorito'),
    ], required=True, default='0', tracking=True)
    active = fields.Boolean(
        'Active', default=True,
        help="If unchecked, it will allow you to hide the product without removing it.")
    note = fields.Text('Observaciones')

    persona_ids = fields.One2many('sala.persona', 'calle_id', string="Personas")

    persona_count = fields.Integer(string='Nro. personas', compute='_compute_persona_count')

    def _compute_persona_count(self):
        for rec in self:
            persona_count = self.env['sala.persona'].search_count([('calle_id', '=', rec.id)])
            rec.persona_count = persona_count

    habita_count = fields.Integer(string='Nro. Habitantes', compute='_compute_habita_count')
    habita_conta = fields.Integer('Nro. Habitantes', default=0)      
    def _compute_habita_count(self):
        for rec in self:
            habita_count = self.env['sala.persona'].search_count([('calle_id', '=', rec.id)])
            rec.habita_count = habita_count
            rec.habita_conta = habita_count

    @api.onchange('nombre')
    def _onchange_nombre(self):
         if self.comunidad_id:
            self.comuna_id=self.comunidad_id.comuna_id
            return 

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('sala.calle') or _('New')
        res = super(SalaCalle, self).create(vals)
        return res

    @api.onchange('nombre')
    def _onchange_nombre(self):
         
         if self.nombre:
            self.nombre = self.nombre.upper()
         return

    

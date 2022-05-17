# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

from odoo import models, fields, api

class SalaComunidad(models.Model):
    _name = 'sala.comunidad'
    _description = 'Gestión Gobierno - Comunidades'
    _rec_name = 'nombre'
    _order = 'comuna_id , nombre'

    name = fields.Char(string='Nro.', required=True, copy=False, readonly=True,
                       default=lambda self: _('New'))    

    nombre = fields.Char('Comunidad', required = True)

    direccion_id = fields.Many2one('sala.direccion', 'Direcciòn', required=True)
    territorio_id = fields.Many2one(string='Territorio', related='direccion_id.territorio_id', tracking=True, store=True)

    estado_id = fields.Many2one(string='Estado', related='territorio_id.estado_id', tracking=True, store=True)
    municipio_id = fields.Many2one(string='Municipio', related='territorio_id.municipio_id', tracking=True, store=True)
    parroquia_id = fields.Many2one(string='Parroquia', related='territorio_id.parroquia_id', tracking=True, store=True)
    comuna_id = fields.Many2one(string='Comuna', related='territorio_id.comuna_id', tracking=True, store=True)

    image = fields.Image(max_width=100, max_height=100, store=True)
    codigo_situr = fields.Char('Código Situr')
    rif = fields.Char('Rif')
    limite_n = fields.Char('Norte')
    limite_s = fields.Char('Sur')
    limite_e = fields.Char('Este')
    limite_o = fields.Char('Oeste')
    superficie = fields.Integer(string='Superficie')
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Favorito'),
       
    ], required=True, default='0', tracking=True)
    active = fields.Boolean(string="Active", default=True)
    note = fields.Text('Observaciones')

    accion_ids = fields.One2many('acciong.lines', 'comunidad_id', string="Acciones de gobierno")
    calle_ids = fields.One2many('sala.calle', 'comunidad_id', string="Calles")

    @api.onchange('nombre')
    def _onchange_nombre(self):
         
         if self.nombre:
            self.nombre = self.nombre.upper()
         return

    accion_count = fields.Integer(string='Nro. Acciones', compute='_compute_accion_count')
    accion_conta = fields.Integer('Nro. Acciones', default=0)   
    def _compute_accion_count(self):
        for rec in self:
            accion_count = self.env['acciong.lines'].search_count([('comunidad_id', '=', rec.id)])
            rec.accion_count = accion_count
            rec.accion_conta = accion_count          
 
    calle_count = fields.Integer(string='Nro. Calles', compute='_compute_calle_count')
    calle_conta = fields.Integer('Nro. Calles', default=0)
    def _compute_calle_count(self):
        for rec in self:
            calle_count = self.env['sala.calle'].search_count([('comunidad_id', '=', rec.id)])
            rec.calle_count = calle_count
            rec.calle_conta = calle_count

    casa_count = fields.Integer(string='Nro. Viviendas', compute='_compute_casa_count')
    casa_conta = fields.Integer('Nro. Casas', default=0)
    def _compute_casa_count(self):
        for rec in self:
            casa_count = self.env['sala.casa'].search_count([('calle_id.comunidad_id', '=', rec.id)])
            rec.casa_count = casa_count
            rec.casa_conta = casa_count

    familia_count = fields.Integer(string='Nro. Familias', compute='_compute_familia_count')
    familia_conta = fields.Integer('Nro. Familias', default=0)
    def _compute_familia_count(self):
        for rec in self:
            # familia_count = self.env['sala.familia'].search_count([('casa_id.calle_id.comunidad_id.comuna_id', '=', rec.id)])
            familia_count = self.env['sala.persona'].search_count([('comunidad_id', '=', rec.id),('is_jefe', '=', 'true')])

            rec.familia_count = familia_count
            rec.familia_conta = familia_count

    habita_count = fields.Integer(string='Nro. Habitantes', compute='_compute_habita_count')
    habita_conta = fields.Integer('Nro. Habitantes', default=0)      
    def _compute_habita_count(self):
        for rec in self:
            habita_count = self.env['sala.persona'].search_count([('comunidad_id', '=', rec.id)])
            rec.habita_count = habita_count
            rec.habita_conta = habita_count

    vd_count = fields.Integer(string='Nro. Votos Duros', compute='_compute_vd_count')
    vd_conta = fields.Integer('Cantidad Votos Duros', default=0)
    vd_porc = fields.Float(string='% Votos Duros', compute='_compute_vd_porc')

    def _compute_vd_count(self):
        for rec in self:
            vd_count = self.env['familia.persona.lines'].search_count([('familia_id.comunidad_id', '=', rec.id), ('intencion', '=', 'duro')])
            rec.vd_count = vd_count
            rec.vd_conta = vd_count

    def _compute_vd_porc(self):
        for rec in self:
            if self.habita_count > 0:
                vd_porc = (self.vd_count/self.habita_count)*100
            else:
                vd_porc = 0
            rec.vd_porc = vd_porc
             
    vb_count = fields.Integer(string='Nro. Votos Blandos', compute='_compute_vb_count')
    vb_conta = fields.Integer('Cantidad Votos Blandos', default=0)
    vb_porc = fields.Float(string='% Votos Blandos', compute='_compute_vb_porc')

    def _compute_vb_count(self):
        for rec in self:
            vb_count = self.env['familia.persona.lines'].search_count([('familia_id.comuna_id', '=', rec.id), ('intencion', '=', 'blando')])
            rec.vb_count = vb_count
            rec.vb_conta = vb_count
            

    def _compute_vb_porc(self):
        for rec in self:
            if self.habita_count > 0:
                vb_porc = (self.vb_count/self.habita_count)*100
            else:
                vb_porc = 0
            rec.vb_porc = vb_porc  

    vo_count = fields.Integer(string='Nro. Votos Opositor', compute='_compute_vo_count')
    vo_conta = fields.Integer('Cantidad Votos Opositor', default=0)
    vo_porc = fields.Float(string='% Votos Opositor', compute='_compute_vo_porc')

    def _compute_vo_count(self):
        for rec in self:
            vo_count = self.env['familia.persona.lines'].search_count([('familia_id.comuna_id', '=', rec.id), ('intencion', '=', 'opositor')])
            rec.vo_count = vo_count
            rec.vo_conta = vo_count

    def _compute_vo_porc(self):
        for rec in self:
            if self.habita_count > 0:
                vo_porc = (self.vo_count/self.habita_count)*100
            else:
                vo_porc = 0
            rec.vo_porc = vo_porc

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('sala.comunidad') or _('New')
        res = super(SalaComunidad, self).create(vals)
        return res

    @api.onchange('nombre')
    def _onchange_nombre(self):
         
        if self.nombre:
            self.nombre = self.nombre.upper()
        
        domain = [('nombre', '=', self.nombre)]
        if self.id.origin:
            domain.append(('id', '!=', self.id.origin))
        
        if self.env['sala.comunidad'].search(domain, limit=1):
            return {'warning': {
                'title': ("Precauciòn:"), 
                'message': ("El nombre para la Comunidad ya existe ", self.nombre), 
            }}
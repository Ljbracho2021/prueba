# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SalaTipoReportWizard(models.TransientModel):
    _name = 'sala.tipo.report.wizard'

    date_start = fields.Date(string='Fecha inicio', required=True, default=fields.Date.today)
    date_end = fields.Date(string='Fecha fin', required=True, default=fields.Date.today)
    tipo_id = fields.Many2one('sala.tipoa', 'Tipo acciòn', required=True)

    @api.onchange('date_start')
    def _onchange_date_start(self):
        if self.date_start and self.date_end and self.date_end < self.date_start:
            self.date_end = self.date_start

    @api.onchange('date_end')
    def _onchange_date_end(self):
        if self.date_end and self.date_end < self.date_start:
            self.date_start = self.date_end

    def get_report(self):
        data = {
            'model': self._name,
            'ids': self.ids,
            'form': {
                'date_start': self.date_start, 'date_end': self.date_end, 'tipo_id': self.tipo_id.nombre,
            },
        }

        # ref `module_name.report_id` as reference.
        return self.env.ref('it_sala.sala_tipo_report').report_action(self, data=data)
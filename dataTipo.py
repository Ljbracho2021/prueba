# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class ReportSalaTipoReportView(models.AbstractModel):
    """
        Abstract Model specially for report template.
        _name = Use prefix `report.` along with `module_name.report_name`
    """
    _name = 'report.it_sala.sala_tipo_report_view'

    @api.model
    def _get_report_values(self, docids, data=None):
        date_start = data['form']['date_start']
        date_end = data['form']['date_end']
        tipo_a = data['form']['tipo_id']

        SO = self.env['acciong.lines']
        start_date = datetime.strptime(date_start, DATE_FORMAT)
        end_date = datetime.strptime(date_end, DATE_FORMAT)
        a_tipo = tipo_a
        delta = timedelta(days=1)

        docs = []

        date = start_date
        print(date, start_date)

        if a_tipo == 'TODOS':
            acciones = SO.search([
                    ('acciong_id.date_apertura', '>=', start_date.strftime(DATETIME_FORMAT)),
                    ('acciong_id.date_cierre', '<', end_date.strftime(DATETIME_FORMAT)),
                    ('acciong_id.state', 'in', ['ejecutada', 'en proceso'])
                ])
        else:
            acciones = SO.search([
                    ('acciong_id.date_apertura', '>=', start_date.strftime(DATETIME_FORMAT)),
                    ('acciong_id.date_cierre', '<', end_date.strftime(DATETIME_FORMAT)),
                    ('acciong_id.state', 'in', ['ejecutada', 'en proceso']),
                    ('accion_id', '=', a_tipo)
                ])
      
        for accion in acciones: 
            fecha_apertura = accion.date_apertura
            nombre_accion  = accion.nombre
            monto_accion   = accion.acciong_id.monto
            unidad_id      = accion.unidad_id.nombre
            accion_id      = accion.accion_id.nombre

            docs.append({
                 'fecha_apertura': fecha_apertura.strftime("%d-%m-%y"),
                 'nombre_accion': nombre_accion,
                 'monto_accion': monto_accion,
                 'unidad_id': unidad_id, 
                 'accion_id': accion_id,                 
                 'company': self.env.user.company_id
            })

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'date_start': date_start,
            'date_end': date_end,
            'docs': docs,
        }
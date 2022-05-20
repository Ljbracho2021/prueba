# -*- coding: utf-8 -*-
{
    'name': "Sala",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,
    'sequence': -100,
    'author': "Alcaldia de Paez",
    'website': "http://www.alcaldiapaez.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'license': 'AGPL-3',
    'category': 'Application',
    'version': '1.0',
    'installable': True,
    'application': True,
    'auto_install': False,
    # any module necessary for this one to work correctly
    #'depends': ['base'],
    'depends': [
    
        'mail',
    
    ],

    # always loaded
    'data': [  
        'security/ir.model.access.csv',
        'security/sala_access_rules.xml', 
        'data/data.xml',
 
        'report/persona_details.xml',  
        'report/comuna_details_template.xml',
        'report/comuna_list_template.xml',
        'report/comunidad_details_template.xml',
        'report/comunidad_list_template.xml',
        'report/unidad_details_template.xml',
        'report/ubch_details_template.xml',
        'report/ubch_list_template.xml',  
        'report/activo_details_template.xml',   
        'report/activo_list_template.xml',    
        'report/memoria_template.xml', 
        'report/memoria_tipo_template.xml', 

        'report/report.xml',  

        'views/views.xml',
        'views/estado_view.xml',
        'views/municipio_view.xml',
        'views/comuna_view.xml',
        'views/comunidad_view.xml',

        'views/ubicacion_view.xml',
        'views/territorio_view.xml',
        'views/persona_view.xml',
        'views/activo_view.xml',
        'views/sector_view.xml',
        'views/direccion_view.xml',
        'views/organizacion_view.xml',
        'views/rol_view.xml',
        'views/clap_view.xml',
        'views/ubch_view.xml',
        'views/unidad_view.xml',
        'views/categoria_view.xml',
        'views/centro_view.xml',
        'views/tipoa_view.xml',
        'views/tipov_view.xml',
        'views/acciong_view.xml',
        'views/parentesco_view.xml',
        'views/calle_view.xml',
        'views/parroquia_view.xml',
        'views/agparroquia_view.xml',
        'views/rwaccion_view.xml',
        'views/rwtipo_view.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [],
    'qweb': [],
}

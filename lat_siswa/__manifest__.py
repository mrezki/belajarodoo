# -*- coding: utf-8 -*-
{
    "name": "Latihan Generate Student Module",
    "version": "1.0",
    "author": "Falinwa Indonesia",
    "description": """
        Module to Generate Data Student.
    """,
    "depends": ["base"],
    "init_xml": [],
    "data": [
        'views/register.xml',
        'views/receipt.xml',
        'views/student.xml',
        'views/sequence.xml',
        'security/ir.model.access.csv',
        'report/receipt_rpt.xml',
    ],
    "active": False,
    "application": False,
    "installable": True,
}

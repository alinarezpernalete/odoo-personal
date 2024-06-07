{
    'name': 'Real Estate',
    'depends': [
        'base',
        'auth_totp'
    ],
    'application': True,
    'author': 'ALinarezPernalete',
    'data': [
        'security/ir.model.access.csv',
        'views/real_estate_property_offer.xml',
        'views/res_users.xml',
        'views/real_estate.xml',
        'views/real_estate_property_type.xml',
        'views/real_estate_property_tag.xml',
        'views/real_estate_menu.xml',
    ],
    'license': 'LGPL-3',
}
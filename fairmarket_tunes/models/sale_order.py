from openerp.osv import osv, fields

class sale_order(osv.Model):
    _inherit = 'sale.order'
    _columns = {
        'fcaddress':fields.char('Faircoin Address'),
        'qrcode':fields.binary("QR Code"),
    }
    
    

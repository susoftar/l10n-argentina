# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2008-2011
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from osv import osv, fields

class sale_shop(osv.osv):
    _name = "sale.shop"
    _inherit = "sale.shop"
    _columns = {
        'pos_ar_ids' : fields.one2many('pos.ar','shop_id','Points of Sales'),
    }
sale_shop()

class sale_order(osv.osv):
    _name = "sale.order"
    _inherit = "sale.order"

    #overwrite    
    def _make_invoice(self, cr, uid, order, lines, context=None):
        
        invoice_id = super(sale_order, self)._make_invoice(cr, uid, order, lines, context)
    
        # Para la denomination, se deberia? preguntar si esta seteada la fiscal position y sino lazar una exept??                         
        denom_id = order.fiscal_position.denomination_id
               
        pos_ar_obj = self.pool.get('pos.ar')
        
        if not order.fiscal_position :
            raise osv.except_osv( ('Error'),
                                  ('Check the Fiscal Position Configuration')) 
        
        res_pos = pos_ar_obj.search(cr, uid,[('shop_id', '=', order.shop_id.id), ('denomination_id', '=', denom_id.id)])
        if not len(res_pos):
            raise osv.except_osv( ('Error'),
                                  ('You need to set up a Shop and/or a Fiscal Position')) 
                                  
        inv_obj = self.pool.get('account.invoice')
        vals = {'denomination_id' : denom_id.id , 'pos_ar_id': res_pos[0] }
        #escribo en esa invoice y retorno su id como debe ser
        inv_obj.write(cr, uid, invoice_id, vals)
                
        return invoice_id
    
sale_order()

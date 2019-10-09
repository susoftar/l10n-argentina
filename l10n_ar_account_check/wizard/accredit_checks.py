# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2017 Aconcagua Team (http://www.proyectoaconcagua.com.ar)
#    All Rights Reserved. See AUTHORS for details.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, api, fields


class WizardAccreditChecks(models.TransientModel):
    _name = 'wizard.accredit.checks'
    _description = 'Select several checks which are Waiting Accreditation so you can accredit them'

    def get_default_checks(self):
        check_ids = self.env.context.get("active_ids", [])
        return [(6, False, check_ids)]

    def get_default_domain(self):
        ids = self.get_default_checks()[0][2]
        return [('id', 'in', ids)]

    issued_checks = fields.Many2many(
        'account.issued.check',
        'wiz_accredit_check_rel',
        'wiz_id',
        'check_id',
        default=get_default_checks,
        domain=get_default_domain,
    )
    date = fields.Date(required=True, default=fields.Date.context_today, string='Accreditation Date')

    @api.multi
    def button_accredit_checks(self):
        self = self.with_context(date_to_use=self.date)
        return self.issued_checks.accredit_checks()

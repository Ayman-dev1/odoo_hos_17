from odoo import models, fields, api


class Patient(models.Model):
    _name = 'patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hospital Patient'

    name = fields.Char(string='Name', required=True)
    age = fields.Integer(string='Age', required=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender')
    note = fields.Text(string='Notes')
    examination_date = fields.Date(string='Examination Date', compute='_compute_examination_date', store=True)
    department_id = fields.Many2one('department', string='Department')
    doctor_id = fields.Many2one('doctor', string='Doctor')
    state = fields.Selection(
        [('after', 'After'), ('examination', 'Examination'), ('done', 'Done')],
        default='after', string='State', tracking=True
    )

    @api.depends('state')
    def _compute_examination_date(self):
        for record in self:
            if record.state == 'examination':
                record.examination_date = fields.Date.today()

    @api.onchange('department_id')
    def _onchange_department_id(self):
        if self.department_id:
            return {'domain': {'doctor_id': [('department_id', '=', self.department_id.id)]}}
        else:
            self.doctor_id = False
            return {'domain': {'doctor_id': [('id', '=', False)]}}

    def action_after(self):
        for rec in self:
            rec.state = 'after'

    def action_patient_examination(self):
        action = self.env.ref('odoo_hos_17.action_patient_examination').read()[0]
        return action

    def action_examination(self):
        for rec in self:
            rec.state = 'examination'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

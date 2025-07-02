from dateutil.utils import today
from odoo import api,fields,models

class LetterLetter(models.Model):
    _name = 'letter.letter'
    _description = 'Letters Model'

    _inherit = 'letter.base'

    letter_name=fields.Char(string="Letter Name", readonly=True, copy=False, compute='compute_letter_code',store=True)
    letter_date=fields.Date(string="Letter Date", default=today())
    template_id=fields.Many2one('letter.template',string="Template",required=True)
    linked_content=fields.Html(readonly=True, related='template_id.template_content')

    _sql_constraints = [('unique_letter_code','UNIQUE(letter_name)','Letter Name should be unique! (Hint: It already exists)')]

    def print_letter(self):
        return self.env.ref('letter_writer.letter_html_report').report_action(self)

    def save_letter_docx(self):
        return {
            'type' : 'ir.actions.act_url',      #Type: URL (To send the request to the HTTP Controller we created in the controllers
            'url' : f'/letter/{self.id}/download_docx',     #URL endpoint. Will be heard by the controller
            'target' : 'self'       #self = Same Window
        }

    #This method is the actual backend implementation for letter_name. _change_letter_code changes the letter name in the UI
    #at real time, but this changes it in the record itself
    @api.depends('template_id','letter_date')
    def compute_letter_code(self):
        for record in self:
            if record.template_id and record.letter_date:   #TO-DO: Add validation for record.template_id.next_number
                record.letter_name = record.template_id.template_code + '/' + str(record.letter_date.year) + '/' + str(record.template_id.next_number)
                record.template_id.next_number += 1
            else:
                record.letter_name = None

    #This method helps with the visualization for the user in real-time while changing templates. It doesn't affect the database or
    #backend.
    @api.onchange('template_id','letter_date')
    def _change_letter_code(self):
        for record in self:
            if record.template_id and record.letter_date:
                record.letter_name = (record.template_id.template_code + '/' + str(record.letter_date.year)
                                  + '/' + str(record.template_id.next_number))

from dateutil.utils import today

from odoo import api,fields,models

class LetterLetter(models.Model):
    _name = 'letter.letter'
    _description = 'Letters Model'

    letter_name=fields.Char(string="Letter Name", required=True, copy=False)
    letter_date=fields.Date(string="Letter Date", default=today())
    template_id=fields.Many2one('letter.template',string="Template",required=True)
    linked_content=fields.Html(readonly=True, string="Letter Preview", related='template_id.template_content')
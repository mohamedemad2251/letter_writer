from dateutil.utils import today

from odoo import api,fields,models

class LetterLetter(models.Model):
    _name = 'letter.letter'
    _description = 'Letters Model'
    # from ../letter_base import LetterBase  # for IDE only

    _inherit = 'letter.base'

    letter_name=fields.Char(string="Letter Name", required=True, copy=False)
    letter_date=fields.Date(string="Letter Date", default=today())
    template_id=fields.Many2one('letter.template',string="Template",required=True)
    linked_content=fields.Html(readonly=True, related='template_id.template_content')
    # company_id=fields.Many2one('res.company',string="Company")



    # @api.onchange('template_id','company_id','letter_date','use')
    # def replace_html_content(self):
    #     return super().replace_html_content(self)
        # for record in self:
        #     record.replaced_content = record.linked_content
        #     record.replaced_content = record.replaced_content.replace("*company_name*", str(record.company_id.name))
        #     record.replaced_content = record.replaced_content.replace("*date*", str(record.letter_date))

from odoo import api, fields, models

class LetterTemplate(models.Model):
    _name = 'letter.template'
    _description = "Letter Templates Model"

    template_name = fields.Char(string="Template Name")
    template_date = fields.Date(string="Template Date")
    template_content = fields.Html(string="Template Content - HTML")
    template_placeholders = fields.Selection(string="Template Placeholders", selection=[('*selection_one*','Selection One'),('*selection_two*','Selection Two')])

    @api.onchange('template_placeholders')
    def _embed_template_placeholder(self):
        for record in self:
            record.template_content+=record.template_placeholders
            record.template_placeholders=None
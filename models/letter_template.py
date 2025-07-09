import markupsafe
from dateutil.utils import today

from odoo import api, fields, models
from odoo.exceptions import UserError


class LetterTemplate(models.Model):
    _name = 'letter.template'
    _description = "Letter Templates Model"
    _rec_name = 'template_name'  #Your template name isn't called "name" so Odoo's ORM by default can't grab records/show their names. We need to represent records with a variable assigned.

    template_name = fields.Char(string="Template Name", required=True)
    template_date = fields.Date(string="Template Date", default=today())
    template_content = fields.Html(string="Template Content", sanitize=False, sanitize_tags=False,
                                   sanitize_attributes=False, required=True)
    template_module = fields.Selection(string="Template Module", required=True,
                                       selection=lambda self: self._get_dynamic_modules_selection(), readonly=False)

    template_placeholders_id = fields.Many2one('letter.placeholders',string="Template Placeholders")

    template_code = fields.Char(string="Template Code", required=True)
    next_number = fields.Integer(string="Next Allowed Number")


    #Adds a layer of validation using the query UNIQUE. This checks if the table already has that template_code field value or not. If it does, it throws a validation error.
    _sql_constraints = [('unique_template_code', 'UNIQUE(template_code)',
                         "Template\'s code must be unique! (Hint: This code already exists)")]

    @api.model
    def _module_is_installed(self, module_name):    #Extra method to check ir.module.module records if a module (given by module_name) is installed or not.
        return self.env['ir.module.module'].sudo().search_count([
            ('name', '=', module_name),
            ('state', '=', 'installed')]
        ) > 0

    def _get_dynamic_modules_selection(self):       #Dynamic dropdown depending on the modules installed (extensions of Letter Writer)
        selection = [
            ('base', 'No Module'),
        ]
        if self._module_is_installed('letter_hr'):
            selection.append(('hr','HR'))
        return selection

    @api.onchange('template_placeholders_id')
    def _embed_template_placeholder(self):
        string_added = ""
        for record in self:
            if record.template_placeholders_id:  #Protects UI from having undefined behavior since a selection is by default None
                if not record.template_content:  #If no content has been added yet (new template/deleted content)
                    record.template_content = markupsafe.Markup(
                        '')  #Transform the template_content from 'bool' to 'Markup'
                record.template_content = markupsafe.Markup(record.template_content)
                string_added = markupsafe.Markup('<span>') + markupsafe.Markup(
                    record.template_placeholders_id.code) + markupsafe.Markup('</span>')
                record.template_content = record.template_content + string_added  #Concatenate the placeholder
                record.template_placeholders_id = None  #Reset the dropdown to None (nothing shows up, like the selection took effect & vanished)

    @api.onchange('template_code')
    def _capitalize_template_code(self):
        for record in self:
            if record.template_code:

                if not record.template_code.isalpha():
                    record.template_code = None
                    raise UserError("The template's code must be letters only (Max: 3 letters)")

                if len(record.template_code) > 3:
                    raise UserError("The template's code must be less than or equals 3 letters!")

                record.template_code = record.template_code.upper()
            else:
                return

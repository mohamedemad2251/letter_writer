import markupsafe
from dateutil.utils import today

from odoo import api, fields, models
from odoo.addons.test_convert.tests.test_env import record
from odoo.exceptions import UserError


class LetterTemplate(models.Model):
    _name = 'letter.template'
    _description = "Letter Templates Model"
    _rec_name = 'template_name'  #Your template name isn't called "name" so Odoo's ORM by default can't grab records/show their names. We need to represent records with a variable assigned.

    template_name = fields.Char(string="Template Name", required=True)
    template_date = fields.Date(string="Template Date", default=today(),help="Template's creation date. This field has no effect for the letters but can be used for "
                                                                             "filtering.")
    template_content = fields.Html(string="Template Content", sanitize=False, sanitize_tags=False,
                                   sanitize_attributes=False, required=True)
    template_module = fields.Selection(string="Template Module", required=True,
                                       selection=lambda self: self._get_dynamic_modules_selection(), readonly=False,
                                       help="Choosing a module affects both the template's placeholder dropdown menu (extends it) and letter's shown fields to populate "
                                            "such placeholders.")

    template_placeholders_id = fields.Many2one('letter.placeholders',string="Template Placeholders")

    template_code = fields.Char(string="Template Code", required=True, help="Code that will be used in the letters as part of the letter's name. Letter's Name: "
                                                                            "Template Code/Letter's Year (in Date)/Next Allowed Number.")
    next_number = fields.Integer(string="Next Allowed Number", readonly=False, help="A number/code that is a part of the letter's name code. Letter's Name: "
                                                                                    "Template Code/Letter's Year (in Date)/Next Allowed Number. "
                                                                                    "Use this field responsibly if you're populating it manually. Failing "
                                                                                    "to do so can cause a letter to throw an error for already existing.")
    # next_number = fields.Integer(string="Next Allowed Number", readonly=False, compute='_validate_next_number')

    letter_ids = fields.One2many('letter.letter','template_id',string="Letters")


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

    def compute_next_allowed_number(self):
        year = int(fields.Date.today().year)     #Get the current year using today & year
        for record in self:
            used_next_numbers = set()       #Create an empty set for all used next_number values IN THIS YEAR
            for letter in record.letter_ids:
                if letter.letter_date:
                    if int(letter.letter_name.split('/')[-2]) == year:
                        used_next_numbers.add(int(letter.letter_name.split('/')[-1]))
            for next_number in range(10000):
                if next_number not in used_next_numbers:
                    record.next_number = next_number
                    return
            raise UserError('This template already has 9999 letters (full). Please create a new template or enter the next number manually. (for older years)')

    # @api.depends('next_number')
    # def _validate_next_number(self):
    #     for record in self:
    #         if record.next_number > 9999:
    #             raise UserError('The Next Allowed Number cannot be more than 9999!')
            # for letter in record.letter_ids:
            #     letter_next_number = int(letter.letter_name.replace((letter.template_id.template_code + '/' + str(letter.letter_date.year) + '/'),''))
            #     while letter_next_number == record.next_number:
            #         count=0
            #
            #         raise UserError('')

            # raise UserError(str(record.letter_ids))
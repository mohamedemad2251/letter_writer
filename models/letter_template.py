import markupsafe
from dateutil.utils import today

from odoo import api, fields, models


class LetterTemplate(models.Model):
    _name = 'letter.template'
    _description = "Letter Templates Model"
    _rec_name = 'template_name' #Your template name isn't called "name" so Odoo's ORM by default can't grab records/show their names. We need to represent records with a variable assigned.

    template_name = fields.Char(string="Template Name", required=True)
    template_date = fields.Date(string="Template Date", default=today())
    template_content = fields.Html(string="Template Content", sanitize=False, sanitize_tags=False, sanitize_attributes=False, required=True)
    template_placeholders = fields.Selection(
        string="Template Placeholders",
        selection=lambda self: self._get_dynamic_placeholders_selection(),
        help="Select a placeholder that will be changed dynamically in your letter. Placeholders have special syntax to be detected"
              "later. Please don't change the syntax as it won't be replaced later on."
     )

    def _get_dynamic_placeholders_selection(self):
        # Create a fake letter record to access get_letter_placeholders
        letter_model = self.env['letter.letter']
        letter_sample = letter_model.new({})  # empty in-memory record

        placeholder_dict = letter_sample.get_letter_placeholders()
        return [(key, key.replace("*", "").replace("_", " ").title()) for key in placeholder_dict.keys()]

    @api.onchange('template_placeholders')
    def _embed_template_placeholder(self):
        string_added = ""
        for record in self:
            if record.template_placeholders:   #Protects UI from having undefined behavior since a selection is by default None
                if not record.template_content:        #If no content has been added yet (new template/deleted content)
                    record.template_content = markupsafe.Markup('') #Transform the template_content from 'bool' to 'Markup'
                record.template_content = markupsafe.Markup(record.template_content)
                string_added = markupsafe.Markup('<span>') + markupsafe.Markup(record.template_placeholders) + markupsafe.Markup('</span>')
                record.template_content = record.template_content + string_added  #Concatenate the placeholder
                record.template_placeholders=None           #Reset the dropdown to None (nothing shows up, like the selection took effect & vanished)


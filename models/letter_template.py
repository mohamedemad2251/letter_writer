import markupsafe
from dateutil.utils import today

from odoo import api, fields, models

class LetterTemplate(models.Model):
    _name = 'letter.template'
    _description = "Letter Templates Model"

    template_name = fields.Char(string="Template Name", required=True)
    template_date = fields.Date(string="Template Date", default=today())
    template_content = fields.Html(string="Template Content", sanitize=False, sanitize_tags=False, sanitize_attributes=False, required=True)
    template_placeholders = fields.Selection(
        string="Template Placeholders",
        selection=[('*selection_one*','Selection One'),('*selection_two*','Selection Two')],
        help="Select a placeholder that will be changed dynamically in your letter. Placeholders have special syntax to be detected"
              "later. Please don't change the syntax as it won't be replaced later on."
     )

    # @api.onchange('template_placeholders')
    # def _embed_template_placeholder(self):
    #     for record in self:
    #         if record.template_placeholders is not False:   #Protects UI from having undefined behavior since a selection is by default None
    #             if record.template_content is False:        #If no content has been added yet (new template/deleted content)
    #                 record.template_content = markupsafe.Markup('') #Transform the template_content from 'bool' to 'Markup'
    #             record.template_content = markupsafe.Markup(record.template_content) + markupsafe.Markup(record.template_placeholders)  #Concatenate the placeholder
    #             # record.template_content = markupsafe.escape(record.template_content)
    #             # record.template_content = markupsafe.Markup(record.template_content)
    #             record.template_placeholders=None           #Reset the dropdown to None (nothing shows up, like the selection took effect & vanished)
    #             # record.template_content = markupsafe.Markup('<div>Hello</div><div>World</div>')
    #             # record.template_content = markupsafe.Markup(
    #             #     "<div><h2 style='text-align: center;'>Certificate of Completion</h2>"
    #             #     "<p>This certifies that <b>John Doe</b> has completed the course.</p>"
    #             #     "<p>Date: <i>June 10, 2025</i></p></div>"
    #             # )
    #

    @api.onchange('template_placeholders')
    def _embed_template_placeholder(self):
        string_added = ""
        for record in self:
            if record.template_placeholders is not False:   #Protects UI from having undefined behavior since a selection is by default None
                if record.template_content is False:        #If no content has been added yet (new template/deleted content)
                    record.template_content = markupsafe.Markup('') #Transform the template_content from 'bool' to 'Markup'
                record.template_content = markupsafe.Markup(record.template_content)
                string_added = markupsafe.Markup('<span>') + markupsafe.Markup(record.template_placeholders) + markupsafe.Markup('</span>')
                record.template_content = record.template_content + string_added  #Concatenate the placeholder
                # record.template_content = markupsafe.escape(record.template_content)
                # record.template_content = markupsafe.Markup(record.template_content)
                record.template_placeholders=None           #Reset the dropdown to None (nothing shows up, like the selection took effect & vanished)
                # record.template_content = markupsafe.Markup('<div>Hello</div><div>World</div>')
                # record.template_content = markupsafe.Markup(
                #     "<div><h2 style='text-align: center;'>Certificate of Completion</h2>"
                #     "<p>This certifies that <b>John Doe</b> has completed the course.</p>"
                #     "<p>Date: <i>June 10, 2025</i></p></div>"
                # )


    # @api.onchange('template_content')
    # def _update_html(self):
    #     for record in self:
    #         markupsafe.escape(record.template_content)
    #         record.template_content = markupsafe.Markup(record.template_content)

    # def _embed_template_placeholder(self):
    #     for record in self:
    #         if record.template_placeholders:
    #             # Ensure the content is a Markup string
    #             if not record.template_content:
    #                 record.template_content = markupsafe.Markup('')
    #             elif not isinstance(record.template_content, markupsafe.Markup):
    #                 record.template_content = markupsafe.Markup(record.template_content)
    #
    #             # Safely escape the placeholder and wrap in div
    #             placeholder_html = markupsafe.Markup(f"<div>{markupsafe.escape(record.template_placeholders)}</div>")
    #
    #             # Append to existing content
    #             record.template_content += placeholder_html
    #
    #             # Clear the dropdown (visual reset)
    #             record.template_placeholders = None


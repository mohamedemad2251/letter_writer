# -*- coding: utf-8 -*-
# from odoo import http


# class LetterWriter(http.Controller):
#     @http.route('/letter_writer/letter_writer', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/letter_writer/letter_writer/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('letter_writer.listing', {
#             'root': '/letter_writer/letter_writer',
#             'objects': http.request.env['letter_writer.letter_writer'].search([]),
#         })

#     @http.route('/letter_writer/letter_writer/objects/<model("letter_writer.letter_writer"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('letter_writer.object', {
#             'object': obj
#         })


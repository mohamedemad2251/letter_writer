# -*- coding: utf-8 -*-
from odoo import http   #Include the http model (to use controllers)
from odoo.http import request,content_disposition   #Include the request library (NOTE: Request here serves as the self since the user clicks and makes a request in a record (the request is the record)
# from io import BytesIO  #Include io stream to have the bytes of the document in the RAM (we won't save the document on the server but on the RAM temporarily to save the document later on
                        #the client side
from html2docx import html2docx     #UPDATE: This line already imports Document (in docx) and ByteIO (in io). No need to import them again, commented the imports.
# from docx import Document   #Include the library we're going to use for the Word Document: Document inside python-docx


class LetterDownloadController(http.Controller):
    @http.route(route='/letter/<int:letter_id>/download_docx', type='http', auth='user')
    def _download_letter_document(self, letter_id):     #The method linked to the HTTP decorator. This holds the document creation & download logic
        letter = request.env['letter.letter'].browse(letter_id)     #Make a variable (type: any) that holds the letter data. If it failed to fetch the request's record from the model
                                                                    #letter.letter, then it'll be none. But if it finds it, it returns the record (fetches using letter_id & browse() )
        if not letter.exists():     #If not found
            return request.not_found()  #Return a 404
        # document = Document()       #Initialize a new document to hold the content
        # buffer = BytesIO()          #Initialize the buffer

        # document.add_paragraph(letter.replaced_content)
        # document.save(buffer)       #Saves the document to the buffer. Note, you can't go the other way around (i.e. buffer.write(document) because buffer accepts only bytes,
                                    # not 'Document' object. I think document.save(buffer) implicitly converts the object's content to bytes.

        buffer = html2docx(str(letter.replaced_content),'letter')
        buffer.seek(0)              #Go to the start of the buffer (so that we read the document from the very start, VERY IMPORTANT!
        filename = (letter.letter_name or 'letter').replace(' ','_') + '.docx'  #If letter is Letter 1, the filename will be Letter_1.docx
        return request.make_response(
            data=buffer.read(),
            headers=[
                ('Content-Type', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'),    #MIME type for Microsoft Word (.docx) (Standard)
                ('Content-Disposition', content_disposition(filename)),     #Load attachement, downloadable, with: filename (letter_name.docx)
            ]
        )
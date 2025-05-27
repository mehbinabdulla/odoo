# -*- coding: utf-8 -*-
import json
from odoo import http
from odoo.http import content_disposition, request
from odoo.tools import html_escape
class XLSXReportController(http.Controller):
   @http.route('/xlsx_reports', type='http', auth='user', methods=['POST'], csrf=False)
   def get_report_xlsx(self, model, options, output_format, report_name, **kw):
       uid = request.session.uid
       report_obj = request.env[model].with_user(uid)
       options = json.loads(options)
       token = 'dummy-because-api-expects-one'
       try:
           if output_format == 'xlsx':
               response = request.make_response(
                   None,
                   headers=[
                       ('Content-Type', 'application/vnd.ms-excel'),
                       ('Content-Disposition',
                        content_disposition(report_name + '.xlsx'))
                   ]
               )
               report_obj.get_xlsx_report(options, response)
               response.set_cookie('fileToken', token)
               return response
           return None
       except Exception as e:
           se = http.serialize_exception(e)
           error = {
               'code': 200,
               'message': 'Odoo Server Error',
               'data': se
           }
           return request.make_response(html_escape(json.dumps(error)))


class StudentRegistrationController(http.Controller):
   @http.route('/registration', auth='user', website=True)
   def student_registration(self):
       return request.render('school_management.student_registration_template')

   @http.route(['/register_student/'], type='http', auth="user", website=True,  methods=['POST'])
   def register_student(self, **post):
       first_name = post.get('first_name')
       last_name = post.get('last_name')
       email = post.get('email')
       mobile = post.get('mobile')
       dob = post.get('dob')
       age = post.get('age')
       aadhaar =  post.get('aadhaar')
       gender =  post.get('gender')
       try:
           student = request.env['student'].sudo().create({
               'first_name': first_name,
               'last_name': last_name,
               'email': email,
               'mobile': mobile,
               'dob': dob,
               'aadhaar_number': aadhaar,
               'gender': gender,
               'class_id':'',
               'dept_id':'',
               'stage':'registered',

           })
           print(student.id)
           return request.redirect('/register_student')
       except Exception as e:
           print(e)
           return request.render('school_management.student_registration_template',
                                  {'submitted': post.get('submitted', False)})
# -*- coding: utf-8 -*-
import json
import psycopg2
from odoo import http
from odoo.http import content_disposition, request
from odoo.tools import html_escape


class XLSXReportController(http.Controller):
    @http.route('/xlsx_reports', type='http', auth='user', methods=['POST'], csrf=False)
    def get_report_xlsx(self, model, options, output_format, report_name):
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
    @http.route(['/students'], type='http', auth='public', website=True)
    def students(self):
        students = request.env['student'].sudo().search([])
        return request.render('school_management.students_list_template', {
            'students': students
        })

    @http.route(['/student/<int:student_id>'], type='http', auth='public', website=True)
    def student_view(self, student_id):
        student = request.env['student'].sudo().browse(student_id)
        return request.render('school_management.student_view_form_template', {
            'student': student
        })

    @http.route('/registration', auth='user', website=True)
    def student_registration(self):
        return request.render('school_management.student_registration_form_template', {
            'error': False,
            'success': False,
            'values': {}
        })

    @http.route(['/register_student/'], type='http', auth="user", csrf=True, website=True, methods=['POST'])
    def register_student(self, **values):
        first_name = values.get('first_name')
        last_name = values.get('last_name')
        email = values.get('email')
        mobile = values.get('mobile')
        dob = values.get('dob')
        aadhaar = values.get('aadhaar')
        gender = values.get('gender')
        department_id = values.get('department_id')
        class_id = values.get('class_id')

        try:
            request.env['student'].sudo().create({
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'mobile': mobile,
                'dob': dob,
                'aadhaar_number': aadhaar,
                'gender': gender,
                'class_id': class_id,
                'dept_id': department_id,
                'stage': 'registered',
            })

            request.session['success_message'] = f'Registration of {first_name} {last_name} is completed'
            request.session['success_href'] = '/registration'
            return request.redirect('/success')
        except psycopg2.errors.UniqueViolation as e:
            print(str(e))
            request.env.cr.rollback()
            return request.render('school_management.student_registration_form_template', {
                'error': f'Email ({email}) already exists',
                'success': False,
                'values': values
            })
        except Exception as e:
            print(str(e))
            request.env.cr.rollback()
            return request.render('school_management.student_registration_form_template', {
                'error': str(e),
                'success': False,
                'values': values
            })

    @http.route(['/success'], type='http', auth='public', website=True)
    def success(self):
        message = request.session.pop('success_message', '')
        href = request.session.pop('success_href', '#')
        return request.render('school_management.form_success_template', {
            'message': message,
            'href': href
        })

class StudentLeaveController(http.Controller):
    @http.route(['/leaves'],  type='http', auth='public', website=True)
    def leaves(self):
        leaves = request.env['student.leave'].sudo().search([])
        return request.render('school_management.student_leaves_list_template',{'leaves': leaves})

    @http.route(['/leaves/create'], type='http', auth='public', website=True)
    def create_leave(self):
        return request.render('school_management.student_leave_create_form_template', {
            'error': False,
            'success': False,
            'values': {}
        })

    @http.route(['/api/student/<int:student_id>'], type='json', auth='public', website=True)
    def api_student_data(self, student_id):
        student = request.env['student'].sudo().browse(student_id)
        res = {
            'id': student.id,
            'name': student.name,
            'class_id': student.class_id.id,
            'class_name': student.class_id.name
        }
        return res

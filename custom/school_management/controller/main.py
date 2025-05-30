# -*- coding: utf-8 -*-
import json
import psycopg2
from odoo import http
from odoo.http import content_disposition, request
from odoo.tools import html_escape


class XLSXReportController(http.Controller):
    @http.route('/xlsx_reports', type='http', auth='user', methods=['POST'], csrf=False)
    def get_report_xlsx(self, model, options, output_format, report_name, **kwargs):
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

    @http.route('/students/registration', auth='user', website=True)
    def student_registration(self):
        return request.render('school_management.student_registration_form_template', {
            'error': False,
            'success': False,
            'values': {}
        })

    @http.route(['/student/<int:student_id>'], type='http', auth='public', website=True)
    def student_view(self, student_id):
        student = request.env['student'].sudo().browse(student_id)
        return request.render('school_management.student_view_form_template', {
            'student': student
        })

    @http.route(['/students/register-student'], type='http', auth="user", csrf=True, website=True, methods=['POST'])
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

    @http.route(['/api/student/<int:student_id>'], type='json', auth='public', website=True)
    def api_student_data(self, student_id):
        student = request.env['student'].sudo().browse(student_id)
        res = {
            'id': student.id,
            'name': student.name,
            'class_id': {
                'id': student.class_id.id,
                'name': student.class_id.name
            },
        }
        return res


class StudentLeaveController(http.Controller):
    @http.route(['/leaves'],  type='http', auth='public', website=True)
    def leaves(self):
        leaves = request.env['student.leave'].sudo().search([])
        return request.render('school_management.student_leaves_list_template',{'leaves': leaves})

    @http.route(['/leaves/new'], type='http', auth='public', website=True)
    def leave_form(self):
        return request.render('school_management.student_leave_create_form_template', {
            'error': False,
            'success': False,
            'values': {}
        })

    @http.route(['/leaves/create'], type='http', auth="user", csrf=True, website=True, methods=['POST'])
    def create_leave(self, **values):
        student_id = values.get('student_id')
        class_id = values.get('class_id')
        date_from = values.get('date_from')
        date_to = values.get('date_to')
        is_half_day = values.get('is_half_day')
        half_day = values.get('half_day')
        number_of_days = values.get('number_of_days')
        reason = values.get('reason')

        if date_from > date_to:
            return request.render('school_management.student_leave_create_form_template', {
                'error': 'Start date must be lower than end date!',
                'success': False,
                'values': values
            })

        try:
            request.env['student.leave'].sudo().create({
                'student_id': student_id,
                'class_id': class_id,
                'date_from': date_from,
                'date_to': date_to,
                'is_half_day': True if is_half_day else False,
                'half_day': half_day if is_half_day else 'na',
                'reason': reason,
            })
            request.session['success_message'] = f'Leave from {date_from} to {date_to} is created'
            request.session['success_href'] = '/leaves/new'
            return request.redirect('/success')
        except Exception as e:
            print(str(e))
            request.env.cr.rollback()
            return request.render('school_management.student_leave_create_form_template', {
                'error': str(e),
                'success': False,
                'values': values
            })

class SchoolEventController(http.Controller):
    @http.route(['/event/new'], type='http', website=True, auth='user')
    def event_form(self):
        return request.render('school_management.school_event_create_form_template', {
            'error': False,
            'success': False,
            'values': {}
        })

    @http.route(['/event/create'], type='http', website=True, auth='user', csrf=True, methods=['POST'])
    def create_event(self, **values):
        name = values.get('event_name')
        club_id = values.get('club_id')
        date_begin = values.get('date_from')
        date_end = values.get('date_to')
        description = values.get('description')

        try:
            request.env['event.event'].sudo().create({
                'name': name,
                'club_id': club_id,
                'date_begin': date_begin,
                'date_end': date_end,
                'description': description,
                'date_tz': 'Asia/Kolkata',
                'website_published': True,
                'is_published': True,
            })
            request.session['success_message'] = f'Event {name} is created'
            request.session['success_href'] = '/event/new'
            return request.redirect('/success')
        except Exception as e:
            print(str(e))
            request.env.cr.rollback()
            return request.render('school_management.school_event_create_form_template', {
                'error': str(e),
                'success': False,
                'values': values
            })


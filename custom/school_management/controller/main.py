# -*- coding: utf-8 -*-
import calendar
import json
from collections import OrderedDict
from datetime import datetime
import psycopg2
from odoo import http, exceptions
from odoo.http import content_disposition, request
import ast
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
    @http.route(['/students', '/students/page/<int:page>'], type='http', auth='public', website=True)
    def students(self, page=1, **params):
        domain = []
        searchbar_filters = {
            'all': {'label': 'All', 'domain': []},
            'registered': {
                'label': 'Registered',
                'domain': [('stage', '=', 'registered')]},
            'draft': {
                'label': 'Draft',
                'domain': [('stage', '=', 'draft')]},
            'front_end': {
                'label': 'From Website',
                'domain': [('is_created_from_front_end', '=', True)]},
        }
        filterby = params.get('filterby') if params.get('filterby') else 'all'
        domain += searchbar_filters[filterby]['domain']
        students = request.env['student'].sudo()
        total = students.search_count(domain)
        item_per_page = 10
        pager = request.website.pager(
            url = '/students',
            total = total,
            page = page,
            step = item_per_page,
            scope = 5,
            url_args = params
        )
        students = students.search(domain, offset=pager['offset'], limit=item_per_page, order='id DESC')
        return request.render('school_management.students_list_template', {
            'students': students,
            'default_url': f'/students/page/{page}',
            'searchbar_filters': OrderedDict(searchbar_filters.items()),
            'filterby': filterby,
            'pager': pager,
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

    @http.route(['/student/<int:student_id>/delete'], type='http', auth='public', website=True)
    def delete_student(self, student_id):
        partner_id = request.env['student'].sudo().browse(student_id).partner_id
        request.env['res.users'].sudo().search([('partner_id', '=', partner_id.id)], limit=1).unlink()
        partner_id.unlink()
        return request.redirect('/students')

    @http.route(['/student/<int:student_id>/edit'], type='http', auth='public', website=True)
    def edit_student(self, student_id):
        student = request.env['student'].sudo().browse(student_id)
        values = {
            'first_name': student.first_name,
            'last_name': student.last_name,
            'email': student.email,
            'mobile': student.mobile,
            'dob': student.dob,
            'aadhaar': student.aadhaar_number,
            'gender': student.gender,
            'department_id': student.dept_id.id,
            'department_name': student.dept_id.name,
            'class_id': student.class_id.id,
        }
        return request.render('school_management.student_registration_form_template', {
            'error': False,
            'success': False,
            'student_id': student_id,
            'values': values
        })

    @http.route(['/students/register'], type='http', auth="user", csrf=True, website=True, methods=['POST'])
    def register_student(self, **values):
        first_name = values.get('first_name')
        last_name = values.get('last_name')
        email = values.get('email')
        mobile = values.get('mobile')
        dob = values.get('dob')
        age = values.get('age')
        aadhaar = values.get('aadhaar')
        gender = values.get('gender')
        department_id = values.get('department_id')
        class_id = values.get('class_id')
        student_id = values.get('student_id')

        try:
            if 5 > int(age) < 20:
                raise Exception('You entered age is not between 5 and 20. Please check the data is correct!')

            if student_id:
                request.env['student'].sudo().browse(int(student_id)).write({
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'mobile': mobile,
                    'dob': dob,
                    'aadhaar_number': aadhaar,
                    'gender': gender,
                    'class_id': int(class_id),
                    'dept_id': int(department_id),
                    'is_created_from_front_end': True,
                })
            else:
                request.env['student'].sudo().create({
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'mobile': mobile,
                    'dob': dob,
                    'aadhaar_number': aadhaar,
                    'gender': gender,
                    'class_id': int(class_id),
                    'dept_id': int(department_id),
                    'is_created_from_front_end': True,
                    'stage': 'draft',
                })

            request.session['success_message'] = f'{'Editing' if student_id else 'Registration'} of {first_name} {last_name} is completed'
            request.session['success_href'] = '/students/registration'
            request.session['success_view'] = '/students'
            return request.redirect('/success')
        except psycopg2.errors.UniqueViolation as e:
            print(str(e))
            request.env.cr.rollback()
            return request.render('school_management.student_registration_form_template', {
                'error': f'Email ({email}) already exists',
                'success': False,
                'values': values
            })
        except exceptions.ValidationError as e:
            print(str(e))
            request.env.cr.rollback()
            return request.render('school_management.student_registration_form_template', {
                'error': f'{str(e)}',
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
        href = request.session.pop('success_href', False)
        view = request.session.pop('success_view', False)
        return request.render('school_management.form_success_template', {
            'message': message,
            'href': href,
            'view': view,
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

    @http.route(['/api/class/<int:class_id>'], type='json', auth='public', website=True)
    def api_student_data(self, class_id):
        class_res = request.env['school.class'].sudo().browse(class_id)
        res = {
            'id': class_res.id,
            'name': class_res.name,
            'department_id': {
                'id': class_res.department_id.id,
                'name': class_res.department_id.name
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
            request.session['success_view'] = '/leaves'
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
                'date_begin': datetime.strptime(date_begin, '%Y-%m-%dT%H:%M'),
                'date_end': datetime.strptime(date_end, '%Y-%m-%dT%H:%M'),
                'description': description,
                'website_published': True,
                'is_published': True,
            })
            request.session['success_message'] = f'Event {name} is created'
            request.session['success_href'] = '/event/new'
            request.session['success_view'] = '/event'
            return request.redirect('/success')
        except Exception as e:
            print(str(e))
            request.env.cr.rollback()
            return request.render('school_management.school_event_create_form_template', {
                'error': str(e),
                'success': False,
                'values': values
            })

    @http.route(['/event/widget/latest'], type="json", auth="public", website=True)
    def latest_events(self, **params):
        events_list = request.env['event.event'].sudo().search_read(
            [('club_id', '!=', False)],
            fields = ['id', 'name', 'date_begin', 'date_end', 'club_id', 'description', 'cover_properties'],
            limit = int(params.get('limit', '1')),
            order = 'id DESC'
        )

        for event in events_list:
            cover_properties = ast.literal_eval(event.get('cover_properties'))
            background_image = cover_properties.get('background-image')
            background_image_url = background_image.split("'")[1]

            date_begin_obj = event.get('date_begin')
            date_begin = {
                'year': date_begin_obj.year,
                'month': calendar.month_abbr[date_begin_obj.month],
                'day': date_begin_obj.day,
                'hour': date_begin_obj.hour,
                'minute': date_begin_obj.minute,
            }

            date_end_obj = event.get('date_end')
            date_end = {
                'year': date_end_obj.year,
                'month': calendar.month_abbr[date_end_obj.month],
                'day': date_end_obj.day,
                'hour': date_end_obj.hour,
                'minute': date_end_obj.minute,
            }

            event.update({
                'background_image_url': background_image_url,
                'date_begin': date_begin,
                'date_end': date_end
            })

        values = {
            'events': events_list,
        }
        return values


from odoo import models, fields, api


class SchoolExam(models.Model):
    """Create, edit, assign exams"""
    _name = 'school.exam'
    _description = 'School Exam'

    name = fields.Char(string='Exam')
    class_id = fields.Many2one('school.class', string='Class')
    paper_ids = fields.Many2many('school.exam.paper')
    state = fields.Selection([('draft', 'Draft'),('assigned', 'Assigned')], default='draft')

    def action_exam_assignment(self):
        self.state = 'assigned' if self.state == 'draft' else 'draft'

class SchoolExamPaper(models.Model):
    """Create, edit papers"""
    _name = 'school.exam.paper'
    _description = 'School Exam Paper'

    subject_id = fields.Many2one('school.subject', string='Subject')
    pass_mark = fields.Integer('Pass Mark')
    max_mark = fields.Integer('Total Mark')
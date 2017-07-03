from odoo import models, fields, api


class Course(models.Model):
    _name = 'test_module.course'

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    responsible_id = fields.Many2one(
        'res.users', ondelete='set null',
        string="Responsible", index=True)
    session_ids = fields.One2many(
        'test_module.session', 'course_id', string="Sessions")
    iv_id = fields.Many2one(
        'product.template',
        string="Product ID")
    duration = fields.Float(digits=(6, 2), help="Duration in days")
    seats = fields.Integer(string="Number of seats")

    instructor_id = fields.Many2one(
        'res.partner', string="Instructor",
        domain=['|', ('instructor', '=', True), ('category_id.name', 'ilike', "Teacher")])
    course_id = fields.Many2one(
        'test_module.course',
        ondelete='cascade', string="Course", required=True)
    attendee_ids = fields.Many2many(
        'res.partner', string="Attendees")

    taken_seats = fields.Float(string="Taken seats", compute='_taken_seats')

    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        for r in self:
            if not r.seats:
                r.taken_seats = 0.0
            else:
                r.taken_seats = 100.0 * len(r.attendee_ids) / r.seats

class Session(models.Model):
    _name = 'test_module.session'

    start_date = fields.Date()
    duration = fields.Float(digits=(6, 2), help="Duration in days")
    seats = fields.Integer(string="Number of seats")

    instructor_id = fields.Many2one('res.partner', string="Instructor")
    course_id = fields.Many2one('test_module.course',
        ondelete='cascade', string="Course", required=True)
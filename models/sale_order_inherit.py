from odoo import models, fields


class SaleOrderLineInherit(models.Model):
    _inherit = "sale.order"

    project_create = fields.Boolean(default=False)

    def action_create(self):
        self.project_create = True
        project = self.env['project.project'].create({
            'name': self.name,
            'partner_id': self.partner_id.id,
            'company_id': self.company_id.id
        })
        line = []
        for rec in self.order_line:
            if rec.milestone not in line:
                line.append(rec.milestone)
                task = rec.env['project.task'].create({
                    'name': 'Milestone' + str(rec.milestone),
                    'project_id': project.id,
                    'partner_id': self.partner_id.id,
                    'company_id': self.company_id.id,
                })

            rec.env['project.task'].create({
                'name': 'Milestone' + str(rec.milestone) + '/' + str(rec.product_template_id.name),
                'project_id': project.id,
                'partner_id': self.partner_id.id,
                'company_id': self.company_id.id,
                'parent_id': task.id
            })

    def action_update(self):
        task_list = self.env['project.task'].search([('project_id.name', '=', self.name)]).mapped('name')
        sl = []
        project = self.env['project.project'].search([('name', '=', self.name)])
        for rec in self.order_line:
            if ('Milestone' + str(rec.milestone) + '/' + (rec.product_template_id.name)) not in task_list:
                if ('Milestone' + str(rec.milestone)) not in task_list:
                    if rec.milestone not in sl:
                        sl.append(rec.milestone)
                        task = rec.env['project.task'].create({
                            'name': 'Milestone' + str(rec.milestone),
                            'project_id': project.id,
                            'partner_id': self.partner_id.id,
                            'company_id': self.company_id.id,
                        })

                    rec.env['project.task'].create({
                        'name': 'Milestone' + str(rec.milestone) + '/' + str(rec.product_template_id.name),
                        'project_id': project.id,
                        'partner_id': self.partner_id.id,
                        'company_id': self.company_id.id,
                        'parent_id': task.id
                    })
                else:
                    task = self.env['project.task'].search(
                        [('project_id.name', '=', self.name), ('name', '=', 'Milestone' + str(rec.milestone))])
                    rec.env['project.task'].create({
                        'name': 'Milestone' + str(rec.milestone) + '/' + str(rec.product_template_id.name),
                        'project_id': project.id,
                        'partner_id': self.partner_id.id,
                        'company_id': self.company_id.id,
                        'parent_id': task.id
                    })

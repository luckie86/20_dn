#!/usr/bin/env python
import os
import jinja2
import webapp2
import cgi

from models import Task

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("index.html")

class ToDoHaldner(BaseHandler):
    def get(self):
        return self.render_template("todo.html")

class SaveHandler(BaseHandler):
    def post(self):
        task = cgi.escape(self.request.get("name"))
        status = cgi.escape(self.request.get("status"))
        save_task = Task(task=task, status=status)
        save_task.put()
        return self.render_template("saved.html")

class AllTasksHandler(BaseHandler):
    def get(self):
        tasks = Task.query(Task.deleted == False).fetch()
        params = {"tasks": tasks}
        return self.render_template("tasks.html", params)

class EachTaskHandler(BaseHandler):
    def get(self, task_id):
        tasks = Task.get_by_id(int(task_id))
        params = {"tasks": tasks}
        return self.render_template("tasks-details.html", params)

class EditTaskHandler(BaseHandler):
    def get(self, task_id):
        task = Task.get_by_id(int(task_id))
        params = {"task": task}
        return self.render_template("edit.html", params)

    def post(self, task_id):
        task = Task.get_by_id(int(task_id))
        task.task = self.request.get("name")
        task.status = self.request.get("status")
        task.put()
        return self.redirect("/tasks")

class DeleteTaskHandler(BaseHandler):
    def get(self, task_id):
        task = Task.get_by_id(int(task_id))
        params = {"task": task}
        return self.render_template("delete.html", params)

    def post(self, task_id):
        task = Task.get_by_id(int(task_id))
        task.deleted = True
        task.put()
        return self.redirect("/tasks")

class DeletedTasksHandler(BaseHandler):
    def get(self):
        del_tasks = Task.query(Task.deleted == True).fetch()
        params = {"del_tasks": del_tasks}
        return self.render_template("deleted.html", params)

class RestoreTaskHandler(BaseHandler):
    def get(self, task_id):
        task = Task.get_by_id(int(task_id))
        params = {"task": task}
        return self.render_template("restore.html", params)

    def post(self, task_id):
        task = Task.get_by_id(int(task_id))
        task.deleted = False
        task.put()
        return self.redirect("/tasks")

class CompleteDeleteTaskHandler(BaseHandler):
    def get(self, task_id):
        task = Task.get_by_id(int(task_id))
        params = {"task": task}
        return self.render_template("complete.html", params)

    def post(self, task_id):
        task = Task.get_by_id(int(task_id))
        task.key.delete()
        return self.redirect("/deleted")

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/todo', ToDoHaldner),
    webapp2.Route('/tasks', AllTasksHandler),
    webapp2.Route('/saved', SaveHandler),
    webapp2.Route('/tasks-details/<task_id:\d+>', EachTaskHandler),
    webapp2.Route('/tasks-details/<task_id:\d+>/edit', EditTaskHandler),
    webapp2.Route('/tasks-details/<task_id:\d+>/delete', DeleteTaskHandler),
    webapp2.Route('/deleted', DeletedTasksHandler),
    webapp2.Route('/tasks-details/<task_id:\d+>/restore', RestoreTaskHandler),
    webapp2.Route('/tasks-details/<task_id:\d+>/complete', CompleteDeleteTaskHandler),
], debug=True)

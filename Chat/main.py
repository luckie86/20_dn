#!/usr/bin/env python
import os
import jinja2
import webapp2
import cgi

from models import Message

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

class SaveShowMessages(BaseHandler):
    def post(self):
        nickname = cgi.escape(self.request.get("nickname"))
        message = cgi.escape(self.request.get("message"))
        save_message = Message(nickname=nickname, message=message)
        save_message.put()
        return self.redirect("/")

    def get(self):
        messages = Message.query().fetch()
        params = {"messages": messages}
        return self.render_template("index.html", params)

app = webapp2.WSGIApplication([
    webapp2.Route('/', SaveShowMessages),
], debug=True)

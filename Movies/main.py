#!/usr/bin/env python
import os
import jinja2
import webapp2
import cgi

from models import Movie

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

class SubmitHandler(BaseHandler):
    def post(self):
        title = cgi.escape(self.request.get("title"))
        cover = cgi.escape(self.request.get("cover"))
        rate = self.request.get("rate")
        save_movie = Movie(title=title, cover=cover, rate=rate)
        save_movie.put()
        return self.redirect("/mymovies")

    def get(self):
        return self.render_template("submit.html")

class MyMoviesHandler(BaseHandler):
    def get(self):
        movies = Movie.query().fetch()
        params = {"movies": movies}
        return self.render_template("mymovies.html", params)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/submit', SubmitHandler),
    webapp2.Route('/mymovies', MyMoviesHandler),
], debug=True)

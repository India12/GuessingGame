#!/usr/bin/env python
import os
import jinja2
import webapp2
import random


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
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("index.html")

    def post(self):
        number = 26
        minimum = 0
        maximum = 51
        message = ""
        again = ""
        guess = int(self.request.get("guess"))

        if number == guess:
            message = "Congratulations, you win!"
        elif number > guess and guess > minimum and guess < maximum:
            again = "Sorry, your guess is to low."
        elif number < guess and guess > minimum and guess < maximum:
            again = "Sorry, your guess is to high."
        else:
            again = "Please enter a number between 1 an 50."

        params = {"message": message, "again": again}

        return self.render_template("result.html", params=params)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
], debug=True)

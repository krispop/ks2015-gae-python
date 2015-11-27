#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cgi
import random
import webapp2

from google.appengine.ext import ndb

class Message(ndb.Model):
  """Models an individual Guestbook entry with content and date."""
  content = ndb.StringProperty()
  time = ndb.DateTimeProperty(auto_now_add=True)

class Root(webapp2.RequestHandler):
  def get(self):
    self.response.write("""
<head>
<link rel="stylesheet" href="pure/pure-min.css">
<title>Kawaii-Science Hackathon Guestbook</title>
</head>
<body>
<h1>理系女子のHackathonにメッセージを残そう！</h1>
<table width=100%>
<td width=50%>
<form action="sign" method=post>
<textarea name=message placeholder="世界に伝えたいこと" rows=10 cols=80></textarea>
<br><input type=submit value="送信">
</form>
</td>
<td width=50% valign=top>
""")
    qry = Message.query()
    msg = qry.fetch(100)
    if len(msg) > 0:
      msg = random.choice(msg)
      self.response.write("他の人からのメッセージ:<p style='border-style: solid; border-color: blue; border-width: 2px;' align=center>")
      self.response.write(cgi.escape(msg.content))
      self.response.write("</p> @ %s" % msg.time)
      self.response.write("</td></body>")

class Send(webapp2.RequestHandler):
  def post(self):
    content = self.request.get('message')
    if len(content) < 1:
      self.response.write('もう少し面白いことを書きましょう！')
      return

    Message(content=content).put()
    self.response.write('<html><body>ありがとうございます！これを記録しました：<pre>')
    self.response.write(cgi.escape(content))
    self.response.write('</pre><a href="/">戻ります</a></body></html>')

app = webapp2.WSGIApplication([
    ('/', Root),
    ('/sign', Send)
], debug=True)

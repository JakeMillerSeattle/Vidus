from google.appengine.api import urlfetch
from django.utils import simplejson
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import urllib
import urllib2

class RPXTokenHandler(webapp.RequestHandler):

  def post(self):
    token = self.request.get('token')
    url = 'https://rpxnow.com/api/v2/auth_info'
    args = {
      'format': 'json',
      'apiKey': 'c6ff7ddfa28cc5a892a7a3f090a9cfdf9a683285',
      'token': token
      }

    r = urlfetch.fetch(url=url,
                       payload=urllib.urlencode(args),
                       method=urlfetch.POST,
                       headers={'Content-Type':'application/x-www-form-urlencoded'}
                       )

    json = simplejson.loads(r.content)

    if json['stat'] == 'ok':   
      unique_identifier = json['profile']['identifier']
      nickname = json['profile']['preferredUsername']
      email = json['profile']['email']

      # log the user in using the unique_identifier
      # this should your cookies or session you already have implemented
      self.response.headers['Content-Type'] = 'text/plain'
      self.response.out.write(unique_identifier)
      self.response.out.write(nickname)
      self.response.out.write(email)
    else:
      self.redirect('/error')


application = webapp.WSGIApplication(
                                    [('/', RPXTokenHandler)],
                                    debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()


#!/usr/bin/python
import web
render = web.template.render('templates/', base='layout')

urls = (
    '/', 'index',
    '/news', 'news',
    '/about', 'about',
)

class index:
    def GET(self):
        return render.index()

class news:
    def GET(self):
        return render.news()

class about:
    def GET(self):
        return render.about()

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

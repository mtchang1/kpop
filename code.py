import web
import os
#resolve absolute directory path
root_dir = os.path.abspath(os.path.dirname(__file__))

#render templates from folder
template_dir = root_dir + '/templates'
render = web.template.render(template_dir, base='layout')

#absolute path to sqlite db
db_dir = root_dir + '/news.db'

#debugging purposes
#web.config.debug = True

urls = (
    '/', 'index',
    '/news', 'news',
    '/discography','discography',
    '/about', 'about'
)

class index:
    def GET(self):
        return render.index()

class news:
    def GET(self):
        db = web.database(dbn='sqlite', db=db_dir)
        #retrieve only the twenty most recent articles
        articles = db.select('articles', order='epochtime DESC', limit = 20)
        update_time = db.select('articles', what='dbtime', 
                                limit = 1, order = 'dbtime DESC')[0].dbtime
        return render.news(articles,update_time)

class discography:
    def GET(self):
        return render.discography()

class about:
    def GET(self):
        return render.about()

if __name__ == "__main__":
    #development
    app = web.application(urls, globals())
    app.run()
else:
    #mod_wsgi
    app = web.application(urls, globals(), autoreload=False)
    application = app.wsgifunc()

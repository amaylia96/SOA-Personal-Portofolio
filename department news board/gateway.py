import json
import account
from nameko.rpc import RpcProxy
from werkzeug.wrappers import Response
from nameko.web.handlers import http
from urllib.parse import urlparse, parse_qs
from session import SessionProvider

class GatewayService:
    name = 'gateway'
    proxy = RpcProxy('account_service')
    auth = SessionProvider()

    @http('POST', '/login')
    def login(self, request):
        data = request.form
        result = self.proxy.getUser(data['username'], data['password'])
        res = ""
        if result:
            ses_id = self.auth.set_session(result)
            resp = Response(str(result))
            resp.set_cookie('sessionId', ses_id)
            return resp
        else:
            return resp + "failed login"

    @http('GET', '/get_all_news')
    def get_all_news(self, request):
        data = self.proxy.getAllNews()
        return json.dumps(data)

    @http('GET', '/get_news/<int:id>')
    def get_all_news(self, request, id):
        data = self.proxy.getNewsById(id)
        return json.dumps(data)

    @http('GET', '/download/<int:id>')
    def get_all_news(self, request, id):
        data = self.proxy.downloadFileById(id)
        return json.dumps(data)


    @http('POST', '/addNews')
    def addNews(self, request):
        cookies = request.cookies
        if cookies:
            data = request.form
            judul = data['judul']
            isi = data['isi']
            author = data['author']
            file = data['file']

            tmp = self.proxy.addNews(judul, isi, author, file)
            if tmp:
                return 'success'
            else:
                return 'failed'
        else:
            resp = Response('silakan login!')
            return resp

    @http('POST', '/editNews')
    def editNews(self, request):
        cookies = request.cookies
        if cookies:
            data = request.form

            idnews = data['id']
            judul = data['judul']
            isi = data['isi']

            tmp = self.proxy.editNews(idnews, judul, isi)
            if tmp:
                return 'success'
            else:
                return 'failed'
        else:
            resp = Response('silakan login!')
            return resp

    @http('GET', '/deleteNews/<int:idnews>')
    def deleteNews(self, request, idnews):
        cookies = request.cookies
        if cookies:
            tmp = self.proxy.deleteNews(idnews)
            return tmp
        else:
            resp = Response('silakan login!')
            return resp

    @http('GET', '/logout')
    def logout(self, request):
        cookies = request.cookies
        if cookies:
            ses = self.auth.delete_session(cookies['session'])
            resp = Response('logout successfully')
            return resp
        else:
            resp = Response('something wrong')
            return resp
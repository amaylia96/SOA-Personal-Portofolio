from nameko.rpc import rpc
import dependencies

class AccountService:
    name = 'account_service'
    database = dependencies.Database()

    @rpc
    def doLogin(self, username, password):
        accounts = self.database.doLogin(username, password)
        return accounts

    @rpc
    def getAllNews(self):
        news = self.database.getAllNews()
        return news

    @rpc
    def getNewsById(self, id):
        news = self.database.getNewsById(int(id))
        return news

    @rpc
    def downloadFileById(self, id):
        file = self.database.downloadFileById(int(id))
        return file

    @rpc
    def addNews(self, judul, isi, author, file):
        add = self.database.addNews(judul, isi, author, file)
        return add

    @rpc
    def editNews(self, id, judul, isi):
        update = self.database.editNews(id, judul, isi)
        return update

    @rpc
    def deleteNews(self, id):
        delete = self.database.deleteNews(int(id))
        return delete

    @rpc
    def getUser(self, username, password):
        user = self.database.getUser(username, password)
        return user
import redis
HOST='localhost'
PORT='6379'
class redis_client(object):
    def __init__(self):
        self._db=redis.Redis(host=HOST,port=PORT)
        self.name="proxies"
    def rput(self,proxy):
            self._db.rpush(self.name,proxy)
    def lget(self):
        lproxy=self._db.lrange(self.name,0,0)
        ip = lproxy.pop().decode('utf-8')
        self._db.ltrim(self.name, 1, -1)

        return  ip

    def lenth(self):
        return self._db.llen(self.name)
    def getall(self):
        return self._db.lrange(self.name,0,-1)
    def removeall(self):
        self._db.ltrim(self.name,0,0)
    def quchong(self):
        A=self._db.lrange(self.name,0,-1)
        B=set(A)
        C=list(B)
        self.removeall()
        for ip in C:
            self.rput(ip)
    def pop(self):
        return self._db.rpop(self.name)
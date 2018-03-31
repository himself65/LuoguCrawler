class IO:
    @staticmethod
    def saveToFile(fileLocation, content):
        if fileLocation == None:
            raise AttributeError("fileLocation not found")
        f = open(fileLocation, mode='w')
        f.write(content)
        f.close()

    @staticmethod
    def getJson(fileLocation='cookie.json'):
        datas = open(fileLocation, mode='r')
        datas = json.loads(datas.read())
        return datas
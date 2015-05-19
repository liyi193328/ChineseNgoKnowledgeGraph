class perHire:
    def __init__(self,post = None, unit = None, worksite = None,updateTime = None,urlLink = None):
        self.post = post
        self.unit = unit
        self.worksite = worksite
        self.updateTime = updateTime
        self.urlLink = urlLink
    def show(self):
        print(" post:",self.post," unit:",self.unit," worksit:",self.worksite," updateTime",self.updateTime)

class NGO:

    def __init__(self, name=None, enName = None,esTime=None, location=None, field=list(),
               scale=None, description=None, active = None, hire=None, image=None,orgNumber = None,
               province = None,connectionInfo = None):
        self.name = name
        self.enName = enName
        self.esTime = esTime
        self.location = location
        self.field = field
        self.scale = scale
        self.description = description
        self.active = active
        self.hire = hire
        self.image = image
        self.orgNumber = orgNumber
        self.numHire = self.numItem = self.numNews = self.numactive = 0
        self.hire = list()
        self.connectionInfo = connectionInfo

    def getname(self):
        return self.name
    def getesTime(self):
    	return self.esTime
    def getlocation(self):
    	return self.location
    def getfield(self):
    	return self.field
    def getscale(self):
    	return self.scale
    def getdecription(self):
    	return self.description
    def getimage(self):
    	return self.image
    def show(self):
        print("orgNumber:%d\nname:%s\nenName:%s\nesTime:%s\nlocation:%s\nfield: "%(self.orgNumber,self.name,self.enName,self.esTime,self.location))
        print("field: ")
        print(self.field)
        print("\n")
        print("scale:%s\ndescription:%s\nactive: %s\nimage: %s\n "%(self.scale,self.description,self.active,self.image))
        print("numHire: %d\nnumItem: %d\nnumNews: %d\nnumActive: %d\n"%(self.numHire,self.numItem,self.numNews,self.numactive))
        print("province: %s\n")

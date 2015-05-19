class NGO:

    def __init__(self, name="", enName = "",esTime=0, location="", field=list(),
               scale="", description="", active = "", image="",orgNumber = "",orgType="",
               province = "",connectionInfo = "", personCharge="",partners = list(),sponsors=list()):
        self.name = name
        self.enName = enName
        self.esTime = esTime
        self.location = location
        self.field = field
        self.scale = scale
        self.description = description
        self.active = active
        self.image = image
        self.orgNumber = orgNumber
        self.orgType=orgType
        self.personCharge = ""
        self.connectionInfo = connectionInfo
        self.province = province
        self.partners = partners
        self.sponsors = sponsors

    def show(self):
        print("orgNumber:%d\nname:%s\nenName:%s\nesTime:%s\nlocation:%s\nfield: "%(self.orgNumber,self.name,self.enName,self.esTime,self.location))
        print("field: ")
        print(self.field)
        print("\n")
        print("scale:%s\ndescription:%s\nactive: %s\nimage: %s\n "%(self.scale,self.description,self.active,self.image))
        print("numHire: %d\nnumItem: %d\nnumNews: %d\nnumActive: %d\n"%(self.numHire,self.numItem,self.numNews,self.numactive))
        print("province: %s\n")

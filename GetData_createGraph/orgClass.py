class NGO:

    def __init__(self, name="", enName = "",esTime=0, location="", field=list(),
               scale="", description="", active = "", image="",orgNumber = "",orgType="",
               province = "",connectionInfo = "", personCharge="",partners = list(),sponsors = list()):
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

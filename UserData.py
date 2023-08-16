class UserData:
    def __init__(self):
        self.Majors = []
        self.Minors = []
        self.Certificates = []

    def UpdateData(self, DataType, newData):
        if DataType == "Majors":
            self.Majors = newData
        elif DataType == "Minors":
            self.Minors = newData
        elif DataType == "Certificates":
            self.Certificates = newData
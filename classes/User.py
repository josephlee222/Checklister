from flask import flash

from classes.Address import Address


class User:
    def __init__(self, name, password, email, accountType, birthday=None, phone=None):
        try:
            self.name = str(name)
            self.password = str(password)
            self.email = str(email)
            self.accountType = str(accountType)
        except ValueError:
            print("Value error while creating User class")

        self.birthday = birthday
        self.phone = phone
        self.address = []

    def getName(self):
        return self.name

    def getPassword(self):
        return self.password

    def getEmail(self):
        return self.email

    def getAccountType(self):
        return self.accountType

    def getBirthday(self):
        return self.birthday

    def getPhone(self):
        return self.phone

    def getAddress(self):
        return self.address

    def getMedications(self):
        return self.medications

    def setPassword(self, password):
        self.password = password

    def setName(self, name):
        self.name = name

    def setAccountType(self, admin):
        self.accountType = admin

    def setBirthday(self, birthday):
        self.birthday = birthday

    def setPhone(self, phone):
        self.phone = phone

    # ONLY PASS IN ADDRESS CLASSES HERE, NO TEXT
    def setAddress(self, address):
        if isinstance(address, Address):
            self.address.append(address)
        else:
            raise ValueError("Only Address class values are accepted in setAddress")

    def setAddresses(self, addresses):
        self.address = addresses

    # ONLY PASS IN ADDRESS CLASSES HERE, NO TEXT
    def editAddress(self, id, address):
        try:
            self.address[id] = address
        except IndexError:
            flash("Unable to edit address, address does not exist.", category="error")
            return False

    def deleteAddress(self, id):
        try:
            self.address.pop(int(id))
            return True
        except IndexError:
            # Fuck me
            return False

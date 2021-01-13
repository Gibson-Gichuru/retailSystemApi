"""Module contains all the database Models and schema associated to the given models
"""

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

class Crud():

	def create(self, resource):

		db.session.add(resource)
		db.session.commit()

	def update(self):

		db.commit()

	def delete(self, resource):

		db.delete(resource)
		db.commit()


class UserRole(Crud, db.Model):

	__tablename__ = 'userRole'

	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(100), unique = True, nullable = False)

	def __init__(self, name):

		self.name = name

class Users(Crud, db.Model):

	__tablename__ = 'users'

	userId = db.Column(db.String(50), primary_key = True)
	user_first_name = db.Column(db.String(100), nullable = False)
	user_last_name = db.Column(db.String(100), nullable = False)
	user_email = db.Column(db.String(250), unique = True, nullable = False)
	user_pass_salt = db.Column(db.String(100), nullable = False)
	user_pass_hash = db.Column(db.String(300), nullable = False)
	registration_date = db.Column(db.TIMESTAMP, default = db.func.current_timestamp())
	user_role = db.Column(db.Integer, db.ForeignKey("userRole.id", ondelete = "CASCADE"))

	role = db.relationship("UserRole", backref = db.backref("Role", order_by = "Users.userId"))


	def __init__(self, Id, firstName, lastName, Email, passSalt, PassHash):

		self.userId = Id
		self.user_first_name = firstName
		self.user_last_name = lastName
		self.user_email = Email
		self.user_pass_salt = passSalt 
		self.user_pass_hash = PassHash

class ProductCategory(Crud, db.Model):

	__tablename__ = 'productCategory'

	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(100), unique = True, nullable = False)
	discount = db.Column(db.Numeric(8,2), default = 0.0, nullable = False)
	vatTax = db.Column(db.Numeric(2,1), default = 0.0, nullable = False)

	def __init__(self, name, discount, vatTax):

		self.name = name
		self.discount = discount
		self.vatTax = vatTax

class Products(Crud, db.Model):

	__tablename__ = 'products'

	productCode = db.Column(db.String(20), primary_key = True)
	productName = db.Column(db.String(100), unique = True, nullable = False)
	productDescription = db.Column(db.String(200), nullable = False)
	manufactureDate = db.Column(db.DateTime, nullable = False)
	expiryDate = db.Column(db.DateTime, nullable = False)
	quantity = db.Column(db.Integer, nullable = False)
	price = db.Column(db.Numeric(4,2), nullable = False)
	productCategory = db.Column(db.Integer, db.ForeignKey('productCategory.id', ondelete = "CASCADE"), nullable = False)

	category = db.relationship("ProductCategory", backref = db.backref("category", order_by = "productCode"))

	def __init__(self, productCode, productName, productDescription, manufactureDate, expiryDate, quantity,price):

		self.productCode = productCode
		self.productName = productName
		self.productDescription = productDescription
		self.manufactureDate = manufactureDate
		self.expiryDate = expiryDate
		self.quantity = quantity
		self.price = price

class PaymentMethod(Crud, db.Model):

	__tablename__ = 'paymentMethod'

	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(50), unique =True, nullable = True)

	def __init__(self, name):

		self.name = name

class ReceptBook(Crud, db.Model):

	__tablename__ = 'receptBook'

	receptId = db.Column(db.Integer, primary_key = True)
	dateOfPurchase = db.Column(db.DateTime, nullable = False)
	amount = db.Column(db.Numeric(8,2), nullable = False)
	meansOfpayment = db.Column(db.Integer, db.ForeignKey("paymentMethod.id", ondelete = "CASCADE"), nullable = False)

	payment = db.relationship("PaymentMethod", backref = db.backref("payments", order_by="receptId"))

	def __init__(self, dateOfPurchase, amount):

		self.dateOfPurchase = dateOfPurchase
		self.amount = amount

class Creditor(Crud, db.Model):

	__tablename__ = 'creditor'

	creditorId = db.Column(db.String(50), primary_key = True)
	creditorFistName= db.Column(db.String(50), nullable = False)
	creditorLastName = db.Column(db.String(50), nullable = False)
	creditorPhoneNumber = db.Column(db.String(70), nullable = False)
	amountDue = db.Column(db.Numeric(8,2), default = 0.0, nullable = False)
	receptNumber = db.Column(db.Integer, db.ForeignKey("receptBook.receptId", ondelete="CASCADE"), nullable = False)

	dateDue = db.Column(db.DateTime, nullable = False)

	recept = db.relationship("ReceptBook", backref = db.backref("Recept", order_by = "creditorId"))

	def __init__(self, creditorId, creditorFistName, creditorLastName, creditorPhoneNumber, amountDue, dateDue):

		self.creditorId = creditorId
		self.creditorFistName = creditorFistName
		self.creditorLastName = creditorLastName
		self.creditorPhoneNumber = creditorPhoneNumber
		self.amountDue = amountDue
		self.dateDue = dateDue





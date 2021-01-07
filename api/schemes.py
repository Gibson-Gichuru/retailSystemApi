from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow

from models import ma


class userRoleSchema(ma.Schema):

	id = fields.Integer(dump_only = True)
	name = fields.String(required = True, validate = validate.Length(3))

	users = fields.Nested("UserSchema", many = True, exclude = ('role,'))

	url  = ma.URLFor('api.userRoleResource', id = "<int:id>", _external = True)


class UserSchema(ma.Schema):

	id = fields.String(required = True, validate = validate.Length(10))
	user_first_name = fields.String(required = True)
	user_last_name = fields.String(required = True)
	user_email = fields.String(required = True, validate = validate.Length(5))
	role = fields.Nested(userRoleSchema, only = ['name', 'url'], required = True)

	@pre_load
	def process_role(self,data):

		role = data.get('Role')

		if role:

			if isinstance(role, dict):

				role_name = role.get('name')

			else:
				
				role_name = role 

			role_dict = dict(name = role_name)

		else:
			
			role_dict = {}
		data['Role'] = role_dict
		return data


class ProductCategorySchema(ma.Schema):

	id = fields.Integer(dump_only = True)
	name = fields.String(required = True, validate = validate.Length(1))
	discount = fields.Decimal(8,2)
	vatTax = fields.Decimal(2,1)

	products = fields.Nested("ProductSchema", many = True, exclude = ('category,'))

	url = URLFor('api.productCategoryResource')


class productSchema(ma.Schema):

	productCode = fields.String(required = True, validate = validate.Length(3))
	productName = fields.String(required = True, validate = validate.Length(3))
	productDetails = fields.String(required = True, validate = validate.Length(3))
	manufactureDate = fields.Date('%Y-%m-%d', required = True)
	expiryDate = fields.Date('%Y-%m-%d', required = True)

	amount = fields.Integer(required = True)

	category  = fields.Nested(ProductCategorySchema, only = ['name','discount', 'vatTax'], required = True)

	url = URLFor('api.productResource')


class paymentSchema(ma.Schema):

	id  = fields.Integer(dump_only = True)
	name = fields.String(required = True, validate = validate.Length(1))

	url = URLFor('api.paymentResource', id = "<int:id>", _external = True)

	recepts = fields.Nested('ReceptSchema', many = True, exclude=('paymentMethod',))


class ReceptSchema(ma.Schema):

	receptId = fields.Integer(dump_only = True)
	dateOfPurchase = fields.Date('%Y-%m-%d')
	amount = fields.Decimal(8,2)
	paymentMethod = fields.Nested(paymentSchema, only = ['name', 'url'])

	creditor = fields.Nested('creditorSchema', many = True, exclude = ('receptNumber',))

	url = URLFor('api.ReceptResource')


class creditorSchema(ma.Schema):

	creditorId = fields.String(required = True, validate = validate.Length(2))
	creditorFistName = fields.String(required = True, validate = validate.Length(2))
	creditorLastName = fields.String(required = True, validate = validate.Length(2))
	creditorPhoneNumber = fields.String(required = True, validate = validate.Length(2))

	amountDue = fields.Decimal(8,2)

	receptNumber = fields.Nested(ReceptSchema, only = ['receptId', 'dateOfPurchase', 'url'])

	dateDue = fields.Date('%Y-%m-%d')

from models import (UserRole, Users, ProductCategory, Products, 
	PaymentMethod,ReceptBook, Creditor, db)

from schemes import (userRoleSchema, UserSchema, ProductCategorySchema,
	productSchema,paymentSchema,ReceptSchema,creditorSchema)


from flask import Blueprint, request, jsonify, make_response
from flask_restful import Api, Resource
from sqlalchemy.exc import SQLAlchemyError

from helper import PaginationHelper

import status

from flask_httpauth import HTTPBasicAuth
from flask import g

auth = HTTPBasicAuth()

# create a function call back for the HTTPAuth to validate users

@auth.verify_password
def verify_user_password(user_email, password):

	user = Users.query.filter_by(user_email = user_email).first()

	if not user or user.verify_password(password):

		return False

	g.user = user

	return True


#create a resource class blueprint that requiers authentication

class AutheRequiredResource(Resource):

	method_decorators = [auth.login_required]




api_dp = Blueprint('api', __name__)
user_role_schema = userRoleSchema()
user_schema = UserSchema()
product_category_schema = ProductCategorySchema()
product_schema = productSchema()
payment_schema = paymentSchema()
recept_schema = ReceptSchema()
creditor_schema = creditorSchema()
api = Api(api_dp)

class userRoleResource(AutheRequiredResource):
	#resource class used to get, update and delete a given userRole

	def get(self,id):

		"""given the id we can get the reqistered role in the database"""

		role = UserRole.query.get_or_404(id)

		results  = user_role_schema.dump(role)

		return results

	def patch(self,id):

		request_dict = request.get_json(force = True)

		role = UserRole.query.get_or_404(id)

		if "name" in request_dict:

			role.name = request_dict['name']


		pdb.set_trace()

		dumped_message, dumped_error = user_role_schema.dump(role)

		if dumped_error:

			return dumped_errors, status.HTTP_400_BAD_REQUEST

		validate_errors = user_role_schema.validate(dumped_message)

		if validate_errors:

			return validate_errors, status.HTTP_400_BAD_REQUEST


		try:

			UserRole.update()

			return self.get(id)

		except SQLAlchemyError as databaseError:

			db.session.rollback()

			response  = jsonify({"Message": str(databaseError)})

			return response, status.HTTP_400_BAD_REQUEST


	def delete(self, id):

		role = UserRole.query.get_or_404(id)


		try:

			delete = role.delete(role)

			response = {"Message":"user role delete was a success"}

			return response, status.HTTP_204_NO_CONTENT

		except SQLAlchemyError as databaseError:

			db.session.rollback()

			response = jsonify({"Message": str(databaseError)})

			return response, status.HTTP_401_UNAUTHORIZED


class userRoleResourceList(AutheRequiredResource):

	#Get all the roles registered in the database and pass new role values to create new roles

	def get(self):

		pagination_helper = PaginationHelper(request, query = UserRole.query,
			key_name = "Roles", resource_for_url = "api.userroleresourcelist",
			schema = user_role_schema)

		results = pagination_helper.paginate_query()

		return results


	def post(self):

		request_dict = request.get_json()



		if not request_dict:

			response = {"Message": "No input data was given"}

			return response, status.HTTP_400_BAD_REQUEST

		errors = user_role_schema.validate(request_dict)

		
		if errors:

			return jsonifyerrors, status.HTTP_400_BAD_REQUEST


		if not UserRole.is_unique(id = 0, name = request_dict['name']):

			response = dict(Message = "A role with the given name exists")

			return response, status.HTTP_400_BAD_REQUEST

		try:

			role_name = request_dict['name']

			role = UserRole.query.filter_by(name = role_name).first()

			if role is None:

				newRole = UserRole(name = request_dict['name'])

				newRole.create(newRole)

				query = UserRole.query.get(newRole.id)

				results = user_role_schema.dump(query)

				return results, status.HTTP_201_CREATED
			

		except SQLAlchemyError as databaseError:

			db.session.rollback()

			responce = jsonify({"Message": str(databaseError)})

			return responce, status.HTTP_400_BAD_REQUEST

class userResource(AutheRequiredResource):

	def get(self, id):

		user = Users.query.get_or_404(id)

		results = user_schema.dump(user)

		return results


	def patch(self, id):

		request_dict = response.get_json(force = True)

		user = Users.query.get_or_404(id)

		if 'userId' in request_dict:

			user.userId = request_dict['userId']

		if 'user_first_name' in request_dict:

			user.user_first_name = request_dict['user_first_name']

		if 'user_last_name' in request_dict:

			user.user_last_name = request_dict['user_last_name']

		if 'email' in request_dict:
			user.email = request_dict['email']

		if 'user_pass_salt' and 'user_pass_hash' in request_dict:

			user.user_pass_salt = request_dict['user_pass_salt']

			user.user_pass_hash = request_dict['user_pass_hash']


		if 'role' in request_dict:

			checkRole = UserRole.query.filter_by(name = request_dict['role']).first

			if checkRole:

				user.role = checkRole



		dumped_message, dumped_errors = user_schema.dump(user)

		if dumped_errors:

			return dumped_errors, status.HTTP_400_BAD_REQUEST

		validate_errors = user_schema.validate(dumped_message)

		if validate_errors:

			return validate_errors, status.HTTP_400_BAD_REQUEST

		try:

			user.update()

			return self.get(id)

		except SQLAlchemyError as databaseError:

			db.session.rollback()

			response  = jsonify({"Message": str(databaseError)})

			return response, status.HTTP_401_UNAUTHORIZED


	def delete(self, id):

		user = Users.query,get_or_404(id)

		try:

			delete = user.delete(user)

			response = make_response()

			return response, status.HTTP_204_NO_CONTENT


		except SQLAlchemyError as databaseError:

			db.session.rollback()

			response = jsonify({"Message": str(databaseError)})

			return response, status.HTTP_401_UNAUTHORIZED




class userResourceList(Resource):

	@auth.login_required
	def get(self):

		pagination_helper = PaginationHelper(request, query = Users.query,
			key_name = "Users", resource_for_url = 'api.userresourcelist',
			schema = user_schema)

		results = pagination_helper.paginate_query()

		return results

	def post(self):

		request_dict = request.get_json(force = True)

		if not request_dict:

			response = {"Message":"No input data was given"}

			return response, status.HTTP_400_BAD_REQUEST

		validate_errors = user_schema.validate(request_dict)

		if validate_errors:

			return validate_errors, status.HTTP_400_BAD_REQUEST

		try:

			checkUser = Users.query.filter_by(userId = request_dict['userId'])

			if checkUser:

				response = {"Message": "user with the given Id aready exists"}

				return response, status.HTTP_302_FOUND

			else:

				role = UserRole.query.filter_by(name = request_dict['role']).first()

				if not Users.email_is_unique(request_dict['user_email']):

					response = dict(Message = "The given Email Aready exists")

					return response, status.HTTP_400_BAD_REQUEST


				newUser = Users(userId= request_dict['userId'], 
					user_first_name = request_dict['user_first_name'],
					user_last_name = request_dict['user_last_name'],
					user_email = request_dict['user_email'],
					user_pass_salt = request_dict['user_pass_salt'],
					user_pass_hash = request_dict['user_pass_hash'],
					registration_date = request_dict['registration_date'],
					user_role = role)


				newUser.create(newUser)

				query = Users.query.get(newUser.userId)

				results = user_schema.dump(query)

				return results, status.HTTP_201_CREATED

		except SQLAlchemyError as databaseError:

			db.session.rollback()

			response = jsonify({"Message":str(databaseError)})

			return response, status.HTTP_400_BAD_REQUEST

class productCategoryResource(AutheRequiredResource):

	def get(self, id):

		category = ProductCategory.query.get_or_404(id)

		results = product_category_schema.dump(category)

		return results


	def patch(self, id):

		request_dict = request.get_json(force = True)

		category = category = ProductCategory.query.get_or_404(id)

		if 'name' in request_dict:

			category.name = request_dict['name']

		if 'discount' in request_dict:

			category.discount = request_dict['discount']

		if 'vatTax' in request_dict:

			category.vatTax = request_dict['vatTax']


		dumped_message, dumped_errors = product_category_schema.dump(category)

		if dumped_errors:

			return dumped_errors, status.HTTP_400_BAD_REQUEST


		validate_errors = product_category_schema.validate(dumped_message)


		if validate_errors:

			return validate_errors, status.HTTP_400_BAD_REQUEST


		try:

			category.update(category)

			return self.get(id)


		except SQLAlchemyError as databaseError:

			db.session.rollback()
			response = jsonify({"Message":str(databaseError)})

			return response, status.HTTP_400_BAD_REQUEST


	def delete(self, id):

		category = ProductCategory.query.get_or_404(id)

		try:

			category.delete(category)

			response = make_response()

			return response, status.HTTP_204_NO_CONTENT

		except SQLAlchemyError as databaseError:

			db.session.rollback()

			response = jsonify(dict(Message= str(databaseError)))

			return response, status.HTTP_401_UNAUTHORIZED


class productCategoryResourceList(AutheRequiredResource):

	def get(self):

		pagination_helper = PaginationHelper(request, query = ProductCategory.query,
			key_name = 'Product Categories', resource_for_url = 'api.productcategoryresourcelist',
			schema = product_category_schema)

		results = pagination_helper.paginate_query()

		return results

	def post(self):

		request_dict = request.get_json(force = True)

		if not request_dict:

			response = dict(Error= "No input data was given")

			return response, status.HTTP_400_BAD_REQUEST


		errors = product_category_schema.validate(request_dict)

		if errors:

			return errors, status.HTTP_400_BAD_REQUEST


		if not ProductCategory.is_unique(id = 0, name = request_dict['name']):

			response = dict(Message = "A product Category with the given name aready exists")

			return response, status.HTTP_400_BAD_REQUEST


		try:

			checkCategory = ProductCategory.query.filter_by(name = request_dict['name']).first()


			if checkCategory is None:

				newCategory  = ProductCategory(name = request_dict['name'], 
					discount = request_dict['discount'], vatTax = request_dict['vatTax'])

				newCategory.create(newCategory)

				query = ProductCategory.query.get(newCategory.id)

				results = product_category_schema.dump(query)

				return results, status.HTTP_201_CREATED


		except SQLAlchemyError as databaseError:

			db.session.rollback()
			response = jsonify(dict(Message= str(databaseError)))

			return response, status.HTTP_400_BAD_REQUEST

class productResource(AutheRequiredResource):

	def get(self, id):

		product = Products.query.get_or_404(id)

		results = product_schema.dump(product)

		return results


	def patch(self, id):

		request_dict = request.get_json(force = True)

		product = Products.query.get_or_404(id)

		if 'productCode' in request_dict:

			product.productCode = request_dict['productCode']


		if 'productName' in request_dict:

			product.productName = request_dict['productName']

		if 'productDescription' in request_dict:

			product.productDescription = request_dict['productDescription']

		if 'manufactureDate' in request_dict:

			product.manufactureDate = request_dict['manufactureDate']

		if 'expiryDate' in request_dict:

			product.expiryDate = request_dict['expiryDate']

		if 'price' in request_dict:

			product.amount = request_dict['price']

		if 'quatity' in request_dict:

			product.quatity = request_dict['quatity']

		if 'category' in request_dict:

			checkCategory  = ProductCategory.query.filter_by(name = request_dict['category']).first()

			if checkCategory is None:

				response = dict(Message = "The given product Category does not exist")

				return response, status.HTTP_400_BAD_REQUEST

			else:

				product.category = checkCategory


		dumped_message, dumped_errors = product_schema.dump(product)


		if dumped_errors:

			return dumped_errors, status.HTTP_400_BAD_REQUEST

		validate_errors = product_schema.validate(dumped_message)

		if  validate_errors:

			return validate_errors, status.HTTP_400_BAD_REQUEST


		try:

			product.update(product)

			return self.get(id)


		except SQLAlchemyError as databaseError:

			db.session.rollback()

			response = dict(Message= str(databaseError))

			return response, status.HTTP_400_BAD_REQUEST


	def delete(self, id):

		product = Products.query.get_or_404(id)

		try:

			delete  = product.delete(product)

			response = make_response()

			return response, HTTP_401_UNAUTHORIZED

		except SQLAlchemyError as databaseError:

			db.session.rollback()

			response = dict(Error = str(databaseError))

			return response, status.HTTP_400_BAD_REQUEST





class productResourceList(AutheRequiredResource):

	def get(self):

		pagination_helper = PaginationHelper(request, query = Products.query,
			key_name = "Products", resource_for_url = 'api.productresourcelist',
			schema = product_schema)

		results = pagination_helper = paginate_query()

		return results

	def post(self):

		request_dict = request.get_json(force = True)

		if not request_dict:

			response = dict(Message= "No imput data was given")

			return response, status.HTTP_400_BAD_REQUEST

		errors = product_schema.validate(request_dict)

		if errors:

			return errors, status.HTTP_400_BAD_REQUEST


		try:

			checkProduct = Products.query.filter_by(productCode = request_dict['productCode']).first()

			if checkProduct is None:

				newProduct = Products(productCode = request_dict['productCode'], productName = request_dict['productName'],
					productDescription = request_dict['productDescription'],expiryDate= request_dict['expiryDate'],
					quantity = request_dict['quantity'], price = request['price'])


				checkCategory = ProductCategory.query.filter_by(name = request_dict['category'])

				if checkCategory is None:

					response = dict(Error = "The given Product Category does not exist")

					return response, status.HTTP_400_BAD_REQUEST

				else:
					
					newProduct.category = checkCategory
					newProduct.create(newProduct)

					query = Products.query.get(newProduct.id)

					results = product_schema.dump(query)

					return results, status,HTTP_201_CREATED

			else:

				response = dict(Message = "Product with the given productCode aready exists")

				return response, status.HTTP_400_BAD_REQUEST

		except SQLAlchemyError as databaseError:

			db.session.rollback()

			response = jsonify(dict(Message= str(databaseError)))

			return response, status.HTTP_400_BAD_REQUEST

class paymentResource(AutheRequiredResource):
	
	def get(self, name):

		paymentMode = PaymentMethod.query.get_or_404(name)

		results = payment_schema.dump(paymentMode)

		return results

	def patch(self, name):

		request_dict = request.get_json(force = True)

		paymentMode = PaymentMethod.query.get_or_404(name)

		if 'name' in request_dict:

			paymentMode.name = request_dict['name']


		dumped_message, dumped_errors = payment_schema.dump(paymentMode)

		if dumped_errors:

			return dumped_errors, status.HTTP_400_BAD_REQUEST

		validate_errors = payment_schema.validate(dumped_message)

		if validate_errors:

			return validate_errors, status.HTTP_400_BAD_REQUEST


		try:

			paymentMode.update()
			return self.get(name)

		except SQLAlchemyError as databaseError:

			db.session.rollback()

			response = jsonify(dict(Message = str(databaseError)))

			return response, status.HTTP_400_BAD_REQUEST


	def delete(self,name):

		paymentMode = paymentMode.query.get_or_404(name)

		try:

			delete = paymentMode.delete(paymentMode)

			response = make_response()

			return response, status.HTTP_204_NO_CONTENT

		except SQLAlchemyError as databaseError:

			db.session.rollback()

			response = jsonify(dict(Message= str(databaseError)))

			return response, status.HTTP_401_UNAUTHORIZED

class paymentResourceList(AutheRequiredResource):

	def get(self):

		pagination_helper = PaginationHelper(request, query = PaymentMethod.query,
			key_name = 'Payment Methods', resource_for_url='api.paymentresourcelist',
			schema = payment_schema)

		results = pagination_helper.paginate_query()

		return results


	def post(self):

		request_dict = request.get_json(force = True)

		if not request_dict:

			response = dict(Message= "No input data provided")

			return response, status.HTTP_400_BAD_REQUEST

		errors = payment_schema.validate(request_dict)

		if errors:

			return errors, HTTP_400_BAD_REQUEST


		if not ReceptBook.is_unique(id = 0, name = request_dict['name']):

			response = dict(Message = "A payment Method with the given name exists")

			return response, status.HTTP_400_BAD_REQUEST

		try:

			checkPaymentMode = PaymentMethod.query.filter_by(name = request_dict['name']).first()

			if checkPaymentMode is None:

				newPaymentMode = PaymentMethod(name = request_dict['name'])

				newPaymentMode.create(newPaymentMode)

				query = PaymentMethod.query.get(newPaymentMode.id)

				results = payment_schema.dump(query)

				return results, status.HTTP_201_CREATED

		except SQLAlchemyError as databaseError:

			db.session.rollback()

			response = jsonify(dict(Message= str(databaseError)))

			return response, status.HTTP_400_BAD_REQUEST



class receptResource(AutheRequiredResource):
	def get(self, id):

		recept = ReceptBook.query.get_or_404(id)

		results = recept_schema.dump(recept)

		return results

	def patch(self, id):

		request_dict = request.get_json(force = True)

		recept = ReceptBook.query.get_or_404(id)

		if 'dateOfPurchase' in request_dict:

			recept.dateOfPurchase = request_dict['dateOfPurchase']

		if 'amount' in request_dict:

			recept.amount = request_dict['amount']

		if 'meansOfpayment' in request_dict:

			checkPaymentMode = PaymentMethod.query.filter_by(name = request_dict['name']).first()

			if checkPaymentMode is None:

				response = dict(Message= "Payment method {} not available".format(request['meansOfpayment']))

				return response, status.HTTP_400_BAD_REQUEST

			else:

				
				recept.meansOfpayment = checkPaymentMode

				errors = recept_schema.validate(request_dict)

				if errors:

					return errors, status.HTTP_400_BAD_REQUEST


				try:
					recept.update()

					return self.get(id)
				except SQLAlchemyError as databaseError:

					db.session.rollback()

					response = jsonify(dict(Message= str(databaseError)))

					return response, status.HTTP_400_BAD_REQUEST

	def delete(self, id):

		paymentMode = PaymentMethod.query.get_or_404(id)

		try:
			delete = paymentMode.delete(paymentMode)
			response = make_response()

			return response, status.HTTP_204_NO_CONTENT

		except SQLAlchemyError as databaseError:
			
			db.session.rollback()

			response = jsonify(dict(Message= str(databaseError)))

			return response, status.HTTP_400_BAD_REQUEST
			

class receptResourceList(AutheRequiredResource):
	
	def get(self):

		pagination_helper = PaginationHelper(request, query = ReceptBook.query,
			key_name = 'recepts', resource_for_url = 'api.receptresourcelist',
			schema = recept_schema)

		results = pagination_helper.paginate_query()

		return results

	def post(self):

		request_dict = request.get_json(force = True)

		if not request_dict:

			response = dict(Message= "No data input was given")

		errors = recept_schema.validate(request_dict)

		if errors:

			return errors, status.HTTP_400_BAD_REQUEST

		try:
			newRecept = ReceptBook(dateOfPurchase = request_dict['dateOfPurchase'],
				amount = request_dict['amount'])

			checkPaymentMode = PaymentMethod.query.filter_by(name = request_dict['meansOfpayment'])

			if checkPaymentMode is None:

				response = dict(Message= "Payment method not available")

				return response, status.HTTP_400_BAD_REQUEST

			else:
				
				newRecept.meansOfpayment = checkPaymentMode

				newRecept.create(newRecept)

				query = ReceptBook.query.get(newRecept.receptId)

				results = recept_schema.dump(query)

				return results, status.HTTP_201_CREATED
			
		except SQLAlchemyError as databaseError:
			
			db.session.rollback()

			response = jsonify(dict(Message= str(databaseError)))

			return response, status.HTTP_400_BAD_REQUEST

class creditorResource(AutheRequiredResource):

	def get(self, id):

		creditor = Creditor.query.get_or_404(id)

		results = creditorSchema.dump(creditor) 

		return results

	def patch(self, id):

		request_dict = request.get_json(force = True)

		creditor = Creditor.query.get_or_404(id)

		if 'creditorId' in request_dict:
			creditor.creditorId = request_dict['creditorId']

		if 'creditorFistName' in request_dict:
			creditor.creditorFistName = request_dict['creditorFistName']

		if 'creditorLastName' in request_dict:

			creditor.creditorLastName = request_dict['creditorLastName']

		if 'amountDue' in request_dict:

			creditor.amountDue = request_dict['amountDue']

		if 'dateDue' in request_dict:

			creditor.dateDue = request_dict['dateDue']

		if 'recept' in request_dict:

			checkRecept = ReceptBook.query.filter_by(receptId = request_dict['recept'])

			if checkRecept:

				creditor.recept = checkRecept

		dumped_message, dumped_errors = creditorSchema.dump(creditor)

		if dumped_errors:

			return dumped_errors, status.HTTP_400_BAD_REQUEST

		validate_errors = creditorSchema.validate(dumped_message)

		if validate_errors:

			return validate_errors, status.HTTP_400_BAD_REQUEST


		try:

			creditor.update()

			return self.get(id)

		except SQLAlchemyError as databaseError:

			db.session.rollback()

			response  = jsonify(dict(Message= str(databaseError)))

			return response, status.HTTP_400_BAD_REQUEST


	def delete(self, id):

		creditor = Creditor.query.get_or_404(id)

		try:
			delete = creditor.deleta(creditor)

			response = make_response()

			return response, status.HTTP_204_NO_CONTENT
		except SQLAlchemyError as databaseError:
			
			db.session.rollback()

			response = jsonify(dict(Message=str(databaseError)))

			return response, status.HTTP_401_UNAUTHORIZED


class creditorResourceList(AutheRequiredResource):

	def get(self):

		pagination_helper = PaginationHelper(request, query = Creditor.query, 
			key_name = 'Creditors', resource_for_url = 'api.creditorresourcelist',
			schema = creditor_schema)

		results = pagination_helper.paginate_query()

		return results

	def post(self):

		request_dict = request.get_json(force = True)

		if not request_dict:

			response = dict(Message= "No input data was provided ")

			return response, status.HTTP_400_BAD_REQUEST

		errors = creditor_schema.validate(request_dict)

		if errors:

			return errors, status.HTTP_400_BAD_REQUEST

		try:

			newCreditor = Creditor(creditorId = request_dict['creditorId'],
				creditorFistName = request_dict['creditorFistName'], 
				creditorLastName = request_dict['creditorLastName'], 
				creditorPhoneNumber = request_dict['creditorPhoneNumber'],
				amountDue = request_dict['amountDue'])

			checkRecept = ReceptBook.query.filter_by(receptId = request_dict['recept']).first()

			if checkRecept:

				newCreditor.recept = checkRecept

				newCreditor.create(newCreditor)

				query = Creditor.query.get(newCreditor.id)

				results = creditor_schema.dump(query)

				return results, status.HTTP_201_CREATED


			else:
				
				response = dict(Message = "The recept Number {} is not processed yet".format(request_dict['recept']))

				return response, status.HTTP_400_BAD_REQUEST

		except SQLAlchemyError as databaseError:

			db.session.rollback()

			response = jsonify(dict(Message = str(databaseError)))

			return response, status.HTTP_400_BAD_REQUEST
			

api.add_resource(userRoleResourceList,'/userRoles/')
api.add_resource(userRoleResource, '/userRoles/<int:id>')
api.add_resource(userResourceList, '/users/')
api.add_resource(userResource, '/users/<int:id>')
api.add_resource(productCategoryResourceList,'/ProductCategory/')
api.add_resource(productCategoryResource, '/ProductCategory/<int:id>')
api.add_resource(productResourceList,'/products/')
api.add_resource(productResource, '/products/<productCode>')
api.add_resource(paymentResourceList, '/payments/')
api.add_resource(paymentResource,'/payments/<int:id>')
api.add_resource(receptResourceList,'/recept/')
api.add_resource(receptResource,'/recept/<int:id>')
api.add_resource(creditorResourceList, '/creditor/')
api.add_resource(creditorResource, '/creditor/<id>')

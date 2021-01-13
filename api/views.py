from models import (UserRole, Users, ProductCategory, Products, 
	PaymentMethod,ReceptBook, Creditor, db)

from schemes import (userRoleSchema, UserSchema, ProductCategorySchema,
	productSchema,paymentSchema,ReceptSchema,creditorSchema)


from flask import Blueprint, request, jsonify, make_response
from flask_restful import Api, Resource
from sqlalchemy.exc import SQLAlchemyError

import status

api_dp = Blueprint('api', __name__)
user_role_schema = userRoleSchema()
user_schema = UserSchema()
product_category_schema = ProductCategorySchema()
product_schema = productSchema()
payment_schema = paymentSchema()
recept_schema = ReceptSchema()
creditor_schema = creditorSchema()
api = Api(api_dp)

class userRoleResource(Resource):
	#resource class used to get, update and delete a given userRole

	def get(self,id):

		"""given the id we can get the reqistered role in the database"""

		role = UserRole.query.get_or_404(id)

		results  = userRoleSchema.dump(role).data

		return results

	def patch(self,id):

		request_dict = request.get_json(force = True)

		role = role = UserRole.query.get_or_404(id)

		if "name" in request_dict:

			role.name = request_dict['name']

		dumped_message, dumped_errors = userRoleSchema.dump(role)

		if dumped_errors:

			return dumped_errors, status.HTTP_400_BAD_REQUEST

		validate_errors = userRoleSchema.validate(dumped_message)

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

			response = make_response

			return response, status.HTTP_204_NO_CONTENT

		except SQLAlchemyError as databaseError:

			db.session.rollback()

			response = jsonify({"Message": str(databaseErrors)})

			return response, status.HTTP_401_UNAUTHORIZED


class userRoleResourceList(Resource):

	#Get all the roles registered in the database and pass new role values to create new roles

	def get(self):

		roles = UserRole.query.all()

		results = userRoleSchema.dump(roles, many = True).data

		return results


	def post(self):

		request_dict = request.get_json(force = True)

		if not request_dict:

			response = {"Message": "No input data was given"}

			return response, status.HTTP_400_BAD_REQUEST


		errors = userRoleSchema.validate(request_dict)

		if errors:

			return errors, status.HTTP_400_BAD_REQUEST

		try:

			role = UserRole.query.filter_by(name = request_dict['name']).first()

			if role:

				response = {"Message": "Role with a given name Exists"}

				return response, status.HTTP_400_BAD_REQUEST

			else:

				newRole = UserRole(name = request_dict['name'])

				newRole.create(newRole)

				query = UserRole.query.get(newRole.id)

				results = userRoleSchema.dump(query).data

				return results, status.HTTP_201_CREATED


		except SQLAlchemyError as databaseError:

			db.session.rollback()

			response = jsonify({"Message": str(databaseErrors)})

			return response, HTTP_400_BAD_REQUEST

class userResource(Resource):

	def get(self, id):

		user = Users.query.get_or_404(id)

		results = UserSchema.dump(user).data

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



		dumped_message, dumped_errors = UserSchema.dump(user)

		if dumped_errors:

			return dumped_errors, status.HTTP_400_BAD_REQUEST

		validate_errors = UserSchema.validate(dumped_message)

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

	def get(self):

		users = Users.query.all()

		results = UserSchema.dump(users).data

		return results

	def post(self):

		request_dict = request.get_json(force = True)

		if not request_dict:

			response = {"Message":"No input data was given"}

			return response, status.HTTP_400_BAD_REQUEST

		validate_errors = UserSchema.validate(request_dict)

		if validate_errors:

			return validate_errors, status.HTTP_400_BAD_REQUEST

		try:

			checkUser = Users.query.filter_by(userId = request_dict['userId'])

			if checkUser:

				response = {"Message": "user with the given Id aready exists"}

				return response, status.HTTP_302_FOUND

			else:

				role = UserRole.query.filter_by(name = request_dict['role']).first()

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

				results = UserSchema.dump(query).data

				return results, status.HTTP_201_CREATED

		except SQLAlchemyError as databaseError:

			db.session.rollback()

			response = jsonify({"Message":str(databaseError)})

			return response, status.HTTP_400_BAD_REQUEST

class productCategoryResource(Resource):

	def get(self, id):

		category = ProductCategory.query.get_or_404(id)

		results = ProductCategorySchema.dump(category).data

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


		dumped_message, dumped_errors = ProductCategorySchema.dump(category)

		if dumped_errors:

			return dumped_errors, status.HTTP_400_BAD_REQUEST


		validate_errors = ProductCategorySchema.validate(dumped_message)


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


class productCategoryResourceList(Resource):

	def get(self):

		categoryList = ProductCategory.query.all()

		results = ProductCategorySchema.dump(categoryList,many = True,).data

		return results

	def post(self):

		request_dict = request.get_json(force = True)

		if not request_dict:

			response = dict(Error= "No input data was given")

			return response, status.HTTP_400_BAD_REQUEST


		errors = ProductCategorySchema.validate(request_dict)

		if errors:

			return errors, status.HTTP_400_BAD_REQUEST


		try:

			checkCategory = ProductCategory.query.filter_by(name = request_dict['name']).first()


			if checkCategory is None:

				newCategory  = ProductCategory(name = request_dict['name'], 
					discount = request_dict['discount'], vatTax = request_dict['vatTax'])

				newCategory.create(newCategory)

				query = ProductCategory.query.get(newCategory.id)

				results = ProductCategorySchema.dump(query).data

				return results, status.HTTP_201_CREATED


		except SQLAlchemyError as databaseError:

			db.session.rollback()
			response = jsonify(dict(Message= str(databaseError)))

			return response, status.HTTP_400_BAD_REQUEST

class productResource(Resource):

	def get(self, id):

		product = Products.query.get_or_404(id)

		results = productSchema.dump(product).data

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


		dumped_message, dumped_errors = productSchema.dump(product)


		if dumped_errors:

			return dumped_errors, status.HTTP_400_BAD_REQUEST

		validate_errors = productSchema.validate(dumped_message)

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





class productResourceList(Resource):

	def get(self):

		products = Products.query.all()

		results = productSchema.dump(products,many = True)

		return results

	def post(self):

		request_dict = request.get_json(force = True)

		if not request_dict:

			response = dict(Message= "No imput data was given")

			return response, status.HTTP_400_BAD_REQUEST

		errors = productSchema.validate(request_dict)

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

					results = productSchema.dump(query).data

					return results, status,HTTP_201_CREATED

			else:

				response = dict(Message = "Product with the given productCode aready exists")

				return response, status.HTTP_400_BAD_REQUEST

		except SQLAlchemyError as databaseError:

			db.session.rollback()

			response = jsonify(dict(Message= str(databaseError)))

			return response, status.HTTP_400_BAD_REQUEST

class paymentResource(Resource):
	
	def get(self, name):

		paymentMode = PaymentMethod.query.get_or_404(name)

		results = paymentSchema.dump(paymentMode).data

		return results

	def patch(self, name):

		request_dict = request.get_json(force = True)

		paymentMode = PaymentMethod.query.get_or_404(name)

		if 'name' in request_dict:

			paymentMode.name = request_dict['name']


		dumped_message, dumped_errors = paymentSchema.dump(paymentMode)

		if dumped_errors:

			return dumped_errors, status.HTTP_400_BAD_REQUEST

		validate_errors = paymentSchema.validate(dumped_message)

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

class paymentResourceList(Resource):

	def get(self):

		paymentModes = PaymentMethod.query.all()

		results = paymentSchema.dump( paymentModes,many = True)

		return results


	def post(self):

		request_dict = request.get_json(force = True)

		if not request_dict:

			response = dict(Message= "No input data provided")

			return response, status.HTTP_400_BAD_REQUEST

		errors = paymentSchema.validate(request_dict)

		if errors:

			return errors, HTTP_400_BAD_REQUEST

		try:

			checkPaymentMode = PaymentMethod.query.filter_by(name = request_dict['name']).first()

			if checkPaymentMode is None:

				newPaymentMode = PaymentMethod(name = request_dict['name'])

				newPaymentMode.create(newPaymentMode)

				query = PaymentMethod.query.get(newPaymentMode.id)

				results = paymentSchema.dump(query).data

				return results, status.HTTP_201_CREATED

		except SQLAlchemyError as databaseError:

			db.session.rollback()

			response = jsonify(dict(Message= str(databaseError)))

			return response, status.HTTP_400_BAD_REQUEST



class receptResource(Resource):
	def get(self, id):

		recept = ReceptBook.query.get_or_404(id)

		results = ReceptSchema.dump(recept).data

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
			

class receptResourceList(Resource):
	
	def get(self):

		recepts = ReceptBook.query.all()

		results = ReceptSchema.dump(recepts,many = True)

		return results

	def post(self):

		request_dict = request.get_json(force = True)

		if not request_dict:

			response = dict(Message= "No data input was given")

		errors = ReceptSchema.validate(request_dict)

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

				results = ReceptSchema.dump(query).data

				return results, status.HTTP_201_CREATED
			
		except SQLAlchemyError as databaseError:
			
			db.session.rollback()

			response = jsonify(dict(Message= str(databaseError)))

			return response, status.HTTP_400_BAD_REQUEST

class creditorResource(Resource):

	def get(self, id):

		creditor = Creditor.query.get_or_404(id)

		results = creditorSchema.dump(creditor).data 

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


class creditorResourceList(Resource):

	def get(self):

		creditors = Creditor.query.all()

		results = creditorSchema(creditors,many = True)

		return results

	def post(self):

		request_dict = request.get_json(force = True)

		if not request_dict:

			response = dict(Message= "No input data was provided ")

			return response, status.HTTP_400_BAD_REQUEST

		errors = creditorSchema.validate(request_dict)

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

				results = creditorSchema.dump(query).data

				return results, status.HTTP_201_CREATED


			else:
				
				response = dict(Message = "The recept Number {} is not processed yet".format(request_dict['recept']))

				return response, status.HTTP_400_BAD_REQUEST

		except SQLAlchemyError as databaseError:

			db.session.rollback()

			response = jsonify(dict(Message = str(databaseError)))

			return response, status.HTTP_400_BAD_REQUEST
			

api.add_resource(userRoleResourceList,'/userRoles')
api.add_resource(userRoleResource, '/userRoles/<int:id>')
api.add_resource(userResourceList, '/users')
api.add_resource(userResource, '/users/<int:id>')
api.add_resource(productCategoryResourceList,'/ProductCategory')
api.add_resource(productCategoryResource, '/ProductCategory/<int:id>')
api.add_resource(productResourceList,'/products')
api.add_resource(productResource, '/products/<productCode>')
api.add_resource(paymentResourceList, '/payments')
api.add_resource(paymentResource,'/payments/<int:id>')
api.add_resource(receptResourceList,'/recept')
api.add_resource(receptResource,'/recept/<int:id>')
api.add_resource(creditorResourceList, '/creditor')
api.add_resource(creditorResource, '/creditor/<id>')

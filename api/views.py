from models import (UserRole, Users, ProductCategory, Prodcuts, 
	PaymentMethod,ReceptBook, Creditor, db)

from schemes import (userRoleSchema, UserSchema, ProductCategorySchema,
	productSchema,paymentSchema,ReceptSchema,creditorSchema)


from flask import Blueprint, request, jsonify, make_response
from flask_restful import Api, Resource,
from sqlalchemy.exc import SQLAlchemyError

import status

api_bp = Blueprint('api', __name__)
user_role_schema = userRoleSchema()
user_schema = UserSchema()
product_category_schema = ProductCategorySchema()
product_schema = productSchema()
payment_schema = paymentSchema()
recept_schema = ReceptSchema()
creditor_schema = creditorSchema()
api = Api(api_bp)

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

			response  = jsonify({"ERROR": str(databaseError)})

			return response, status.HTTP_400_BAD_REQUEST


	def delete(self, id):

		role = UserRole.query.get_or_404(id)

		try:

			UserRole.delete(role)

			response = make_response

			return response, status.HTTP_204_NO_CONTENT

		except SQLAlchemyError as databaseError:

			db.session.rollback()

			response = jsonify({"Error": str(databaseErrors)})

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

			response = {"Input Error": "No input data was given"}

			return response, status.HTTP_400_BAD_REQUEST

		validate_errors = userRoleSchema.validate(request_dict)

		if validate_errors:

			return validate_errors, status.HTTP_400_BAD_REQUEST

		try:

			role = UserRole.query.filter_by(name = request_dict['name']).first()

			if role:

				response = {"Error": "Role with a given name Exists"}

				return response, status.HTTP_400_BAD_REQUEST

			else:

				newRole = UserRole(name = request_dict['name'])

				newRole.create(newRole)

				query = UserRole.query.get(newRole.id)

				results = userRoleSchema.dump(query).data

				return results, status.HTTP_201_CREATED


		except SQLAlchemyError as databaseError:

			db.session.rollback()

			response = jsonify({"Error": str(databaseErrors)})

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

			if checkRole not None:

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

			response  = jsonify({"Errors": str(databaseError)})

			return response, status.HTTP_401_UNAUTHORIZED


	def delete(self, id):

		user = Users.query,get_or_404(id)

		try:

			User.delete(user)

			response = make_response()

			return response, status.HTTP_204_NO_CONTENT


		except SQLAlchemyError as databaseError:

			db.session.rollback()

			response = jsonify({"Error": str(databaseError)})

			return response, status.HTTP_401_UNAUTHORIZED




class userResourceList(Resource):

	def get(self):

		users = Users.query.all()

		results = UserSchema.dump(users).data

		return results

	def post(self):

		request_dict = request.get_json(force = True)

		if not request_dict:

			response = {"Input Error":"No input data was given"}

			return response, status.HTTP_400_BAD_REQUEST

		validate_errors = UserSchema.validate(request_dict)

		if validate_errors:

			return validate_errors, status.HTTP_400_BAD_REQUEST

		try:

			checkUser = Users.query.filter_by(userId = request_dict['userId'])

			if checkUser not None:

				response = {"Error": "user with the given Id aready exists"}

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

			response = jsonify({"Error":str(databaseError)})

			return response, status.HTTP_400_BAD_REQUEST

class productCategoryResource(Resource):

	pass

class productCategoryResourceList(Resource):

	pass

class productResource(Resource):

	pass

class productResourceList(Resource):

	pass

class paymentResource(Resource):
	pass

class paymentResourceList(Resource):

	pass

class receptResource(Resource):
	pass

class receptResourceList(Resource):
	pass

class creditorResource(Resource):

	pass

class creditorResourceList(Resource):

	pass


api.add_resource(userRoleResource, '/userRoles')
api.add_resource(userRoleResourceList,'userRoles/<int:id>')
api.add_resource(userResource, '/users')
api.add_resource(userResourceList, '/users/<int:id>')
api.add_resource(productCategoryResource, '/ProductCategory')
api.add_resource(productCategoryResourceList,'/ProductCategory/<int:id>')
api.add_resource(productResource, '/products')
api.add_resource(productResourceList,'/products/<productCode>')
api.add_resource(paymentResource,'/payments')
api.add_resource(paymentResourceList, '/payments/<int:id>')
api.add_resource(receptResource,'/recept')
api.add_resource(receptResourceList,'/recept/<int:id>')
api.add_resource(creditorResource, '/creditor')
api.add_resource(creditorResourceList, '/creditor/<id>')







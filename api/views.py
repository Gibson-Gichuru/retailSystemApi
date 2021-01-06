from models import (UserRole, Users, ProductCategory, Prodcuts, 
	PaymentMethod,ReceptBook, Creditor)

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

	pass

class userRoleResourceList(Resource):

	pass

class userResource(Resource):

	pass

class userResourceList(Resource):

	pass

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







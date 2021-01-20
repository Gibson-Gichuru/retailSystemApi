from flask import current_app
from flask import url_for

class PaginationHelper():

	def __inti__(self, request, query, key_name, resource_for_url, schema):

		self.request = request
		self.query = query
		self.key_name = key_name
		self.resource_for_url = resource_for_url
		self.schema = schema

		self.results_per_page = current_app.config['PAGINATION_PAGE_SIZE']
		self.page_argument_name = current_app.config['PAGINATION_ARGUMENT_NAME']


	def peginate_query(self):

		"""get the page_number from the request and use the page for pagation
		otherwise set default page number to be one"""

		page_number = self.request.args.get(self.page_argument_name, 1, type = int)

		paginated_objects = self.query.paginate(page_number, per_page = results_per_page,
			error_out = False)

		objects = paginated_objects.items

		if paginated_objects.has_prev:

			previous_page_url = url_for(self.resource_for_url, page = page_number-1)

		else:
			previous_page_url = None


		if paginated_objects.has_next:

			next_page_url  = url_for(self.resource_for_url, page = page_number+1)

		else:
			
			next_page_url = None

		dumped_objects = self.schema.dump(objects, many = True)

		return dict(self.key_name = dumped_objects,
			previous = previous_page_url, next = next_page_url, 
			count = paginated_objects.total)
		
		
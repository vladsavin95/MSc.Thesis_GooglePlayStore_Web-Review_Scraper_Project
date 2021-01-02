from config import api, app
from views import index, Search

# index() Route
app.add_url_rule("/", 'index', index, methods=['GET'])

# search() Route
api.add_resource(Search, "/search")
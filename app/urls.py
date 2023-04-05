from . import app, db
from . import views

app.add_url_rule('/', view_func=views.index)

app.add_url_rule('/admin/transactions/add', view_func=views.transactions_add, methods=['POST', 'GET'])
app.add_url_rule('/admin/transactions/<int:transactions_id>/update', view_func=views.admin_transactions_update, methods=['POST', 'GET'])
app.add_url_rule('/admin/transactions/<int:transactions_id>/delete', view_func=views.admin_transactions_delete, methods=['POST', 'GET'])


app.add_url_rule('/account/register', view_func=views.user_register, methods=['POST', 'GET'])
app.add_url_rule('/account/login', view_func=views.user_login, methods=['POST', 'GET'])
app.add_url_rule('/account/logout', view_func=views.user_logout)



from users.models import Users
from user_input.models import UserClick

query = Users.objects.all()
query.delete()

query = UserClick.objects.all()
query.delete()

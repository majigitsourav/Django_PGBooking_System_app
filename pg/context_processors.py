from .models import Customer
from pg.views import get_username , get_pgowner 



def username_context(request):
    user_unique_id = request.session.get('user_unique_id')
    username = get_username(user_unique_id)
    return {'username': username}

def pgownername_context(request):
    owner_unique_id = request.session.get('owner_unique_id')
    ownername = get_pgowner(owner_unique_id)
    return {'ownername': ownername}
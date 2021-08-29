<<<<<<< HEAD
from .models import user

def isLogin(request):
    if (request.session.get('islogin')=='1'):
        islogin=True
    else:
        islogin=False
        return {}
    uid=request.session.get("u_id")
    cur_user=user.objects.get(u_id=uid)
    context={
        'islogin':islogin,
        'username':cur_user.username
    }
=======
from .models import user

def isLogin(request):
    if (request.session.get('islogin')=='1'):
        islogin=True
    else:
        islogin=False
        return {}
    uid=request.session.get("u_id")
    cur_user=user.objects.get(u_id=uid)
    context={
        'islogin':islogin,
        'username':cur_user.username
    }
>>>>>>> 317414a0c132534335a43ae0a7f07a23d02566ee
    return context
from dynamicresponse.response import *
from models import VimeoUser
import operator
from django.db.models import Q

def Search(request):

    results = VimeoUser.objects.all()

    if request.GET.get('q'):
        queries = request.GET.get('q').split(',')
        qset1 =  reduce(operator.__or__, [Q(display_name__icontains=query) | Q(user_name__icontains=query) \
                                                                for query in queries])
        results = results.filter(qset1).distinct()

    if request.GET.get('is_pay'):
        results = results.filter(is_pay=True)

    if request.GET.get('has_staff_pick'):
        results = results.filter(has_staff_pick=True)

    if request.GET.get('has_videos'):
        results = results.filter(has_videos=True)        

    return SerializeOrRender(request,{'params':dict(request.GET),'results':results[:100],'count':results.count()})


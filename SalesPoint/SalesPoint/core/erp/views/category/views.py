from django.shortcuts import render
from SalesPoint.core.erp.models import Category

def category_list(request):
    data = {
        'categories': Category.objects.all()
    }
    return render(request, 'category/list.html', data)
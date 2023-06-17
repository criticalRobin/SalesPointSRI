from django.shortcuts import render
from SalesPoint.core.erp.models import Category
from django.views.generic import ListView

def category_list(request):
    data = {
        'categories': Category.objects.all()
    }
    return render(request, 'category/list.html', data)


class CategoryListView(ListView):
    model = Category
    template_name = 'category/list.html'
    
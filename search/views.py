from django.shortcuts import render
from shop.models import Product
from .forms import SearchForm
from cart.forms import CartAddProductForm
from django.contrib.postgres.search import SearchVector


# Create your views here.
def product_search(request):
    form = SearchForm()
    query = None
    results = []
    cart_product_form = CartAddProductForm()
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            available_prod = Product.objects.filter(available=True)
            results = available_prod.annotate(
                search=SearchVector('name', 'description'),
            ).filter(search=query)
    return render(request,
                  'search/search.html',
                  {'form': form,
                   'query': query,
                   'results': results,
                   'cart_product_form': cart_product_form})


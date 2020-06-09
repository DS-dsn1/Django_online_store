from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm
from .forms import ReviewForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    object_list = Product.objects.filter(available=True)
    # products = Product.objects.filter(available=True)
    cart_product_form = CartAddProductForm()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        object_list = object_list.filter(category=category)

    paginator = Paginator(object_list, 9)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'page': page,
                   'products': products,
                   'cart_product_form': cart_product_form})


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()

    reviews = product.reviews.filter(active=True)
    new_review = None

    if request.method == 'POST':
        review_form = ReviewForm(data=request.POST)
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.product = product
            new_review.save()
    else:
        review_form = ReviewForm()
    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'reviews': reviews,
                   'new_review': new_review,
                   'review_form': review_form,
                   'cart_product_form': cart_product_form})

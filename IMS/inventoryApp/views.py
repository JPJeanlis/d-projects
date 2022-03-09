from .models import Supplier
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from inventoryApp.forms import RenewProductForm
from django.contrib.auth.decorators import login_required, permission_required
import datetime
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.shortcuts import render

# Create your views here.

from .models import Product, Supplier, ProductInstance, Category


def index(request):
    """View function for home page of site."""
    # Generate counts of some of the main objects
    num_products = Product.objects.all().count()
    num_instances = ProductInstance.objects.all().count()
    # Available copies of products
    num_instances_available = ProductInstance.objects.filter(
        status__exact='a').count()
    # The 'all()' is implied by default.
    num_suppliers = Supplier.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits+1

    # Render the HTML template index.html with the data in the context variable.
    return render(
        request,
        'index.html',
        context={'num_products': num_products, 'num_instances': num_instances,
                 'num_instances_available': num_instances_available, 'num_suppliers': num_suppliers,
                 'num_visits': num_visits},
    )


class ProductListView(generic.ListView):
    """Generic class-based view for a list of products."""
    model = Product
    paginate_by = 10


class ProductDetailView(generic.DetailView):
    """Generic class-based detail view for a product."""
    model = Product


class SupplierListView(generic.ListView):
    """Generic class-based list view for a list of suppliers."""
    model = Supplier
    paginate_by = 10


class SupplierDetailView(generic.DetailView):
    """Generic class-based detail view for an supplier."""
    model = Supplier


class LoanedProductsByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing products on loan to current user."""
    model = ProductInstance
    template_name = 'inventoryApp/productinstance_list_sold_user.html'
    paginate_by = 10

    def get_queryset(self):
        return ProductInstance.objects.filter(employee=self.request.user).filter(status__exact='o').order_by('due_payment_date')


# Added as part of challenge!


class LoanedProductsAllListView(PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing all products on loan. Only visible to users with can_mark_paid permission."""
    model = ProductInstance
    permission_required = 'inventoryApp.can_mark_paid'
    template_name = 'inventoryApp/productinstance_list_sold_all.html'
    paginate_by = 10

    def get_queryset(self):
        return ProductInstance.objects.filter(status__exact='o').order_by('due_payment_date')


# from .forms import RenewProductForm


@login_required
@permission_required('inventoryApp.can_mark_paid', raise_exception=True)
def sell_product(request, pk):
    """View function for renewing a specific ProductInstance by employee."""
    product_instance = get_object_or_404(ProductInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewProductForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_payment_date field)
            product_instance.due_payment_date = form.cleaned_data['buying_date']
            product_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-sold'))

    # If this is a GET (or any other method) create the default form
    else:
        proposed_buying_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewProductForm(
            initial={'buying_date': proposed_buying_date})

    context = {
        'form': form,
        'product_instance': product_instance,
    }

    return render(request, 'inventoryApp/productinstance_list_sold_all.html', context)


class SupplierCreate(PermissionRequiredMixin, CreateView):
    model = Supplier
    fields = ['name', 'business_type', 'start_date', ]
    initial = {'start_date': '11/06/2020'}
    permission_required = 'inventoryApp.can_mark_paid'


class SupplierUpdate(PermissionRequiredMixin, UpdateView):
    model = Supplier
    # Not recommended (potential security issue if more fields added)
    fields = '__all__'
    permission_required = 'inventoryApp.can_mark_paid'


class SupplierDelete(PermissionRequiredMixin, DeleteView):
    model = Supplier
    success_url = reverse_lazy('suppliers')
    permission_required = 'inventoryApp.can_mark_paid'


# Classes created for the forms challenge
class ProductCreate(PermissionRequiredMixin, CreateView):
    model = Product
    fields = ['itemName', 'supplier', 'expiry', 'quantity', 'unit_cost', 'prize', 'note', 'addDate', 'summary',
              'sku', 'category', 'countryoforigin']
    permission_required = 'inventoryApp.can_mark_paid'


class ProductUpdate(PermissionRequiredMixin, UpdateView):
    model = Product
    fields = ['itemName', 'supplier', 'expiry', 'quantity', 'unit_cost', 'prize', 'addDate', 'summary',
              'sku', 'category', 'countryoforigin']
    permission_required = 'inventoryApp.can_mark_paid'


class ProductDelete(PermissionRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('products')
    permission_required = 'inventoryApp.can_mark_paid'


def page1(request):
    return render(request, 'inventoryApp/page1.html', {})


def page2(request):
    return render(request, 'inventoryApp/page2.html', {})


def page3(request):
    return render(request, 'inventoryApp/page3.html', {})

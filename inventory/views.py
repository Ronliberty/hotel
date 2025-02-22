from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from cart.models import MenuItemProduct, OrderItem, MenuItem
from .models import MainCategory, SubCategory, Product, TaxCategory, StockMovement, CounterStock, KitchenStock, SalesInvoice
from django.contrib import messages
from .forms import ProductForm, TaxCategoryForm, SubCategoryForm, SalesInvoiceForm
from django.http import JsonResponse
import requests
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import SalesInvoiceSerializer

class MainCategoryListView(LoginRequiredMixin, ListView):
    model = MainCategory
    template_name = "inventory/main_category_list.html"
    context_object_name = "categories"
    ordering = ["name"]


    def test_func(self):
        return self.request.user.groups.filter(name__in=['manager', 'storekeeper', 'cashier']).exists()

class MainCategoryCreateView(LoginRequiredMixin, CreateView):
    model = MainCategory
    template_name = "inventory/main_category_form.html"
    fields = ['name', 'description']
    success_url = reverse_lazy('inventory:main_category_list')

    def form_valid(self, form):
        # Save the form data
        self.object = form.save()
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Return a JSON response for AJAX requests
            return JsonResponse({
                'message': 'Main Category created successfully!',
                'success_url': str(self.success_url),
            })
        messages.success(self.request, "Main Category created successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Return a JSON response with form errors
            return JsonResponse({'errors': form.errors}, status=400)
        return super().form_invalid(form)
    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()




class MainCategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = MainCategory
    template_name = "inventory/main_category_form.html"
    fields = ['name', 'description']
    success_url = reverse_lazy('inventory:main_category_list')

    def form_valid(self, form):
        messages.success(self.request, "Main Category updated successfully.")
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()


class MainCategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = MainCategory
    template_name = "inventory/main_category_confirm_delete.html"
    success_url = reverse_lazy('inventory:main_category_list')

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Main Category deleted successfully.")
        return super().delete(request, *args, **kwargs)





class SubCategoryListView(LoginRequiredMixin, ListView):
    model = SubCategory
    template_name = "inventory/sub_category_list.html"
    context_object_name = "subcategories"
    ordering = ["name"]
    def test_func(self):
        return self.request.user.groups.filter(name__in=['manager', 'storekeeper', 'cashier']).exists()

class SubCategoryCreateView(LoginRequiredMixin, CreateView):
    model = SubCategory
    form_class = SubCategoryForm
    template_name = "inventory/sub_category_form.html"

    success_url = reverse_lazy('inventory:sub_category_list')

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()

    def form_valid(self, form):
        self.object = form.save()
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'message': 'SubCategory created successfully!',
                'success_url': str(self.success_url),
            })
        messages.success(self.request, "SubCategory created successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'errors': form.errors}, status=400)
        return super().form_invalid(form)



class SubCategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = SubCategory
    template_name = "inventory/sub_category_form.html"
    fields = ['main_category', 'name', 'description']
    success_url = reverse_lazy('inventory:sub_category_list')

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()

    def form_valid(self, form):
        messages.success(self.request, "Sub Category updated successfully.")
        return super().form_valid(form)

class SubCategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = SubCategory
    template_name = "inventory/sub_category_confirm_delete.html"
    success_url = reverse_lazy('inventory:sub_category_list')

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Sub Category deleted successfully.")
        return super().delete(request, *args, **kwargs)


class SubCategoryManagerListView(LoginRequiredMixin, ListView):
    model = SubCategory
    template_name = "inventory/sub_manager_list.html"
    context_object_name = "subcategories"
    ordering = ["name"]
    def test_func(self):
        return self.request.user.groups.filter(name__in=['manager', 'storekeeper', 'cashier']).exists()

class SubCategoryManagerCreateView(LoginRequiredMixin, CreateView):
    model = SubCategory
    template_name = "inventory/sub_manager_form.html"
    form_class = SubCategoryForm
    success_url = reverse_lazy('inventory:sub_list')

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()

    def form_valid(self, form):
        # Save the form data
        self.object = form.save()
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Return a JSON response for AJAX requests
            return JsonResponse({
                'message': 'Main Category created successfully!',
                'success_url': str(self.success_url),
            })
        messages.success(self.request, "Main Category created successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Return a JSON response with form errors
            return JsonResponse({'errors': form.errors}, status=400)
        return super().form_invalid(form)



class SubCategoryManagerUpdateView(LoginRequiredMixin, UpdateView):
    model = SubCategory
    template_name = "inventory/sub_manager_form.html"
    fields = ['main_category', 'name', 'description']
    success_url = reverse_lazy('inventory:sub_list')

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()

    def form_valid(self, form):
        messages.success(self.request, "Sub Category updated successfully.")
        return super().form_valid(form)

class SubCategoryManagerDeleteView(LoginRequiredMixin, DeleteView):
    model = SubCategory
    template_name = "inventory/sub_manager_confirm_delete.html"
    success_url = reverse_lazy('inventory:sub_manager_list')

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Sub Category deleted successfully.")
        return super().delete(request, *args, **kwargs)

class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "inventory/product_list.html"
    context_object_name = "products"
    ordering = ["-created_at"]
    def test_func(self):
        return self.request.user.groups.filter(name__in=['manager', 'storekeeper', 'cashier']).exists()


class ProductManagerListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "inventory/list.html"
    context_object_name = "products"
    ordering = ["-created_at"]

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "inventory/product_detail.html"
    context_object_name = "product"
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    def test_func(self):
        return self.request.user.groups.filter(name__in=['manager', 'storekeeper', 'cashier']).exists()



class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = "inventory/product_form.html"
    form_class = ProductForm
    success_url = reverse_lazy("inventory:product_list")
    def test_func(self):
        return self.request.user.groups.filter(name__in=['manager', 'storekeeper']).exists()


    def form_valid(self, form):
        form.instance.created_by = self.request.user  # Automatically set the creator
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = "inventory/product_form.html"
    fields = [
        "sub_category", "name", "description", "sales_price", "discount", "qty",
        "cost_price", "unit", "tax_category", "volume", "weight"
    ]
    success_url = reverse_lazy("inventory:product_list")


    def test_func(self):
        return self.request.user.groups.filter(name__in=['manager', 'storekeeper']).exists()



class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "inventory/product_confirm_delete.html"
    success_url = reverse_lazy("inventory:product_list")
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


    def test_func(self):
        return self.request.user.groups.filter(name__in=['manager', 'storekeeper']).exists()



class TaxCategoryListView(ListView):
    model = TaxCategory
    template_name = "inventory/taxcategory_list.html"
    context_object_name = "taxcategories"

class TaxCategoryCreateView(CreateView):
    model = TaxCategory
    form_class = TaxCategoryForm
    template_name = "inventory/taxcategory_form.html"
    success_url = reverse_lazy('inventory:taxcategory-list')

class TaxCategoryUpdateView(UpdateView):
    model = TaxCategory
    form_class = TaxCategoryForm
    template_name = "inventory/taxcategory_form.html"
    success_url = reverse_lazy('inventory:taxcategory-list')

class TaxCategoryDeleteView(DeleteView):
    model = TaxCategory
    template_name = "inventory/taxcategory_confirm_delete.html"
    success_url = reverse_lazy('inventory:taxcategory-list')


class StockMovementView(TemplateView):
    template_name = "inventory/stock_movement.html"

    def get(self, request):
        products = Product.objects.all()
        return render(request, self.template_name, {"products": products})

    def post(self, request):
        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity"))
        source = request.POST.get("source")
        destination = request.POST.get("destination")

        product = Product.objects.get(id=product_id)

        # Deduct from the source
        if source == "store":
            if product.qty < quantity:
                messages.error(request, "Not enough stock in store!")
                return redirect("inventory:stock-movement")
            product.qty -= quantity
            product.save()

        elif source == "counter":
            counter_stock = CounterStock.objects.get(product=product)
            if counter_stock.qty < quantity:
                messages.error(request, "Not enough stock in counter!")
                return redirect("inventory:stock-movement")
            counter_stock.qty -= quantity
            counter_stock.save()

        elif source == "kitchen":
            kitchen_stock = KitchenStock.objects.get(product=product)
            if kitchen_stock.qty < quantity:
                messages.error(request, "Not enough stock in kitchen!")
                return redirect("inventory:stock-movement")
            kitchen_stock.qty -= quantity
            kitchen_stock.save()

        # Add to destination
        if destination == "counter":
            counter_stock, created = CounterStock.objects.get_or_create(product=product)
            counter_stock.qty += quantity
            counter_stock.save()

        elif destination == "kitchen":
            kitchen_stock, created = KitchenStock.objects.get_or_create(product=product)
            kitchen_stock.qty += quantity
            kitchen_stock.save()

        # Record stock movement
        StockMovement.objects.create(
            product=product, quantity=quantity, source=source, destination=destination, moved_by=request.user
        )

        messages.success(request, f"Moved {quantity} {product.name} from {source} to {destination}")
        return redirect("inventory:stock-movement")

class CounterStockListView(ListView):
    model = CounterStock
    template_name = "inventory/stock-list.html"
    context_object_name = "counter_stock"

    def get_queryset(self):
        """Fetch all counter stock items."""
        return CounterStock.objects.all()




class SalesInvoiceCreateView(View):
    def get(self, request):
        form = SalesInvoiceForm()
        return render(request, 'inventory/sales_invoice_form.html', {'form': form})

    def post(self, request):
        form = SalesInvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save()

            # Send data to KRA API
            kra_api_url = "https://api.kra.go.ke/submit-invoice"
            headers = {"Content-Type": "application/json", "Authorization": "Bearer YOUR_KRA_API_TOKEN"}
            data = {
                "invoice_number": invoice.invoice_number,
                "bought_at": invoice.bought_at.isoformat(),
                "product": invoice.product.id,
                "qty_sold": invoice.qty_sold,
                "sales_price": float(invoice.sales_price),
                "discount": float(invoice.discount),
                "tax_category": invoice.tax_category.id,
                "tax_amount": float(invoice.tax_amount),
                "total_amount": float(invoice.total_amount),
                "currency": invoice.currency,
                "issued_by": invoice.issued_by.id if invoice.issued_by else None,
            }

            response = requests.post(kra_api_url, json=data, headers=headers)

            if response.status_code == 200:
                messages.success(request, "Invoice successfully sent to KRA!")
            else:
                messages.error(request, "Error sending invoice to KRA: " + response.text)

            return redirect('create-sales-invoice')

        return render(request, 'sales_invoice_form.html', {'form': form})

class SendStockDataToKRA(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SalesInvoiceSerializer(data=request.data)
        if serializer.is_valid():
            invoice = serializer.save()

            # Send data to KRA
            kra_api_url = "https://api.kra.go.ke/submit-invoice"
            headers = {"Content-Type": "application/json", "Authorization": "Bearer YOUR_KRA_API_TOKEN"}
            data = serializer.data

            response = requests.post(kra_api_url, json=data, headers=headers)

            if response.status_code == 200:
                return Response({"message": "Invoice successfully sent to KRA!"}, status=200)
            else:
                return Response({"error": response.text}, status=response.status_code)
        return Response(serializer.errors, status=400)


# API View to list all invoices (GET request)
class SalesInvoiceListView(generics.ListAPIView):
    queryset = SalesInvoice.objects.all()
    serializer_class = SalesInvoiceSerializer
    permission_classes = [IsAuthenticated]



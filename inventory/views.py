from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import MainCategory, SubCategory, Product, TaxCategory
from django.contrib import messages
from .forms import ProductForm, TaxCategoryForm
from django.http import JsonResponse

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
    template_name = "inventory/sub_category_form.html"
    fields = ['main_category', 'name', 'description']
    success_url = reverse_lazy('inventory:sub_category_list')

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
    fields = ['main_category', 'name', 'description']
    success_url = reverse_lazy('inventory:sub_manager_list')

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
    success_url = reverse_lazy('inventory:sub_category_list')

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



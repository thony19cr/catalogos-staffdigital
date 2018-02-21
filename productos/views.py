import stripe
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from productos.models import Product
from django.conf import settings
import json


@method_decorator(csrf_exempt, name='dispatch')
class ProductAllView(View):

    def get(self, request):
        products = Product.objects.all()
        lista_productos = []
        for product in products:
            lista_productos.append({
                'id': product.id,
                'nombre_producto': product.name,
                'descripcion': product.description,
                'precio': product.details.price,
                'tipo': product.type,
                'codigo_procuto': product.code,
                'cantidad': product.details.quantity,
                'marca': product.brand.name
            })
        return HttpResponse(json.dumps(lista_productos), content_type='application/json')


@method_decorator(csrf_exempt, name='dispatch')
class GetProductoView(View):

    def get(self, request, *args, **kwargs):
        try:
            products = Product.objects.get(id=self.kwargs.get('id'))
            lista_producto = []
            for product in products:
                lista_producto.append({
                    'id': product.id,
                    'nombre_producto': product.name,
                    'descripcion': product.description,
                    'precio': product.details.price,
                    'tipo': product.type,
                    'codigo_procuto': product.code,
                    'cantidad': product.details.quantity,
                    'marca': product.brand.name
                })

            return HttpResponse(json.dumps(lista_producto), content_type='application/json', status=200)
        except Product.DoesNotExist:
            msg = 'No existe producto con ese ID'
            return JsonResponse({'msg': msg}, safe=False, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class CreateProductoView(View):

    def post(self, request, *args, **kwargs):
        producto = json.loads(request.body)
        prod = Product(
            nombre=producto.get('nombre'),
            descripcion=producto.get('descripcion')
        )
        prod.save()
        return JsonResponse({'msg': True}, safe=False, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class UpdateProductoView(View):

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        try:
            Product.objects.get(id=self.kwargs.get('id')).update(
                name=data.get('nombre'),
                description=data.get('descripcion')
            )

            return JsonResponse({'msg': True}, safe=False, status=200)
        except Product.DoesNotExist:
            msg = 'No existe producto con ese ID'
            return JsonResponse({'msg': msg}, safe=False, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class DeleteProductoView(View):

    def get(self, request, *args, **kwargs):
        try:
            Product.objects.get(id=self.kwargs.get('id')).delete()
            return JsonResponse({'msg': True}, safe=False, status=200)
        except Product.DoesNotExist:
            msg = 'No existe producto con ese ID'
            return JsonResponse({'msg': msg}, safe=False, status=400)


class SearchOnProducts(View):
    template_name = 'products/home.html'

    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(
            name__icontains=self.request.GET.get('name_product', '').encode('latin-1').replace("/", "")).all()
        if products:
            list_products = []
            for product in products:
                data = {
                    'name': product.name,
                    'description': product.description,
                    'type': product.type
                }
                list_products.append(data)
            return HttpResponse(json.dumps(list_products), content_type='application/json')
        else:
            msg = "No existe el producto"
            return JsonResponse({'msg': msg}, safe=False)


class HomeView(TemplateView):
    template_name = 'products/home.html'

    def get_context_data(self, **kwargs):
        if self.request.GET.get('name_product'):
            products = Product.objects.filter(name__icontains=self.request.GET.get('name_product', '').encode('latin-1'))
        else:
            products = Product.objects.all()
        return {'products': products}


class ProductBuyView(DetailView):
    template_name = 'products/buy.html'

    def post(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        token = request.POST['stripeToken']
        product = self.get_object()
        error_message = None
        try:
            charge = stripe.Charge.create(
                amount=product.precio,
                currency='usd',
                description='cobro por []'.format(product.nombre),
                statement_descriptor="cobro a mi marketDigital",
                source=token
            )
        except stripe.error.CardError as e:
            body = e.json_body
            err = body['error']
            error_message = err['message']
        except stripe.error.StripeError as e:
            error_message = "No puede proceder tu compra, intentelo luego"

        if error_message:
            return render(request, "products/failed.html", {'error_message': error_message, 'producto': product})

        return render(request, "products/success.html", {'debug_info': charge, 'producto': product})


class QuerySearchView(View):

    def get(self, request, *args, **kwargs):
        list_products = []
        products_list = Product.objects.all()
        paginator = Paginator(products_list, 5)
        try:
            products = paginator.page(self.kwargs.get('page'))
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        for product in products.object_list:
            list_products.append({
               'id': product.id,
                    'nombre_producto': product.name,
                    'descripcion': product.description,
                    'precio': product.details.price,
                    'tipo': product.type,
                    'codigo_procuto': product.code,
                    'cantidad': product.details.quantity,
                    'marca': product.brand.name

            })
        return HttpResponse(json.dumps(list_products), content_type='application/json', status=200)

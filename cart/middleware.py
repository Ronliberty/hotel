# yourapp/middleware.py

class EnforceKshMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Ensure all items in the cart have 'Ksh' as currency
        if 'cart' in request.session:
            for item in request.session['cart']:
                item['currency'] = 'Ksh'
        return response

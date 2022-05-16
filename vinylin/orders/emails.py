import os

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from email.mime.image import MIMEImage

from store.models import Image


class AddCartItemEmailMessage(EmailMultiAlternatives):
    def __init__(self, request, context, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.content_subtype = 'html'
        self.mixed_subtype = 'related'

        self.product_title = context['item'].product.title
        self.subject = f'\"{self.product_title}\" has been added to cart!'
        self.body = render_to_string(
            'orders/add_to_cart_email.html',
            context=context,
            request=request,
        )
        self.to = [request.user.email]

    def create_inline_image_attachment(self, image: Image):
        name, subtype = os.path.splitext(image.image.file.name)

        mimei_image = MIMEImage(image.image.read(), _subtype=subtype)
        mimei_image.add_header('Content-ID', f'<{image.image.name}>')
        return self.attach(mimei_image)

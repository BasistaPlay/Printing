from home.models import Product
from django.db.models import Count

duplicates = Product.objects.values('slug').annotate(slug_count=Count('slug')).filter(slug_count__gt=1)

for duplicate in duplicates:
    products = Product.objects.filter(slug=duplicate['slug'])
    for idx, product in enumerate(products):
        # Izmainiet slug v�rt�bu, lai t� b�tu unik�la
        product.slug = f"{product.slug}-{idx+1}"
        product.save()
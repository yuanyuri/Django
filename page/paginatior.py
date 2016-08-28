from django.core.paginator import Paginator

a = 'abcdefghijklmnopqrstuvwxyz'
limit = 10

paginator = Paginator(a, limit)
print(paginator.num_pages)

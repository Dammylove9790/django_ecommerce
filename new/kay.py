from datetime import date

print(date.today())

x = str(date.today()).split('-')[0]
print(x)


# useful scripts
# Entry.objects.get(Q(blog=blog) & Q(entry_number=1))
# Q(question__startswith="Who") | Q(question__startswith="What")

# q = Entry.objects.filter(headline__startswith="What")
# q = q.filter(pub_date__lte=datetime.date.today())
# q = q.exclude(body_text__icontains="food")
# print(q)




# Case-sensitive containment version, icontains.
# Entry.objects.get(headline__contains="Lennon")

# There’s also a case-insensitive version, icontains.
# Entry.objects.get(entry__headline__icontains="Lennon")




# from datetime import date
# from django.db import models


# class Blog(models.Model):
#     name = models.CharField(max_length=100)
#     tagline = models.TextField()

#     def __str__(self):
#         return self.name


# class Author(models.Model):
#     name = models.CharField(max_length=200)
#     email = models.EmailField()

#     def __str__(self):
#         return self.name


# class Entry(models.Model):
#     blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
#     headline = models.CharField(max_length=255)
#     body_text = models.TextField()
#     pub_date = models.DateField()
#     mod_date = models.DateField(default=date.today)
#     authors = models.ManyToManyField(Author)
#     number_of_comments = models.IntegerField(default=0)
#     number_of_pingbacks = models.IntegerField(default=0)
#     rating = models.IntegerField(default=5)

#     def __str__(self):
#         return self.headline




# Try and Catch

#     try:
#         poll = Poll.objects.get(pk=poll_id)
#     except Poll.DoesNotExist:
#         raise CommandError('Poll "%s" does not exist' % poll_id)


# To create objects
# Category.objects.create(name='furniture')
#             or 
# category = Category(name='furniture')
# category.save()
#             or
# category, _ = Category.objects.get_or_create(name='furniture')
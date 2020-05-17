from django.db import models
from check_prefetch import Model, Manager


class Author(Model):
    name = models.CharField(max_length=100)


class Publisher(Model):
    name = models.CharField(max_length=100)


class Reporter(Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


class BooksManager(Manager):
    def get_author(self):
        return self.values("author")


class Books(Model):
    name = models.CharField(max_length=100)
    author = models.ManyToManyField(Author, related_name="books")
    publisher = models.ManyToManyField(Publisher, related_name="books_publisher")
    reporter = models.ForeignKey(
        Reporter, blank=True, null=True, on_delete=models.CASCADE
    )

    objects = BooksManager()

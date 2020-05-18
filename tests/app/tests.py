from django.test import TestCase
from app.models import Books, Author, Reporter, DjangoModel
from check_prefetch import PrefetchUnusedWarning, Manager


class Test(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.reporter = Reporter.objects.create(
            first_name="John1", last_name="Smith1", email="john1@example.com"
        )
        book1 = Books.objects.create(name="Book1", reporter=cls.reporter)
        book2 = Books.objects.create(name="Book2", reporter=cls.reporter)

        author1 = Author.objects.create(name="Author1")
        author2 = Author.objects.create(name="Author2")
        author3 = Author.objects.create(name="Author3")

        book1.author.add(author1)
        book1.author.add(author2)

        book2.author.add(author2)
        book2.author.add(author3)

    def test_many_to_one_one_model(self):
        with self.assertWarnsMessage(
            PrefetchUnusedWarning, expected_message="Expected fields : author"
        ):
            list(self.reporter.books_set.values("author"))

    def test_many_to_one_two_models(self):
        with self.assertWarnsMessage(
            PrefetchUnusedWarning,
            expected_message="Expected fields : author, publisher",
        ):
            list(self.reporter.books_set.values("author", "publisher"))

    def test_many_to_one_without_prefetch_related(self):
        self.assertIsNotNone(list(self.reporter.books_set.all()))

    def test_many_to_many_one_model(self):
        with self.assertWarnsMessage(
            PrefetchUnusedWarning, expected_message="Expected fields : author"
        ):
            list(Books.objects.values("author"))

    def test_many_to_many_two_models(self):
        with self.assertWarnsMessage(
            PrefetchUnusedWarning,
            expected_message="Expected fields : author, publisher",
        ):
            list(Books.objects.values("author", "publisher"))

    def test_many_to_many_without_prefetch_related(self):
        self.assertIsNotNone(list(Books.objects.all()))

    def test_many_to_many_with_custom_manager_one_model(self):
        with self.assertWarnsMessage(
            PrefetchUnusedWarning, expected_message="Expected fields : author"
        ):
            list(Books.objects.get_author())

    def test_manipulate_manager(self):
        list(DjangoModel.objects.values("book"))

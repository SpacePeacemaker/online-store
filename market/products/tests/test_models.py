from datetime import timedelta

from accounts.models import User
from django.test import TestCase
from django.utils import timezone
from products.models import (
    Product,
    Detail,
    ProductDetail,
    Category,
    Banner,
    Review,
    ProductImage,
    ProductsViews,
    DiscountSet,
    DiscountProduct,
)


class ProductModelTest(TestCase):
    """Класс тестов модели Продукт"""

    @classmethod
    def setUpTestData(cls):
        cls.detail = Detail.objects.create(name="тестовая характеристика")
        cls.product = Product.objects.create(
            name="Тестовый продукт",
        )
        cls.product.details.set([cls.detail])

    def test_verbose_name(self):
        product = ProductModelTest.product
        field_verboses = {
            "name": "наименование",
            "details": "характеристики",
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(product._meta.get_field(field).verbose_name, expected_value)

    def test_name_max_length(self):
        product = ProductModelTest.product
        max_length = product._meta.get_field("name").max_length
        self.assertEqual(max_length, 512)


class DetailModelTest(TestCase):
    """Класс тестов модели Свойство продукта"""

    @classmethod
    def setUpClass(cls):
        cls.detail = Detail.objects.create(name="тестовая характеристика")

    @classmethod
    def tearDownClass(cls):
        cls.detail.delete()

    def test_verbose_name(self):
        detail = DetailModelTest.detail
        field_verboses = {
            "name": "наименование",
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(detail._meta.get_field(field).verbose_name, expected_value)

    def test_name_max_length(self):
        detail = DetailModelTest.detail
        max_length = detail._meta.get_field("name").max_length
        self.assertEqual(max_length, 512)


class ProductDetailModelTest(TestCase):
    """Класс тестов модели Значение свойства продукта"""

    @classmethod
    def setUpClass(cls):
        cls.detail = Detail.objects.create(name="тестовая характеристика")
        cls.product = Product.objects.create(
            name="Тестовый продукт",
        )
        cls.product_detail = ProductDetail.objects.create(
            product=cls.product,
            detail=cls.detail,
            value="тестовое значение характеристики",
        )

    @classmethod
    def tearDownClass(cls):
        cls.product.delete()
        cls.detail.delete()
        cls.product_detail.delete()

    def test_verbose_name(self):
        product_detail = ProductDetailModelTest.product_detail
        field_verboses = {
            "value": "значение",
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(product_detail._meta.get_field(field).verbose_name, expected_value)

    def test_value_max_length(self):
        product_detail = ProductDetailModelTest.product_detail
        max_length = product_detail._meta.get_field("value").max_length
        self.assertEqual(max_length, 128)


class CategoryTest(TestCase):
    """
    Класс тестов модели Категория
    """

    fixtures = ["05-categories.json"]

    def test_assert_expected_num_of_categories(self):
        self.assertEqual(Category.objects.count(), 12)


class BannerModelTest(TestCase):
    """Класс тестов модели Banner"""

    @classmethod
    def setUpClass(cls):
        """Создание продукта и баннера с ним"""

        cls.product = Product.objects.create(
            name="Тестовый продукт",
        )
        cls.banner = Banner.objects.create(product=cls.product, image="...static/img/content/home/slider.png")

    @classmethod
    def tearDownClass(cls):
        """Удаление сущности продукта и баннера"""

        cls.product.delete()
        cls.banner.delete()

    def test_verbose_name(self):
        """Тестирование валидности имени поля модели"""

        banner = self.banner
        field_verboses = {
            "image": "изображение",
        }

        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(banner._meta.get_field(field).verbose_name, expected_value)


class ReviewModelTest(TestCase):
    """Класс тестов модели Review"""

    @classmethod
    def setUpClass(cls):
        """Создание пользователя, продукта и отзыва к нему"""

        cls.user = User.objects.create_user(email="user@email.ru", password="qwerty")
        cls.product = Product.objects.create(
            name="Тестовый продукт",
        )
        cls.review = Review.objects.create(
            product=cls.product,
            user=cls.user,
            text="Тестовый отзыв",
        )

    @classmethod
    def tearDownClass(cls):
        """Удаление сущности пользователя, продукта и отзыва"""

        cls.user.delete()
        cls.product.delete()
        cls.review.delete()

    def setUp(self):
        """Логин пользователя"""

        self.client.force_login(self.user)

    def test_verbose_name(self):
        """Тестирование валидности имени поля модели"""

        field_verboses = {
            "product": "Продукт",
            "user": "Пользователь",
            "text": "Отзыв",
        }

        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(self.review._meta.get_field(field).verbose_name, expected_value)

    def test_text_max_length(self):
        """Тестирование максимально доступной длины поля text"""

        max_length = Review._meta.get_field("text").max_length
        self.assertEqual(max_length, 3000)


class ProductImageTest(TestCase):
    """
    Класс тестов модели Изображения продуктов
    """

    fixtures = ["05-categories.json", "06-products.json", "11-product-images.json"]

    def test_assert_expected_num_of_categories(self):
        self.assertEqual(ProductImage.objects.count(), 82)


class ProductsViewsTest(TestCase):
    """Класс тестов модели ProductsViews"""

    fixtures = [
        "01-users.json",
        "05-categories.json",
        "06-products.json",
        "19-products-views.json",
    ]

    def test_verbose_name(self):
        """Тестирование валидности имени поля модели"""
        views = ProductsViews.objects.first()

        field_verboses = {
            "product": "Продукт",
            "user": "Пользователь",
        }

        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(views._meta.get_field(field).verbose_name, expected_value)

    def test_assert_expected_num_of_views(self):
        """Тестирование количества просмотров"""

        self.assertTrue(ProductsViews.objects.count() > 5)


class DiscountProductTest(TestCase):
    """Класс тестов модели DiscountProduct"""

    fixtures = [
        "06-products.json",
        "discount-products.json",
    ]


class DiscountSetTest(TestCase):
    """Класс тестов модели DiscountSet"""

    def setUp(self):
        self.category1 = Category.objects.create(name="Category 1")
        self.category2 = Category.objects.create(name="Category 2")

        self.discount_set = DiscountSet.objects.create(
            percentage=10, start_date=timezone.now().date(), end_date=timezone.now().date() + timedelta(days=7)
        )

        self.discount_set.categories.add(self.category1, self.category2)

    def tearDown(self):
        self.category1.delete()
        self.category2.delete()
        self.discount_set.delete()

    def test_discount_set_categories(self):
        self.assertEqual(self.discount_set.categories.count(), 2)
        self.assertIn(self.category1, self.discount_set.categories.all())
        self.assertIn(self.category2, self.discount_set.categories.all())

    def test_discount_set_creation(self):
        self.assertIsInstance(self.discount_set, DiscountSet)
        self.assertEqual(self.discount_set.percentage, 10)

    def test_discount_set_active(self):
        self.assertTrue(self.discount_set.is_active())

    def test_discount_set_inactive(self):
        self.discount_set.end_date = self.discount_set.start_date - timedelta(days=1)
        self.discount_set.save()
        self.assertFalse(self.discount_set.is_active())


class DiscountProductTestCase(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="Test Product")
        self.discount_product = DiscountProduct.objects.create(
            percentage=20, start_date=timezone.now().date(), end_date=timezone.now().date() + timedelta(days=7)
        )
        self.discount_product.products.add(self.product)

    def tearDown(self):
        self.product.delete()
        self.discount_product.delete()

    def test_is_active(self):
        """Проверяем, что активная скидка возвращает True"""
        today = timezone.now().date()
        self.discount_product.start_date = today - timedelta(days=1)
        self.discount_product.end_date = today + timedelta(days=1)
        self.discount_product.save()
        self.assertTrue(self.discount_product.is_active())

    def test_products(self):
        """Проверяем, что продукты добавлены к скидке"""
        self.assertEqual(self.discount_product.products.count(), 1)
        self.assertEqual(self.discount_product.products.first(), self.product)

from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpRequest

from products.models import Product, Review

User = get_user_model()


class ReviewsService:
    """Сервис для работы с отзывами"""

    def __init__(self, request: HttpRequest, product: Product):
        self.request = request
        self.product = product

    def get_reviews_for_product(self):
        """
        Возвращает отзывы о выбранном товаре
        :return: пагинатор
        """

        reviews = Review.objects.filter(product=self.product).order_by("product_id")
        paginator = Paginator(reviews, 3)
        page = self.request.GET.get("page")

        try:
            reviews = paginator.page(page)
        except PageNotAnInteger:
            reviews = paginator.page(1)
        except EmptyPage:
            reviews = paginator.page(paginator.num_pages)

        if reviews.has_next():
            next_page: int = paginator.get_page(page).next_page_number()
            has_next: bool = True
        else:
            next_page: int = 1
            has_next: bool = False

        return reviews, next_page, has_next

    def get_reviews_count(self) -> int:
        """
        Возвращает количество отзывов о выбранном товаре
        :return: число отзывов
        """

        reviews_count = Review.objects.filter(product=self.product).count()
        return reviews_count

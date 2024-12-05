from django.db.models import Manager

from ..queryset import CategoryQuerySet


class CategoryDataAccessLayer(Manager):
    """
    Tutorial Data Access Layer
    """

    def get_queryset(self):
        """
        Override the default get_queryset method to return a TutorialQuerySet instance.

        This method ensures that any query made using this manager will utilize
        the custom methods and properties defined in the TutorialQuerySet.
        """
        return CategoryQuerySet(self.model, using=self._db)

    def annotate_total_tutorials(self):
        """
        Annotates each category with the total number of tutorials in that category.

        This method uses Django's Count aggregation function to count the number
        of tutorials associated with each category. The resulting queryset will have
        an additional attribute 'total_tutorials' for each category object, which
        indicates the count of tutorials in that category.
        """
        return self.get_queryset().annotate_total_tutorials()

    def filter_published(self, is_published=True):
        """
        Filters categories based on their active status.
        """
        return self.get_queryset().filter_published(is_published)

    def filter_published_tutorials(self, is_published=True):
        """
        Prefetches related tutorials for each category in the queryset.
        """
        return self.get_queryset().filter_published_tutorials(is_published)

    def join_tutorials(self):
        """
        Excludes categories that are only associated with
        inactive or discontinued tutorials.
        """
        return self.get_queryset().join_tutorials()

    def exclude_unpublished_tutorials(self) -> "QuerySet":
        """
        Excludes categories that are only associated with
        inactive or discontinued tutorials.
        """
        return self.get_queryset().exclude_unpublished_tutorials()

    def filter_recent_categories(self, num_categories=5, obj=None):
        """
        Retrieves a specified number of the most recently created categories.
        If 'obj' is provided, it excludes that object from the results.
        """
        return self.get_queryset().filter_recent_categories(num_categories, obj)

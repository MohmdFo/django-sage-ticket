from datetime import timedelta

from django.db.models import Count, Max, Q, QuerySet
from django.utils import timezone


class TagQuerySet(QuerySet):
    """
    A custom QuerySet for Tag model, providing specialized querying capabilities for
    tags. This class extends Django's QuerySet, adding methods that are specific to
    handling and analyzing tags in relation to associated tutorials.
    """

    def filter_recent_tags(self, days_ago=30, limit=None, obj=None) -> QuerySet:
        """
        Filter tags that have been used in tutorials within the specified number of days.
        If 'obj' is provided, it excludes that object from the results.
        """
        if not isinstance(days_ago, int) or days_ago < 0:
            raise ValueError("`days_ago` must be a non-negative integer")

        if limit is not None and (not isinstance(limit, int) or limit <= 0):
            raise ValueError("`limit` must be a positive integer or None")

        if days_ago == 0:
            qs = self.annotate(latest_tutorial_date=Max("tutorials__created_at")).order_by(
                "-latest_tutorial_date"
            )
        else:
            recent_date = timezone.now() - timedelta(days=days_ago)
            qs = self.filter(tutorials__created_at__gte=recent_date).distinct()

        if obj:
            qs = qs.exclude(Q(pk=obj.pk))

        if limit is not None:
            qs = qs[:limit]

        return qs

    def filter_trend_tags(self, days_ago=30, min_count=5, limit=None) -> QuerySet:
        """
        Filters and retrieves tags based on their usage frequency in tutorials,
        identifying trending tags either within a specific timeframe or overall.

        This method functions differently based on the 'days_ago' parameter:
        - If 'days_ago' is zero, it identifies trending tags regardless of the time
        frame, ranking them by their total usage count in tutorials.
        - If 'days_ago' is greater than zero, it filters tags used more than 'min_count'
        times in the specified number of days before the current date.

        An optional 'limit' parameter allows controlling the maximum number of tags
        returned.

        Args:
            days_ago (int): The number of days to look back for identifying trends. If
                            zero, trends are identified based on total usage count.
            min_count (int): The minimum number of times a tag must be used to be
                            considered  trending within the specified timeframe.
            limit (int, optional): The maximum number of tags to return. If None, no
                                    limit is applied.

        Examples:
            - To get overall trending tags with no time restriction:
            >>> trending_tags = Tag.objects.filter_trend_tags(days_ago=0)

            - To get tags that are trending in the last 7 days, used at least 10 times:
            >>> weekly_trends = Tag.objects.filter_trend_tags(days_ago=7, min_count=10)

            - To get the top 5 overall trending tags:
            >>> top_tags = Tag.objects.filter_trend_tags(days_ago=0, limit=5)

            - To get the top 3 trending tags in the last 30 days:
            >>> monthly = Tag.objects.filter_trend_tags(days_ago=30, min_count=5, limit=3)
        """
        if not isinstance(days_ago, int) or days_ago < 0:
            raise ValueError("`days_ago` must be a non-negative integer")

        if not isinstance(min_count, int) or min_count <= 0:
            raise ValueError("`min_count` must be a positive integer")

        if limit is not None and (not isinstance(limit, int) or limit <= 0):
            raise ValueError("`limit` must be a positive integer or None")

        if days_ago == 0:
            qs = (
                self.annotate(total_count=Count("tutorials"))
                .filter(total_count__gte=min_count)
                .order_by("-total_count")
            )
        else:
            recent_date = timezone.now() - timedelta(days=days_ago)
            qs = self.annotate(
                recent_count=Count(
                    "tutorials", filter=Q(tutorials__created_at__gte=recent_date)
                )
            ).filter(recent_count__gte=min_count)

        if limit is not None:
            qs = qs[:limit]

        return qs

    def annotate_total_tutorials(self) -> QuerySet:
        """
        Annotates each tag with the total number of tutorials in that tag.

        This method uses Django's Count aggregation function to count the number
        of tutorials associated with each tag. The resulting queryset will have
        an additional attribute 'total_tutorials' for each tag object, which
        indicates the count of tutorials in that tag.
        """
        published_tutorials = self.filter_published_tutorials()
        qs = published_tutorials.annotate(total_tutorials=Count("tutorials"))
        return qs

    def filter_published(self, is_published: bool = True):
        """
        Filters categories based on their published status.
        """
        qs = self.filter(is_published=is_published)
        return qs

    def filter_published_tutorials(self, is_published: bool = True):
        """
        Prefetches related tutorials for each tag in the queryset.
        """
        published_tutorials_condition = Q(tutorials__is_published=is_published)
        published = self.filter_published()
        qs = published.filter(published_tutorials_condition)
        return qs

    def search(self, search_term) -> QuerySet:
        """
        Performs a case-insensitive search for tags based on their name.
        """
        qs = self.filter(title__icontains=search_term)
        return qs

    def filter_by_tutorials_category(self, category_title) -> QuerySet:
        """
        Filters tags based on the category of associated tutorials.
        """
        qs = self.filter(tutorials__category__title=category_title).distinct()
        return qs

    def exclude_unpublished_tutorials(self) -> QuerySet:
        """
        Excludes tags that are only associated with inactive or discontinued tutorials.
        """
        qs = self.filter(tutorials__is_published=True)
        return qs

    def sort_by_popularity(self) -> QuerySet:
        """
        Sorts tags based on the number of tutorials associated with each, in descending
        order.
        """
        qs = self.annotate(tutorials_count=Count("tutorials")).order_by("-tutorials_count")
        return qs

    def filter_by_tutorial_date_range(self, start_date, end_date) -> QuerySet:
        """
        Filters tags based on the publication date range of the associated tutorials.
        """
        return self.filter(tutorials__created_at__range=(start_date, end_date)).distinct()

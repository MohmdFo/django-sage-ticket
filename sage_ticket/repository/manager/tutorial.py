from django.db.models import Manager

from ..queryset.tutorial import TutorialQuerySet


class TutorialDataAccessLayer(Manager):
    """
    Tutorial Data Access Layer
    """

    def get_queryset(self):
        """
        Override the default get_queryset method to return a TutorialQuerySet instance.

        This method ensures that any query made using this manager will utilize
        the custom methods and properties defined in the TutorialQuerySet.
        """
        return TutorialQuerySet(self.model, using=self._db)

    def filter_actives(self, is_published=True):
        """
        Returns a queryset of tutorials filtered by their active status.
        """
        return self.get_queryset().filter_actives(is_published)

    def filter_recent_tutorials(self, num_tutorials=5, obj=None):
        """
        Retrieves a specified number of the most recently created tutorials.
        If 'obj' is provided, it excludes that object from the results.
        """
        return self.get_queryset().filter_recent_tutorials(num_tutorials=num_tutorials, obj=obj)

    def filter_by_category(self, category_slug):
        """
        Filters tutorials by a given category slug.
        """
        return self.get_queryset().filter_by_category(category_slug=category_slug)

    def filter_by_tag(self, tag_slug):
        """
        Filters tutorials by a given tag slug.
        """
        return self.get_queryset().filter_by_tag(tag_slug=tag_slug)

    def filter_in_date_range(self, start_date, end_date):
        """
        Filters tutorials created within a specified date range.
        """
        return self.get_queryset().filter_in_date_range(start_date, end_date)

    def filter_new_tutorials(self, days=7):
        """
        Fetches tutorials that are considered 'new', i.e., created within the specified
        number of recent days.
        """
        return self.get_queryset().filter_new_tutorials(days)

    def annotate_total_tags(self):
        """
        Annotates each tutorial in the queryset with the count of its associated tags.
        """
        return self.get_queryset().annotate_total_tags()

    def annotate_published_since(self):
        """
        Annotates each tutorial in the queryset with the number of days since it was
        published.
        """
        return self.get_queryset().annotate_published_since()

    def annotate_is_recent(self):
        """
        Annotates each tutorial in the queryset with a boolean indicating if it is recent
        (created within the last 7 days).
        """
        return self.get_queryset().annotate_is_recent()

    def full_text_search(self, search_query):
        """
        Performs a full-text search on 'title' and 'description' fields of the tutorials.
        This method is optimized for finding complete words or phrases, not partial
        substrings.
        """
        return self.get_queryset().full_text_search(search_query)

    def substring_search(self, search_query):
        """
        Performs a case-insensitive substring search in 'title' and 'description'
        fields of the tutorials. This method is useful for partial word matching, but it is
        less efficient than full-text search.
        """
        return self.get_queryset().substring_search(search_query)

    def trigram_similarity_search(self, search_query):
        """
        Performs a search using trigram similarity on 'title' and 'description' fields
        of the tutorials.
        This method supports partial word matches and is more linguistically aware than
        a simple substring search, but it requires TutorialgreSQL with pg_trgm extension.
        """
        return self.get_queryset().trigram_similarity_search(search_query)

    def heavy_search(self, search_query):
        """
        Combines full-text search, substring search, and trigram similarity search to
        provide a comprehensive search experience. The method first tries a full-text
        search. If it yields no results, it falls back to a substring search. If
        available and suitable, it also uses trigram similarity for nuanced matching.
        """
        return self.get_queryset().heavy_search(search_query)

    def join_category(self):
        return self.get_queryset().join_category()

    def join_tags(self):
        return self.get_queryset().join_tags()

    def annotate_next_and_prev(self):
        """
        Annotates each tutorial in the queryset with slugs of the next and previous tutorials
        in the same category.

        This method uses subqueries to determine the 'slug' of the
        next and previous tutorials based on their primary key (pk)
        within the same category. The result is the addition
        of two new fields to each tutorial object in the queryset:
        `next_tutorial_slug` and `prev_tutorial_slug`.
        """
        return self.get_queryset().annotate_next_and_prev()

from django.utils import timezone
from posts.serializers import PostSerializer
import json


class FeedAlgorithm:
    def __init__(self, user):
        self.user = user

    def get_feed(self):
        # Step 1: Gather Data
        user_following = self.user.following.all()

        # Step 2: Determine Relevance Factors
        # Consider factors like recency, popularity, user interactions, etc.

        # Step 3: Design the Scoring Mechanism
        feed_items = []
        for following_user in user_following:
            posts = following_user.posts.all()
            for post in posts:
                # Calculate relevance score based on factors like recency, popularity, etc.
                relevance_score = self.calculate_relevance_score(post)
                feed_items.append((post, relevance_score))

        # Step 4: Sort the Feed Items based on Relevance Score
        sorted_feed = sorted(feed_items, key=lambda x: x[1], reverse=True)

        # Step 5: Personalization (Optional)
        # Apply personalization techniques based on user preferences and interactions

        # Step 6: Return the Feed
        feeds = [item[0] for item in sorted_feed]
        return feeds

    def calculate_relevance_score(self, post):
        # Implement your scoring logic here
        # Calculate the relevance score for a post based on different factors
        # Adjust the weights and calculations based on your specific requirements
        relevance_score = 0

        # Example: Consider recency and popularity
        time_difference = timezone.now().date() - post.created
        popularity_score = post.likes.count() + post.comment.count()

        # Weight the factors and calculate the relevance score
        relevance_score = (popularity_score * 0.6) + (time_difference.days * 0.4)

        return relevance_score

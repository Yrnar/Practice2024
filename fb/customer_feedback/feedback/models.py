from django.db import models

class Feedback(models.Model):
    RATING_CHOICES = [
        ('very bad', 'Very Bad'),
        ('very good', 'Very Good'),
    ]

    customer_name = models.CharField(max_length=100)
    rating = models.CharField(max_length=10, choices=RATING_CHOICES)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.customer_name} - {self.rating}'

from django.db import models

class UserCoursePurchase(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)  # Useful for subscriptions

    class Meta:
        unique_together = ('user', 'course')  # Prevent duplicate purchases
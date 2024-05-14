from django.db import models
from django.utils import timezone

class ChatHistory(models.Model):
    input = models.CharField(max_length=255)  # 用户输入
    result = models.TextField()  # 返回的结果
    execution_time = models.DateTimeField(default=timezone.now)  # 执行时间
    is_valid = models.BooleanField(default=False)  # 输入是否有效

    def __str__(self):
        return f"{self.input} - {self.result}"

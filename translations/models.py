from django.db import models

class Translation(models.Model):
    msgid = models.TextField()
    msgstr = models.TextField(blank=True)
    locations = models.TextField()
    fuzzy = models.BooleanField(default=False)
    source_file = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.msgid
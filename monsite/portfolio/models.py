from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    github_link = models.URLField(blank=True, null=True)
    hashtags = models.CharField(max_length=300, help_text="Sépare par des virgules")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='project_images/')

    def __str__(self):
        return f"Image for {self.project.title}"

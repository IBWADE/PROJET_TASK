from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class TypeTasks(models.Model):
    typetasks = (
        ('EOT','eot'),
        ('SGH','sgh'),
        ('R/I','r/i'),
        ('MFI','mfi'),
        ('TS','ts'),
        ('MOD','mod'),
        ('REP','rep'),
        ('INSP','isnp'),
        ('FOT','fot'),
        ('MEL','mel'),
    )
    singletask = models.CharField(max_length=100,choices=typetasks)

    def __str__(self):
        return self.singletask
    
class TypeActivities(models.Model):
    typeactivities = (
        ('Training','training'),
        ('Perform','perform'),
        ('Supervise','supervise'),
        ('CRS','crs')
    )
    singleactivity = models.CharField(max_length=15,choices=typeactivities)

    def __str__(self):
        return self.singleactivity
    

class maintenance(models.Model):
    privilegechoices = (
        ("B1","b1"),
        ("B2","b2")
    )
    date = models.DateField()
    location = models.CharField(max_length=300)
    actype = models.CharField(max_length=300)
    acregistration = models.CharField(max_length=250)
    typemaintenance = models.CharField(max_length=300)
    privilege = models.CharField(max_length=2,choices=privilegechoices,null=True)
    tasktype = models.ManyToManyField(TypeTasks,related_name="typetask",blank=True)
    activitytype = models.ManyToManyField(TypeActivities,related_name="typeact",blank=True)
    ata = models.IntegerField()
    operation = models.CharField(max_length=300)
    time = models.IntegerField()
    maintenanceref = models.CharField(max_length=300)
    remark = models.TextField(null=True)
    technicalrecorder = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.maintenanceref
    
class Post(models.Model):
    auteur = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    likes = models.ManyToManyField(User,related_name="likes",blank=True)
    photo = models.ImageField(upload_to="posts/",null=True,blank=True) 
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-id']

    def total_likes(self):
        return self.likes.count()

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    comment_content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}-{}'.format(self.post.titre_Post, str(self.user.username))

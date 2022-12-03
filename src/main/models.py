from django.db import models
#File model
 

# Create your models here.

class Author(models.Model):
    '''Author model
    
    Fields:
    - name: str - name of author
    - surname: str - surname of author
    - patronymic: str - patronymic of author
    - email: str - email of author
    - organization: str - organization of author
    - position: str - position of author
    - password: str - password of author

    '''

    fio = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    organization = models.CharField(max_length=100)
    position = models.CharField(max_length=99)

    def __str__(self):
        return self.fio 


class CoAuthor(models.Model):
    '''CoAuthor model
    
    Fields:
    - name: str - name of coauthor
    - surname: str - surname of coauthor
    - patronymic: str - patronymic of coauthor
    - email: str - email of coauthor
    - organization: str - organization of coauthor
    - position: str - position of coauthor

    '''

    fio = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    organization = models.CharField(max_length=100)
    position = models.CharField(max_length=100)

    def __str__(self):
        return self.fio

class Application(models.Model):
    ''' Заявка на участие в конкурсе 
    
    Fields:
    - id: int
    - email: str
    - heading: str
    - topic: str
    - annotation: str
    - file: File
    - main author: Author
    - coauthors: Author[]
    - status: ['new', 'accepted', 'rejected']
    - date: datetime
    - links: str[]
    - photo: File
    '''

    id = models.AutoField(primary_key=True)
    email = models.EmailField()
    heading = models.CharField(max_length=100) 
    topic = models.CharField(max_length=100)
    annotation = models.TextField()
    file = models.FileField(upload_to='files')
    main_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    coauthors = models.ManyToManyField(CoAuthor)
    # статусы заявки: новая, принята, отклонена
    status = models.CharField(max_length=10, default='new')
    date = models.DateTimeField(auto_now_add=True)
    # много ссылки на статьи
    links = models.TextField()
    photo = models.FileField(upload_to='photos')

    
    def __str__(self):
        return self.heading

    



    
    

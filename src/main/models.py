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
    email = models.EmailField(max_length=100, blank=True)
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
    - rating: int
    - votes: int

    '''

    id = models.AutoField(primary_key=True)
    email = models.EmailField()
    heading = models.CharField(max_length=100) 
    topic = models.CharField(max_length=100)
    annotation = models.TextField()
    file = models.FileField(upload_to='files')
    main_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    coauthors = models.ManyToManyField(CoAuthor, blank=True)
    # статусы заявки: новая, принята, отклонена
    # status = models.CharField(max_length=10, default='new')
    # либо new, либо accepted, либо rejected
    status = models.CharField(max_length=10, default='new', choices=[('new', 'Новая'), ('accepted', 'Одобрено'), ('rejected', 'Отклонено')])
    date = models.DateTimeField(auto_now_add=True)
    # много ссылки на статьи
    links = models.TextField(blank=True)
    photo = models.FileField(upload_to='photos', blank=True)

    rating = models.FloatField(blank=True, default=0)
    votes = models.IntegerField(blank=True , default=0)
    uid_antiplagiat = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.heading


class Expert(models.Model):
    '''Эксперт
    
    Fields:
    - id: int
    - fio: str
    - password: str
    - login: str


    '''

    id = models.AutoField(primary_key=True)
    fio = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    #уникальный логин
    login = models.CharField(max_length=100, default='', unique=True)

    def __str__(self):
        return self.fio



class Mark(models.Model):
    '''Оценки экспертов
    
    Fields:
    - id: int
    - name: str
    - type: str

    '''

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=300)
    # video or article or downgrade or upgrade
    type = models.CharField(max_length=100, choices=[('video', 'Видео'), ('article', 'Статья'), ('downgrade', 'Штраф', ), ('upgrade', 'Дополнительный балл')])


    def __str__(self):
        return self.name




class ExpertMark(models.Model):
    '''Оценки экспертов
    
    Fields:
    - id: int
    - application: Application
    - expert: Expert
    - mark: Mark
    - value: int

    '''

    id = models.AutoField(primary_key=True)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE)
    mark = models.ForeignKey(Mark, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    # от 1 до 10
    value = models.IntegerField()
    


    def __str__(self):
        return str(self.id)

class Stage(models.Model):
    '''Этапы
    
    Fields:
    - id: int
    - name: str
    - description: str
    - H: str
    - P: str

    '''

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10)
    description = models.TextField(max_length=30, blank=True)
    H = models.CharField(max_length=20, blank=True)
    P = models.CharField(max_length=20, blank=True)


    def __str__(self):
        return self.name + ' ' + self.description + ' ' + self.H + ' ' + self.P

class Contests(models.Model):
    '''Конкурсы
    
    Fields:
    - id: int
    - name: str
    - date: datetime
    - status: ['now', 'old', 'new']
    - stages: Stage[]
    - page_heading: str
    - heading_0: str
    - heading_1: str
    - heading_2: str
    - about_contest: str
    - participate_info: str
    - participate_info_available: bool
    - registration is available: bool
    - viewing works: bool
    - results: bool
    - uid_antiplagiat: str



    '''

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    # статусы конкурса: новый, старый, текущий
    status = models.CharField(max_length=10, default='new', choices=[('new', 'Новый'), ('old', 'Старый'), ('now', 'Текущий')])
    stages = models.ManyToManyField(Stage)
    page_heading = models.CharField(max_length=100, blank=True)
    heading_0 = models.CharField(max_length=100, blank=True)
    heading_1 = models.CharField(max_length=100, blank=True)
    heading_2 = models.CharField(max_length=100, blank=True)
    about_contest = models.TextField(blank=True)
    participate_info = models.TextField(blank=True)
    registration_is_available = models.BooleanField(default=False)
    viewing_works = models.BooleanField(default=False)
    results = models.BooleanField(default=False)

    participate_info_available = models.BooleanField(default=False)

    


    def __str__(self):
        return self.name + ' ' + self.status


from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect


#Модели из БД
from main.models import *
# Create your views here.

def index(request):


    stages = [
        { 'name': 'Этап 1', 'description': 'Ожидание объявления конкурса', 'H': 'до 15', 'P': 'сентября 2023', },
        { 'name': 'Этап 2', 'description': 'Подача заявок', 'H': 'до 1', 'P': 'ноября 2023', },
        { 'name': 'Этап 3', 'description': 'Экспертная оценка', 'H': 'до 10', 'P': 'ноября 2023', },
        { 'name': 'Этап 4', 'description': 'Объявление победителей', 'H': 'до 15', 'P': 'ноября 2023', },
    ]


    work = {
        'id': 1,
        'name': 'Какая-то работа',
    }

    works = [ w for i in range(10) for w in [work] ]

    result = {
        'place': 1,
        'name': 'Какая-то работа',
        'author': 'Иванов Иван Иванович',
        'coauthors': ['Петров Петр Петрович', 'Сидоров Сидор Сидорович'],
        'expert': '123',
        'guest': '123',
        'work_id': 123,
        }
    
    results = [ r for i in range(10) for r in [result] ]

    context = {
        'page_heading': 'Конкурс среди журналистов на соискание премий Губернатора Оренбургской области',
        'heading': ['Творческий конкурс', 'на соискание премий Губернатора Оренбургской области', 'среди журналистов, редакцийсредств массовой информации, полиграфических предприятий'],
        'participates': 'Лауреатами премий могут быть признаны журналисты печатных и электронных СМИ Оренбургской области, редакции СМИ, работающие в Оренбургской области, иные физические лица, осуществляющие деятельность в сфере журналистики в Оренбургской области, юридические лица, работающие в области полиграфии, зарегистрированные на территории Оренбургской области, ярко проявившие в своей работе объективность, беспристрастность, уважение к оппонентам, стремление правдиво и оперативно информировать население о происходящих событиях, профессионализм.',
        'about_contest': 'Губернатором Оренбургской области вручаются премии в следующих номинациях:\n1) "Журналист года" - 1 премия.\nПремия присуждается журналисту за особые достижения в профессиональной сфере: творческие работы, новаторство, эффективные акции. Премия присуждается решением конкурсного жюри. Заявки на участие в данной номинации не представляются;\n2) "Медиапроект года" - 1 премия.\nПремия присуждается издателю СМИ или редакции СМИ за реализацию проекта, посвященного Году культурного наследия народов России.\nВ номинации оцениваются оригинальность проекта, качество его воплощения и информационная составляющая, профессионализм исполнения, журналистское, операторское и режиссерское (для телевидения), фотомастерство (для печатных и интернет-изданий), декорации, дизайн;\n3) "Территория комфорта" - 1 премия.\nПремия присуждается журналисту или редакции СМИ за цикл материалов, отражающих тематику приоритетного проекта "Формирование комфортной городской среды";\n4) "Оренбуржье - сердце Евразии" - 1 премия.\nПремия присуждается журналисту или редакции СМИ за цикл материалов об Оренбургской области, о ее уникальности и роли в сфере евразийского сотрудничества.\nГубернатором Оренбургской области также вручается учрежденная им специальная премия.\nСпециальная премия Губернатора Оренбургской области присуждается решением конкурсного жюри журналисту или редакции СМИ за организацию и проведение творческой профессиональной акции, получившей широкий общественный резонанс и признание в профессиональном сообществе, за новаторские идеи и подходы. Заявки на соискание премии не представляются.',
        'stages': stages,
        'reg_enable': 1,
        'participate_enable': 1,
        'works': works,
        'results': results,

        }


    return render(request, 'landing.html', context=context)






def registration(request):
    if request.method == 'POST':


        form = request.POST 

        print(form)

        files = request.FILES

        print(files)

        print(files['file'])

        #email
        if 'email' in form:
            email = form['email']
        else: return HttpResponse('error email')

        #password
        if 'password' in form:
            password = form['password']
        else: return HttpResponse('error password')

        #fio
        if 'fio' in form:
            fio = form['fio']
        else: return HttpResponse('error fio')

        #organization
        if 'org' in form:
            org = form['org']
        else: return HttpResponse('error org')

        #position
        if 'pos' in form:
            pos = form['pos']
        else: return HttpResponse('error pos')

        #topic
        if 'topic' in form:
            topic = form['topic']
        else: return HttpResponse('error topic')

        #annotation
        if 'annotation' in form:
            annotation = form['annotation']
        else: return HttpResponse('error email')

        #heading
        if 'heading' in form:
            heading = form['heading']
        else: return HttpResponse('error head')

        #link
        if 'link' in form:
            links = form.getlist('link')

        #coauthors
        coauthors = []
        if 'fio2' in form and 'org2' in form and 'pos2' in form:
            fios = form.getlist('fio2')
            orgs = form.getlist('org2')
            poss = form.getlist('pos2')
            print(fios)
            print(orgs)
            print(poss)

            

            for i in range(len(fios)-1):
                coauthors.append({'fio': fios[i], 'org': orgs[i], 'pos': poss[i]})

        #file
        if 'file' in files:
            file_ = files['file']
        else: return HttpResponse('error file')

        #photo
        if 'photo' in files:
            photo = files['photo']
        else: photo = ''

        #check if email is unique
        # if Author.objects.filter(email=email).exists():
        #     return HttpResponse('error email 2')
        
        

        #Сохраняем файл
        # fs = FileSystemStorage()
        # filename = fs.save('', file_)




        #create author
        author = Author.objects.create(email=email, password=password, fio=fio, organization=org, position=pos)

        #create coauthors
        coauthors_ = []
        for coauthor in coauthors:
            coauthors_.append(CoAuthor.objects.create(fio=coauthor['fio'], organization=coauthor['org'], position=coauthor['pos']))
        



        #create Application
        if photo:
            application = Application.objects.create(
            email=email, heading=heading, topic=topic, annotation=annotation, file=file_, main_author=author,
            photo=photo, links=links, status='new')
        
        else:
            application = Application.objects.create(
            email=email, heading=heading, topic=topic, annotation=annotation, file=file_, main_author=author,
            links=links, status='new')

        #add coauthors
        for coauthor in coauthors_:
            application.coauthors.add(coauthor)

        return redirect('/login')
    else:
        return render(request, 'registration.html')



def login(request):

    if request.method == 'POST':
        form = request.POST
        email = form['login']
        login = form['login']
        password = form['password']
        if Author.objects.filter(email=email, password=password).exists():
            author = Author.objects.get(email=email, password=password)
            
            request.session['login'] = 1
            request.session['account_type'] = 'author'
            request.session['author_id'] = author.id
            return redirect('/lk')
        else:
            return HttpResponse('error')
    else:
        return render(request, 'login.html')

def logout(request):
    request.session['login'] = 0
    request.session['account_type'] = ''
    request.session['author_id'] = ''
    return redirect('/')

def work(request, id):
    work = Application.objects.get(id=id)

    #соавторы
    coauthors = []
    for coauthor in work.coauthors.all():
        coauthors.append(coauthor)

    print(work.main_author)

    context = {
        'work': work,
        'coauthors': coauthors,
        'is_video': work.file.name.split('.')[-1] == 'mp4' or work.file.name.split('.')[-1] == 'avi',
    }
    
    

    return render(request, 'work.html', context=context)

def lk(request):
    if request.session['login'] == 1:
        if request.session['account_type'] == 'author':
            return redirect('/lk/work')
    else:
        return redirect('/login')

def lk_work(request):

    if 'login' in request.session and request.session['login'] == 1:
        if request.session['account_type'] == 'author':
            author = Author.objects.get(id=request.session['author_id'])
            works = Application.objects.filter(main_author=author)
            info = {'fio': author.fio, 'email': author.email, 'org': author.organization, 'pos': author.position, 'ap_id': works[0].id}
            
            result = []

            context = {
                'info': info,
                'result': result,
            }
            return render(request, 'participant.html', context=context)
        else:
            return HttpResponse('error')
    else:
        return redirect('/login')

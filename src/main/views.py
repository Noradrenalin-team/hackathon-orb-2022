from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
import traceback


#Модели из БД
from main.models import *
# Create your views here.

def index(request):

    #конкурс который сейчас идет
    contest = Contests.objects.filter(status='now').first()


    stages = contest.stages.all()

    results = []
    if contest.results:
            works = Application.objects.all()
            works_dict = []
            

            for work in works:
                work_dict = {
                    'id': work.id,
                    'guest' : work.rating,
                }

                all_work_marks = ExpertMark.objects.filter(application=work)
                
                print(all_work_marks)

                marks_dict = {}
                marks_down_dict = {}
                marks_up_dict = {}

                for mark in all_work_marks:
                    mark_type = mark.mark.type
                    if mark_type == 'upgrade':
                        if mark.mark.id in marks_up_dict:
                            marks_up_dict[mark.mark.id].append( mark.value )
                        else:
                            marks_up_dict[mark.mark.id] = [mark.value]
                    elif mark_type == 'downgrade':
                        if mark.mark.id in marks_down_dict:
                            marks_down_dict[mark.mark.id].append( mark.value )
                        else:
                            marks_down_dict[mark.mark.id] = [mark.value]
                    else:
                        if mark.mark.id in marks_dict:
                            marks_dict[mark.mark.id].append( mark.value )
                        else:
                            marks_dict[mark.mark.id] = [mark.value]
            
                print(marks_dict) 
                print(marks_down_dict)
                print(marks_up_dict)

                #считаем среднее значение оценок
                for key in marks_dict:
                    marks_dict[key] = sum(marks_dict[key])/len(marks_dict[key])
                for key in marks_down_dict:
                    marks_down_dict[key] = sum(marks_down_dict[key])/len(marks_down_dict[key])
                for key in marks_up_dict:
                    marks_up_dict[key] = sum(marks_up_dict[key])/len(marks_up_dict[key])

                print(marks_dict)
                print(marks_down_dict)
                print(marks_up_dict)

                #считаем итоговую оценку
                rating = 0
                for key in marks_dict:
                    rating += marks_dict[key]
                for key in marks_down_dict:
                    rating -= marks_down_dict[key]
                for key in marks_up_dict:
                    rating += marks_up_dict[key]

                print(rating)

                work_dict['expert'] = rating

                work_dict['info'] = work.heading+', ' + work.main_author.fio

                

                works_dict.append(work_dict)

            #сортируем по рейтингу
            works_dict = sorted(works_dict, key=lambda k: k['expert'], reverse=True)

            #присваиваем места
            for i in range(len(works_dict)):
                works_dict[i]['place'] = i+1

            results = works_dict
        


    context = {
        'page_heading': contest.page_heading,
        'about_contest': contest.about_contest,
        'heading': [contest.heading_0, contest.heading_1, contest.heading_2],
        'participates': contest.participate_info,
        'stages': stages,
        'reg_enable': contest.registration_is_available,
        'participate_enable': contest.participate_info_available,
        'works': [],
        'results': results,
        }


    #все работы со статусом "принято"

    if contest.viewing_works:
        all_works = Application.objects.filter(status='accepted')

        works = []
        for work in all_works:
            name = work.heading
            annotation = work.annotation

            if len(annotation) > 95:
                annotation = annotation[:95] + '...'
            w = {'id': work.id, 'name': name, 'annotation': annotation}
            if work.photo:
                w['photo'] = work.photo
            works.append(w)

        context['works'] = works

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
        
        elif Expert.objects.filter(login=login, password=password).exists():
            expert = Expert.objects.get(login=login, password=password)
            request.session['login'] = 1
            request.session['account_type'] = 'expert'
            request.session['expert_id'] = expert.id
            return redirect('/lk')

        #вход админа

        elif User.objects.filter(username=login).exists() and check_password(password, User.objects.get(username=login).password):
            user = User.objects.get(username=login)

            if user.is_superuser:
                request.session['login'] = 1
                request.session['account_type'] = 'admin'
                return redirect('/lk/result')

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

    if request.POST:
        form = request.POST.copy()
        del form['csrfmiddlewaretoken']
        print(form)

        voute = int(list(form.keys())[0])
        print(voute)

        request.session['voute'] = 1
        request.session[id] = voute

        work = Application.objects.get(id=id)

        if work.rating == 0:
            work.rating = voute
            work.votes = 1
        else:
            work.votes = work.votes + 1
            work.rating = work.rating + voute

        work.save()

        return redirect('/work/' + str(id))


    try:
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
        
        # голосование
        context['voute'] = 1
        print(dict(request.session))

        if 'voute' in request.session:
            print('voute')
            if str(id) in request.session:
                print('id')
                context['c'] = {request.session[str(id)]: 'red'}
                context['voute'] = 0
                print(context)


        return render(request, 'work.html', context=context)
    except Exception as e:
        #404
        print(e)
        print(traceback.format_exc())
        print('error')

        return HttpResponse('404')

def lk(request):
    if 'login' in request.session:
        if request.session['login'] == 1:
            if 'account_type' in request.session and request.session['account_type'] == 'author':
                return redirect('/lk/work')
            elif 'account_type' in request.session and request.session['account_type'] == 'expert':
                return redirect('/lk/works')
            elif 'account_type' in request.session and request.session['account_type'] == 'admin':
                return redirect('/lk/result')
            else:
                return HttpResponse('error')
    
        else:return redirect('/login')
    else:return redirect('/login')

def lk_work(request):

    if 'login' in request.session and request.session['login'] == 1:
        if request.session['account_type'] == 'author':
            author = Author.objects.get(id=request.session['author_id'])
            works = Application.objects.filter(main_author=author)
            info = {'fio': author.fio, 'email': author.email, 'org': author.organization, 'pos': author.position, 'ap_id': works[0].id}
            
            result = []
            result_down = []
            result_up = []

            print('до')
            all_work_marks = ExpertMark.objects.filter(application=works[0])
            print('после')
            if all_work_marks:
                print('1342353456346356')
                print(all_work_marks)

                marks_dict = {}
                marks_down_dict = {}
                marks_up_dict = {}

                for mark in all_work_marks:
                    mark_type = mark.mark.type
                    if mark_type == 'upgrade':
                        if mark.mark.id in marks_up_dict:
                            marks_up_dict[mark.mark.id].append( mark.value )
                        else:
                            marks_up_dict[mark.mark.id] = [mark.value]
                    elif mark_type == 'downgrade':
                        if mark.mark.id in marks_down_dict:
                            marks_down_dict[mark.mark.id].append( mark.value )
                        else:
                            marks_down_dict[mark.mark.id] = [mark.value]
                    else:
                        if mark.mark.id in marks_dict:
                            marks_dict[mark.mark.id].append( mark.value )
                        else:
                            marks_dict[mark.mark.id] = [mark.value]
            
                print(marks_dict) 
                print(marks_down_dict)
                print(marks_up_dict)

                #считаем среднее значение оценок
                for key in marks_dict:
                    marks_dict[key] = sum(marks_dict[key])/len(marks_dict[key])
                for key in marks_down_dict:
                    marks_down_dict[key] = sum(marks_down_dict[key])/len(marks_down_dict[key])
                for key in marks_up_dict:
                    marks_up_dict[key] = sum(marks_up_dict[key])/len(marks_up_dict[key])

                print(marks_dict)
                print(marks_down_dict)
                print(marks_up_dict)

                #считаем итоговую оценку
                rating = 0
                for key in marks_dict:
                    rating += marks_dict[key]
                for key in marks_down_dict:
                    rating -= marks_down_dict[key]
                for key in marks_up_dict:
                    rating += marks_up_dict[key]

                print(rating)
                print('fdfdhdhfghdfhdfh')
                for r in marks_dict:
                    result.append({'name': Mark.objects.get(id=r).name, 'value': marks_dict[r]})
                for r in marks_down_dict:
                    result_down.append({'name': Mark.objects.get(id=r).name, 'value': marks_down_dict[r]})
                for r in marks_up_dict:
                    result_up.append({'name': Mark.objects.get(id=r).name, 'value': marks_up_dict[r]})
                print('gggggggggggggggggggggggggg')
            context = {
                'info': info,
                'result': result,
                'result_down': result_down,
                'result_up': result_up,
                'rating': rating,
            }
            return render(request, 'participant.html', context=context)
        else:
            return HttpResponse('error')
    else:
        return redirect('/login')


def lk_works(request):
    print('lk_works')
    if 'login' in request.session and request.session['login'] == 1:
        print('login')
        if request.session['account_type'] == 'expert':
            print('expert')
                #все одобренные работы
            works = Application.objects.filter(status='accepted')

            print(works)



            result = []

            w_none = []
            w_done = []
            w_wait = []
    
            for work in works:
                print('work')
                
                #узнаём тип работы
                if work.file.name.split('.')[-1] == 'mp4' or work.file.name.split('.')[-1] == 'avi':
                    work_type = 'video'
                else:
                    work_type = 'article'
                #получаем все ExpertMark работы
                marks = ExpertMark.objects.filter(application=work)

                if work_type == 'video':
                    #все критерии для видео работ
                    video_criteria_ = Mark.objects.filter(type='video')
                    video_criteria = []
                    for criteria in video_criteria_: video_criteria.append(criteria.name)
                    #оценки этой работы экспертом
                    marks = ExpertMark.objects.filter(application=work, expert=Expert.objects.get(id=request.session['expert_id'])) 

                    #слоаврь оценок
                    marks_dict = {}
                    for mark in marks: marks_dict[mark.mark.name] = mark.value

                    if len(marks_dict) >= len(Mark.objects.all()) - len(Mark.objects.filter(type='article')):
                        w_done.append(work)
                    elif len(marks) == 0:
                        w_none.append(work)
                    else:
                        w_wait.append(work)

                elif work_type == 'article':
                    #все критерии для статьи
                    article_criteria_ = Mark.objects.filter(type='article')
                    article_criteria = []
                    for criteria in article_criteria_: article_criteria.append(criteria.name)
                    #оценки этой работы экспертом
                    marks = ExpertMark.objects.filter(application=work, expert=Expert.objects.get(id=request.session['expert_id'])) 

                    #слоаврь оценок
                    marks_dict = {}
                    for mark in marks: marks_dict[mark.mark.name] = mark.value

                    if len(marks_dict) >= len(Mark.objects.all()) - len(Mark.objects.filter(type='video')):
                        w_done.append(work)
                    elif len(marks) == 0:
                        w_none.append(work)
                    else:
                        w_wait.append(work)
                        
            print(w_none)
            print(w_done)
            print(w_wait)


            context = {
                'w_none': w_none,
                'w_done': w_done,
                'w_wait': w_wait,
            }
            return render(request, 'expert.html', context=context)


        else:
            return redirect('/lk')
    else:
        return redirect('/login')

def lk_works_work(request, id):
    if 'login' in request.session and request.session['login'] == 1:
        if request.session['account_type'] == 'expert':


            #обрабатываем пост
            if request.method == 'POST':
                print('post')
                form = dict(request.POST).copy()
                del form['csrfmiddlewaretoken']
                print(form)

                for key in form:
                    print(key)
                    print(form[key][0])
                    mark = Mark.objects.get(id=key)
                    try:
                        expert_mark = ExpertMark.objects.get(application=Application.objects.get(id=id), expert=Expert.objects.get(id=request.session['expert_id']), mark=mark)
                        expert_mark.value = form[key][0]
                        expert_mark.save()
                    except:
                        expert_mark = ExpertMark(application=Application.objects.get(id=id), expert=Expert.objects.get(id=request.session['expert_id']), mark=mark, value=form[key][0])
                        expert_mark.save()






            work = Application.objects.get(id=id)
            marks = ExpertMark.objects.filter(application=work, expert=Expert.objects.get(id=request.session['expert_id']))
            marks_dict = {}
            for mark in marks: marks_dict[mark.mark.name] = mark.value
            coauthors = work.coauthors.all()

            if work.file.name.split('.')[-1] == 'mp4' or work.file.name.split('.')[-1] == 'avi':
                work_type = 'video'
                all_marks = Mark.objects.filter(type='video')

            else:
                work_type = 'article'
                all_marks = Mark.objects.filter(type='article')
            all_down_marks = Mark.objects.filter(type='downgrade')
            all_up_marks = Mark.objects.filter(type='upgrade')

            p_marks = []
            for mark_ in all_marks:
                mark__ = {'id': mark_.id, 
                            'name': mark_.name,
                }
                if mark_.name in marks_dict:
                    mark__[marks_dict[mark_.name]] = 'checked'
            
                p_marks.append(mark__)

            print(p_marks)

            down_marks = []
            for mark_ in all_down_marks:
                mark__ = {'id': mark_.id, 
                            'name': mark_.name,
                }
                if mark_.name in marks_dict:
                    mark__[marks_dict[mark_.name]] = 'checked'
            
                down_marks.append(mark__)

            print(down_marks)

            up_marks = []
            for mark_ in all_up_marks:
                mark__ = {'id': mark_.id, 
                            'name': mark_.name,
                }
                if mark_.name in marks_dict:
                    mark__[marks_dict[mark_.name]] = 'checked'
            
                up_marks.append(mark__)

            print(up_marks)

            context = {
                'work': work,
                'all_marks': p_marks,
                'coauthors': coauthors,
                'down_marks': down_marks,
                'up_marks': up_marks,
                'is_video': work_type == 'video',

            }
            return render(request, 'expert-work.html', context=context)
        else:
            return redirect('/lk')
    else:
        return redirect('/login')


def lk_result(request):
    if 'login' in request.session and request.session['login'] == 1:
        if request.session['account_type'] == 'admin':
            works = Application.objects.all()
            works_dict = []
            

            for work in works:
                work_dict = {
                    'id': work.id,
                    'guest' : work.rating,
                }

                all_work_marks = ExpertMark.objects.filter(application=work)
                
                print(all_work_marks)

                marks_dict = {}
                marks_down_dict = {}
                marks_up_dict = {}

                for mark in all_work_marks:
                    mark_type = mark.mark.type
                    if mark_type == 'upgrade':
                        if mark.mark.id in marks_up_dict:
                            marks_up_dict[mark.mark.id].append( mark.value )
                        else:
                            marks_up_dict[mark.mark.id] = [mark.value]
                    elif mark_type == 'downgrade':
                        if mark.mark.id in marks_down_dict:
                            marks_down_dict[mark.mark.id].append( mark.value )
                        else:
                            marks_down_dict[mark.mark.id] = [mark.value]
                    else:
                        if mark.mark.id in marks_dict:
                            marks_dict[mark.mark.id].append( mark.value )
                        else:
                            marks_dict[mark.mark.id] = [mark.value]
            
                print(marks_dict) 
                print(marks_down_dict)
                print(marks_up_dict)

                #считаем среднее значение оценок
                for key in marks_dict:
                    marks_dict[key] = sum(marks_dict[key])/len(marks_dict[key])
                for key in marks_down_dict:
                    marks_down_dict[key] = sum(marks_down_dict[key])/len(marks_down_dict[key])
                for key in marks_up_dict:
                    marks_up_dict[key] = sum(marks_up_dict[key])/len(marks_up_dict[key])

                print(marks_dict)
                print(marks_down_dict)
                print(marks_up_dict)

                #считаем итоговую оценку
                rating = 0
                for key in marks_dict:
                    rating += marks_dict[key]
                for key in marks_down_dict:
                    rating -= marks_down_dict[key]
                for key in marks_up_dict:
                    rating += marks_up_dict[key]

                print(rating)

                work_dict['expert'] = rating

                work_dict['info'] = work.heading+', ' + work.main_author.fio

                

                works_dict.append(work_dict)

            #сортируем по рейтингу
            works_dict = sorted(works_dict, key=lambda k: k['expert'], reverse=True)

            #присваиваем места
            for i in range(len(works_dict)):
                works_dict[i]['place'] = i+1


            return render(request, 'admin.html', context={'works': works_dict})
        else:
            return redirect('/lk')
    else:
        return redirect('/login')


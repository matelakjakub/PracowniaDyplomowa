from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.shortcuts import redirect,render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User   #biblioteka do przekazywania danych użytkownika do bazy danych
from django.contrib import messages   #biblioteka do wyswietlania wiadomosci np. przy rejestracji dla uzytkownika
from django.contrib.auth import authenticate,login, logout #pozwala na sprawdzenie czy hasło użytkownika oraz nazwa się zgadza 

from .models import Team, PastMatch, Player, ForumPost
from .forms import TeamForm, JoinTeamForm, PastMatchForm, ForumPostForm
from django.db.models import F, Sum



#Tutaj tworzymy widoki


def home(request):
    return render(request, "footapp/index.html")

def mapa(request):
    return render(request, 'footapp/mapa.html')

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()

        # Dodaj obiekt modelu Player dla nowego użytkownika
        player = Player(user=myuser)
        player.save()

        messages.success(request, "Twoje konto zostało utworzone!")

        return redirect('home')

    return render(request, "footapp/signup.html")

def signin(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "footapp/index.html", {'fname': fname})

        else:
            messages.error(request, "Złe dane !")
            return redirect('home') 



    return render(request, "footapp/signin.html")

def signout(request):
    logout(request)
    # messages.success(request, "Pomyślnie wylogowano!")
    return redirect('home')

@login_required
def teams_all(request):
    all = Team.objects.all()
    return render(request, 'footapp/teams.html', {'druzyny': all})

@login_required
def new_team(request):
    form = TeamForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect('home')
    
    return render(request, 'footapp/team_form.html', {'form': form})

@login_required
def edit_team(request, id):
    team = get_object_or_404(Team, pk=id)
    form = TeamForm(request.POST or None, request.FILES or None, instance=team)

    if form.is_valid():
        form.save()
        return redirect(teams_all)
    
    return render(request, 'footapp/team_form.html', {'form': form})

@login_required
def delete_team(request, id):
    team = get_object_or_404(Team, pk=id)

    if request.method =="POST":
        team.delete()
        return redirect(teams_all)
    
    return render(request, 'footapp/apply.html', {'team': team})

@login_required
def join_team(request):
    if request.method == 'POST':
        form = JoinTeamForm(request.POST)
        if form.is_valid():
            join_code = form.cleaned_data['join_code']
            try:
                team = Team.objects.get(join_code=join_code)
                if request.user in team.members.all():
                    messages.error(request, "Jesteś już członkiem drużyny.")
                else:
                    team.members.add(request.user)
                    player = Player.objects.get(user=request.user)
                    player.team = team
                    player.save()
                    messages.success(request, 'Pomyślnie dołączyłeś do drużyny {}.'.format(team.name_team))
            except Team.DoesNotExist:
                form.add_error('join_code', 'Drużyna o podanym kodzie nie istnieje.')
    else:
        form = JoinTeamForm()

    return render(request, 'footapp/join_team.html', {'form': form})


@login_required
def add_past_match(request):
    if request.method == 'POST':
        form = PastMatchForm(request.POST)
        if form.is_valid():
            # Pobierz dane z formularza
            team1_name = form.cleaned_data['team1']
            team2_name = form.cleaned_data['team2']
            team1_goals = form.cleaned_data['score_team1']
            team2_goals = form.cleaned_data['score_team2']

            # Pobierz listę strzelców bramek dla drużyny 1 i 2  
            scorers_team1 = request.POST.getlist('scorers_team1[]')
            scorers_team2 = request.POST.getlist('scorers_team2[]')
            


            # # Dodawanie strzelców bramek dla team1
            # match = PastMatch.objects.get(pk=1)
            # player1 = Player.objects.get(name='John Doe')
            # player2 = Player.objects.get(name='Jane Doe')

            # match.scorers_team1.add(player1, player2)

            # # Dodawanie strzelców bramek dla team2
            # match.scorers_team2.add(player1, player2)

            
            

            # Znajdź lub utwórz obiekty Team na podstawie nazw drużyn
            try:
                team1 = Team.objects.get(name_team=team1_name)
                team2 = Team.objects.get(name_team=team2_name)
            except Team.DoesNotExist:
                # Jeśli drużyna nie istnieje, można ją utworzyć lub obsłużyć błąd
                raise Http404("Drużyna nie istnieje")


            # Dodaj gole do obiektów Team
            team1.goals_for += team1_goals
            team1.goals_against += team2_goals
            team2.goals_for += team2_goals
            team2.goals_against += team1_goals


            if team1_goals > team2_goals:
                team1.points+=3
            elif team2_goals > team1_goals:
                team2.points +=3
            else:
                team1.points+=1
                team2.points+=1


            # Zapisz obiekty Team, aby zaktualizować liczbę goli i punktów
            team1.save()
            team2.save()

            # Możesz również stworzyć nowy obiekt PastMatch i przypisać do niego te drużyny
            past_match = form.save(commit=False)
            past_match.team1 = team1
            past_match.team2 = team2
            past_match.scorers_team1 = scorers_team1
            past_match.scorers_team2 = scorers_team2

            past_match.save()
            
            return redirect('signin')  # Replace 'success_page' with the URL name you want to redirect to
    else:
        form = PastMatchForm()
        
    
    return render(request, 'footapp/add_past_match.html', {'form': form})
@login_required
def recent_matches(request):
    recent_matches = PastMatch.objects.order_by('-date')[:10]
    return render(request, 'footapp/recent_matches.html', {'recent_matches': recent_matches})

@login_required
def league_table(request):
    teams = Team.objects.all()
    teams = Team.objects.annotate(goal_difference=F('goals_for') - F('goals_against')).order_by('-points', '-goal_difference')

    return render(request, 'footapp/league_table.html', {'teams': teams})

@login_required
def your_team(request):
    user_teams = request.user.teams.all()
    return render(request, 'footapp/your_team.html', {'user_teams': user_teams})

@login_required
def leave_team(request, id):
    team = get_object_or_404(Team, pk=id)

    if request.method == "POST":
        team.members.remove(request.user)
        return redirect('your_team')

    return render(request, 'footapp/leave_team.html', {'team': team})


def forum(request):
    posts = ForumPost.objects.all()
    form = ForumPostForm()

    if request.method == 'POST':
        form = ForumPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Przypisz autora posta do aktualnie zalogowanego użytkownika
            post.save()
            return redirect('forum')

    return render(request, 'footapp/forum.html', {'posts': posts, 'form': form})


def forum_post_detail(request, pk):
    post = get_object_or_404(ForumPost, pk=pk)
    return render(request, 'footapp/forum_post_detail.html', {'post': post})

@login_required
def edit_forum_post(request, pk):
    post = get_object_or_404(ForumPost, pk=pk)

    # Dodaj sprawdzenie, czy aktualnie zalogowany użytkownik jest autorem posta
    if request.user != post.author:
        # Możesz przekierować użytkownika, wyświetlić komunikat, itp.
        return HttpResponseForbidden("Nie masz uprawnień do edycji tego posta.")

    if request.method == 'POST':
        form = ForumPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('forum')  # Przekierowanie na stronę 'forum' po zapisaniu zmian
    else:
        form = ForumPostForm(instance=post)

    return render(request, 'footapp/edit_forum_post.html', {'form': form, 'post': post})

@login_required
def delete_forum_post(request, pk):
    post = get_object_or_404(ForumPost, pk=pk)

    # Dodaj sprawdzenie, czy aktualnie zalogowany użytkownik jest autorem posta
    if request.user != post.author:
        # Możesz przekierować użytkownika, wyświetlić komunikat, itp.
        return HttpResponseForbidden("Nie masz uprawnień do usunięcia tego posta.")

    if request.method == 'POST':
        post.delete()
        return redirect('forum')

    return render(request, 'footapp/delete_forum_post.html', {'post': post})



class CustomPasswordResetView(PasswordResetView):
    template_name = 'footapp/registration/password_reset_form.html'


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'footapp/registration/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'footapp/registration/password_reset_confirm.html'

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'footapp/registration/password_reset_complete.html'







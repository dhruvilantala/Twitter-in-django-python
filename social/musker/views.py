from django.shortcuts import redirect, render, get_object_or_404
from .models import *
from django.contrib import messages
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        # profiles = Profile.objects.exclude(user=request.user).order_by('?')[:3]
        current_user_profile = Profile.objects.get(user=request.user)
        profiles = Profile.objects.exclude(followed_by=current_user_profile).order_by('?')[:3]
        form = MeepForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                meep = form.save(commit=False)
                meep.user = request.user
                meep.save()
                messages.success(request, 'Your tweet has been posted...')
                return redirect('home')
        followed_profiles = current_user_profile.follows.all()
        followed_users = followed_profiles.values_list('user', flat=True)    
        meeps = Meep.objects.filter(user__in=followed_users).order_by('-created_at')
        return render(request, 'home.html', {'meeps': meeps, 'form': form, 'profiles': profiles})
    else:
        meeps = Meep.objects.all().order_by('-created_at')
        return render(request, 'home.html', {'meeps': meeps})


def profile_list(request):
    if request.user.is_authenticated:
        current_user_profile = Profile.objects.get(user=request.user)
        profiles = Profile.objects.exclude(followed_by=current_user_profile)
        return render(request, 'profile_list.html', {'profiles': profiles})
    else:
        messages.success(request, 'You Must be logged in to view this page...')
        return redirect('home')
    
def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id = pk)
        meeps = Meep.objects.filter(user_id = pk).order_by('-created_at')

        # post form logic
        if request.method == 'POST':
            #get current user
            current_user_profile = request.user.profile
            #get form data
            action = request.POST['follow']
            # decide to follow or unfollow
            if action == 'unfollow':
                current_user_profile.follows.remove(profile)
            elif action == 'follow':
                current_user_profile.follows.add(profile)
            # save the profile
            current_user_profile.save()

        return render(request, 'profile.html', {'profile': profile, 'meeps':meeps})
    else:
        messages.success(request, 'You Must be logged in to view this page...')
        return redirect('home')
    

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user) 
            messages.success(request, 'You have been logged in!')
            return redirect('home')
        else:
            messages.success(request, 'There was some error logging in. Please try again...')
            return redirect('home')
    return render(request, 'login.html')

def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            # email = form.changed_data['email']
            #login user
            user = authenticate(username=username, password=password)
            login(request,user)
            messages.success(request, ("You have successfully registered! Welcome!"))
            return redirect('home')
    return render(request, 'register.html', {'form':form})

def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logout.')
    return redirect('home')


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        profile_user = Profile.objects.get(user__id=request.user.id)

        user_form = SignUpForm(request.POST or None, instance=current_user)
        profile_form = ProFilePicForm(request.POST or None, request.FILES or None, instance=profile_user)

        if request.method == 'POST':
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')

            if password1 == password2:
                current_user.set_password(password1)

            current_user.email = email
            current_user.first_name = first_name
            current_user.last_name = last_name
            current_user.username = username
            current_user.save()

        if profile_form.is_valid():
            profile_form.save()

            login(request, current_user)
            messages.success(request, 'Your Profile has been updated...')
            return redirect('home')
        return render(request, 'update_user.html', {'user_form':user_form, 'profile_form':profile_form })
    else:
        messages.success(request, 'You have been logout.')
        return redirect('home')
    
def meep_like(request, pk):
    if request.user.is_authenticated:
        meep = get_object_or_404(Meep, id=pk)
        if meep.likes.filter(id=request.user.id):
            meep.likes.remove(request.user)
        else:
            meep.likes.add(request.user)

        return redirect(request.META.get('HTTP_REFERER'))
    
    else:
        messages.success(request, 'You Must be logged in to view this page...')
        return redirect('home')

def meep_show(request, pk):
    meep = get_object_or_404(Meep, id=pk)
    if meep:
        return render(request, 'meep_show.html', {'meep':meep})
    else:
        messages.success(request, 'That tweet does not exist...')
        return redirect('home')
    
def unfollow(request, pk):
	if request.user.is_authenticated:
		# Get the profile to unfollow
		profile = Profile.objects.get(user_id=pk)
		# Unfollow the user
		request.user.profile.follows.remove(profile)
		# Save our profile
		request.user.profile.save()

		# Return message
		messages.success(request, (f"You Have Successfully Unfollowed {profile.user.username}"))
		return redirect(request.META.get("HTTP_REFERER"))

	else:
		messages.success(request, ("You Must Be Logged In To View This Page..."))
		return redirect('home')    

def follow(request, pk):
	if request.user.is_authenticated:
		# Get the profile to unfollow
		profile = Profile.objects.get(user_id=pk)
		# Unfollow the user
		request.user.profile.follows.add(profile)
		# Save our profile
		request.user.profile.save()

		# Return message
		messages.success(request, (f"You Have Successfully Followed {profile.user.username}"))
		return redirect(request.META.get("HTTP_REFERER"))

	else:
		messages.success(request, ("You Must Be Logged In To View This Page..."))
		return redirect('home')

@login_required(login_url='/login/')
def meep_comment(request, pk):
    tweets = Meep.objects.get(id=pk)

    if request.method == 'POST':
        body = request.POST.get('comment_body')
        comment =Comment(
            tweet = tweets,
            user = request.user,
            body = body,
        )
        comment.save()
       
    comments = Comment.objects.filter(tweet_id=pk)
    if tweets:
        return render(request, "meep_comment.html", {'meep':tweets , "comments":comments})
    else:
        messages.success(request, ("That Tweet Does Not Exist..."))
        return redirect('home')	
    


@login_required(login_url='/login/')
def delete_comment(request, pk):
   comment = get_object_or_404(Comment, id=pk)	
   if request.user.id == comment.user.id:
       comment.delete()
       messages.success(request, ("The comment Has Been Deleted!"))
       return redirect(request.META.get("HTTP_REFERER"))
   
   messages.success(request, ("You Don't Own This Comment!!"))
   return redirect('home')

@login_required(login_url='/login/')
def delete_meep(request, pk):
   meep = get_object_or_404(Meep, id=pk)	
   if request.user.id == meep.user.id:
       meep.delete()
       messages.success(request, ("The Tweet Has Been Deleted!"))
       return redirect(request.META.get("HTTP_REFERER"))
   
   messages.success(request, ("You Don't Own This Tweet!!"))
   return redirect('home')

@login_required(login_url='/login/')
def edit_meep(request, pk):
    meep = get_object_or_404(Meep, id=pk)
    if request.user.id == meep.user.id:
        form = MeepForm(request.POST or None, instance=meep)
        if request.method == 'POST':
            if form.is_valid():
                meep = form.save(commit=False)
                meep.user = request.user
                meep.save()
                messages.success(request, 'Your tweet has been updated...')
                return redirect('home')	
        else:
            return render(request, 'edit_meep.html', {'meep': meep, 'form': form})
        
    messages.success(request, ("please login!!"))
    return redirect('home')

@login_required(login_url='/login/')
def like_comment(request,pk):
    comment =  get_object_or_404(Comment,id = pk)
    if comment.likes.filter(id= request.user.id):
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)
    return redirect(request.META.get('HTTP_REFERER'))
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .form import SignUpForm, AddRecordForm
from .models import Record


def home(request):
    records = Record.objects.all()

    if request.method == 'POST':
		try:
	        username = request.POST['username']
	        password = request.POST['password']
	        user = authenticate(request, username=username, password=password)
	        if user is not None:
	            login(request, user)
	            messages.success(request, 'You have successfully logged in!')
	            return redirect('home')
	        else:
	            messages.error(request, 'Username or password is incorrect! Try again!')
	            return redirect('home')
		 except Exception as e:
            print("🔥 POST ERROR:", e)
            raise
    else:
        return render(request, 'index.html', {'records': records})


def logout_user(request):
    logout(request)
    messages.success(request, 'You have successfully logged out!')
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You have successfully registered!')
            return redirect('home')

    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html',{'form': form})


def customer_record(request,pk):
    if request.user.is_authenticated:
        customer_records = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record': customer_records})
    else:
        messages.success(request, 'You must be logged in to view the records!')
        return redirect('home')

def delete_record(request,pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, 'You have successfully deleted!')
        return redirect('home')
    else:
        messages.success(request, 'You must be logged in to delete the records!')
        return redirect('home')

def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':

            if form.is_valid():
                form.save()
                messages.success(request, 'You have successfully added!')
                return redirect('home')

        return render(request, 'add_record.html',{'form': form})
    else:
        messages.success(request, 'You must be logged in to add records!')
        return redirect('home')

def update_record(request, pk):
	if request.user.is_authenticated:
		current_record = Record.objects.get(id=pk)
		form = AddRecordForm(request.POST or None, instance=current_record)
		if form.is_valid():
			form.save()
			messages.success(request, "Record Has Been Updated!")
			return redirect('home')
		return render(request, 'update_record.html', {'form':form})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('home')





from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User, auth
from contact.models import contactform

import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
import re
import pickle

import nltk
from nltk.corpus import wordnet

stopwords = nltk.corpus.stopwords.words('english')
from nltk.stem import PorterStemmer, WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer



@login_required(login_url="/login")
def home(request):

     if request.method=="POST":

        if request.FILES == '':
            msg = "choose a file to upload"
            return render(request,'index.html',{'message':msg})

        else:

         uploaded_text = request.POST.get('rawtext')
         stemmer=PorterStemmer()


        def process_text(text):
            text=text.lower()
            text=re.sub("[^a-zA-Z!ñíá]"," ",str(text))
            text_wt=nltk.word_tokenize(text)
            text_sstopw=list(filter(lambda w: w not in stopwords, text_wt))
            text_stem=list(map(lambda w: stemmer.stem(w), text_sstopw))
            new_text=" ".join(text_stem)
            return new_text

        processed_text =[process_text(uploaded_text)]
        print(processed_text)
        

        file_path_cov = 'count_vectorization.pkl'
        with open(file_path_cov , 'rb') as a:
            cou_vec = pickle.load(a)

        matriz_text = cou_vec.transform(processed_text)
        print(matriz_text)
        final_text = matriz_text.toarray()
        print(final_text)

        file_path = 'svc_stress.pkl'

        with open(file_path , 'rb') as f:
            model = pickle.load(f)

        stress_pred = model.predict(final_text)

        #print(stress_pred)

        if stress_pred == 1:
           transaction = 'Stressed'
           statem = 'The text seems more likely to be Stressed' 
    
        else:
           transaction = 'NotStressed'
           statem = 'This text seems more likely to be Notstressed'

        return render(request,'index.html',{'prediction_text5':transaction, 'statement':statem })



     return render(request, 'index.html')


def signup(request):
     if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Taken')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('signup')
            else:   
                user = User.objects.create_user(username=username, password=password1, email=email,first_name=first_name,last_name=last_name)
                user.save()
                print('user created')
                return redirect('login')
        else:
            messages.info(request,'password not matching..')    
            return redirect('signup')
     else:
        return render(request, 'signup.html')


def login(request):
    if request.method== 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.info(request,'invalid credentials')
            return redirect('login')
    else:

        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('login') 

def contact(request):
    if request.method == "POST":
        
        name = request.POST.get('name')
        email = request.POST.get('email')
        text = request.POST.get('message')
        en = contactform(name=name,email=email,message=text)
        en.save()

    return render(request,'contact.html')             

def models(request):

    return render(request,'models.html')
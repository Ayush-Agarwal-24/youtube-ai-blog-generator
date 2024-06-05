from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
import json
from pytube import YouTube
import os
import assemblyai as aai
import openai
from openai import OpenAI
from markdown2 import markdown
from django.utils.html import mark_safe
from .models import BlogPost
from dotenv import load_dotenv
# Create your views here.
@login_required
def index(request):
    return render(request, 'index.html')

def text_to_html(raw_text):
        html = markdown(raw_text)
        return mark_safe(html)  

@csrf_exempt
def generate_blog(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            yt_link = data.get('link')
        except(KeyError, json.JSONDecodeError):
            return JsonResponse({'error':'Invalid data sent'},status=400)    
        
        title = get_yt_title(yt_link)
        
        transcription = get_transcription(yt_link)
        if not transcription:
            return JsonResponse({'error':'Failed to get transcript'}, status = 500)

        blog_content = generate_blog_from_transcription(transcription)
        if not blog_content:
            return JsonResponse({'error':'Failed to generate blog article'}, status = 500)
        
        
        html_content = text_to_html(blog_content)
        new_blog_article = BlogPost.objects.create(
            user = request.user,
            youtube_title = title,
            youtube_link = yt_link,
            generated_content = html_content
        )
        new_blog_article.save()
        
        return JsonResponse({'content': html_content})
    else:
        return JsonResponse({'error':'Invalid request method'},status=405)

def get_yt_title(link):
    yt = YouTube(link)
    title = yt.title
    return title

def download_audio(link):
    yt = YouTube(link)
    video = yt.streams.filter(only_audio=True).first()

    # Generate a unique filename based on the video title and a random suffix if needed
    base_filename = yt.title.replace(" ", "_").replace(".", "_")
    safe_filename = f"{base_filename}.mp3"
    complete_path = os.path.join(settings.MEDIA_ROOT, safe_filename)

    # Initialize new_filename with safe_filename
    new_filename = safe_filename

    # Check if the file already exists
    if os.path.exists(complete_path):
        base, ext = os.path.splitext(safe_filename)
        import time
        # Adding a time-based suffix to make the filename unique
        new_filename = f"{base}_{int(time.time())}{ext}"
        complete_path = os.path.join(settings.MEDIA_ROOT, new_filename)

    # Download the file
    out_file = video.download(output_path=settings.MEDIA_ROOT, filename=new_filename)

    # Rename the file to have a .mp3 extension if necessary
    base, ext = os.path.splitext(out_file)
    if ext != '.mp3':
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
        out_file = new_file

    return out_file

def get_transcription(link):
    audio_file = download_audio(link)
    aai.settings.api_key =  os.getenv('AAI_API_KEY')

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file)
    
    return transcript.text

def generate_blog_from_transcription(transcription):
    openai.api_key =  os.getenv('OPENAI_API_KEY')  # Replace with your actual key
    client = OpenAI(api_key=openai.api_key)

    prompt = f"Based on the following transcript from a YouTube video, write a comprehensive blog article, write it based on the transcript, but dont make it look like a youtube video, make it look like a proper blog article:\n\n{transcription}\n\nArticle:"
    params = {
        "model": "gpt-4-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1000,
        "temperature": 0.5
    }
    response = client.chat.completions.create(**params)
    generated_content = response.choices[0].message.content.strip()
    
    return generated_content

def blog_list(request):
    blog_articles = BlogPost.objects.filter(user=request.user)
    return render(request, "all-blogs.html",{'blog_articles':blog_articles})    

def blog_details(request,pk):
    blog_article_detail = BlogPost.objects.get(id=pk)
    if request.user == blog_article_detail.user:
        return render(request, 'blog-details.html',{'blog_article_detail':blog_article_detail})
    else:
        return redirect('/')
def user_login(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message':error_message})
    return render(request, 'login.html')

def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repeatPassword = request.POST['repeatPassword']
        
        if password == repeatPassword:
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
                login(request, user)
                return redirect('/')
            except:
                error_message = 'Error creating account'
                return render(request, 'signup.html', {'error_message':error_message})
        else:
            error_message = 'Password do not match'
            return render(request, 'signup.html', {'error_message':error_message})
    return render(request, 'signup.html')

def user_logout(request):
    logout(request)
    return redirect('/')
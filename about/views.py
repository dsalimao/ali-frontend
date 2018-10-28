from django.shortcuts import render

ALI_GOOGLE_PHOTO_ALBUM = 'https://photos.app.goo.gl/hiYEb8ecrVfb1dgV7'


def about_ali(request):
    return render(request, 'about/ali.html')


def about_me(request):
    pass

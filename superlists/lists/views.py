from django.shortcuts import redirect, render
from lists.models import Item, List
from django.core.exceptions import ValidationError

# Create your views here.
def home_page(request):
    # if request.method == 'POST':
    #     Item.objects.create(text=request.POST['item_text'])
    #     return redirect('/lists/the-only-list/')

    return render(request, 'home.html')

def new_list(request):
    new_list = List.objects.create()
    item = Item.objects.create(text=request.POST['item_text'], list= new_list)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        new_list.delete()
        error = "You can't have an empty list item"
        return render(request, 'home.html', {'error':error})
    return redirect('/lists/%d/' % (new_list.id,))

def view_list(request, list_id):

    list_ = List.objects.get(id=list_id)
    items = Item.objects.filter(list=list_)

    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'], list= list_)
    return render(
        request, 'list.html',
        { 'items': items, 'list': list_ }
    )

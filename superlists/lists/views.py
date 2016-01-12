from django.shortcuts import redirect, render
from lists.models import Item, List

# Create your views here.
def home_page(request):
    # if request.method == 'POST':
    #     Item.objects.create(text=request.POST['item_text'])
    #     return redirect('/lists/the-only-list/')
    return render(request, 'home.html')

def new_list(request):
    new_list = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list= new_list)
    return redirect('/lists/%d/' % (new_list.id,))

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    items = Item.objects.filter(list=list_)
    return render(
        request, 'list.html',
        { 'items': items, 'list': list_ }
    )

def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list= list_)
    return redirect('/lists/%d/' % (list_.id,))


def delete_item(request, item_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list= list_)
    return redirect('/lists/%d/' % (list_.id,))

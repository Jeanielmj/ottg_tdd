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
    error = None

    if request.method == 'POST':
        try:
            item = Item(text=request.POST['item_text'], list= list_)
            item.full_clean()
            item.save()
        except ValidationError:
            error = "You can't have an empty list item"

    return render(
        request, 'list.html',
        { 'list': list_, 'error': error }
        )

def delete_item(request, list_id, item_id):
    list_ = List.objects.get(id=list_id)
    item_ = Item.objects.get(id=item_id)
    item_.delete()
    return redirect('/lists/%d/' % (list_.id))

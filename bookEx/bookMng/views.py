from django.http import HttpResponse
from django.shortcuts import render
from .models import MainMenu
from .forms import BookForm
from django.http import HttpResponseRedirect
from .models import Book
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .models import Message
from .forms import MessageForm
from django.shortcuts import redirect
from .models import Cart, CartItem, Book
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url=reverse_lazy('login'))
def index(request):
    #return HttpResponse("<h1>Hello</h1>")
    return render(request,
                  'bookMng/index.html',
                  {
                      'item_list': MainMenu.objects.all()
                  }
                  )
def aboutus(request):

    return render(request,
                  'bookMng/aboutus.html',
                  {
                      'item_list': MainMenu.objects.all()
                  }
                  )
@login_required(login_url=reverse_lazy('login'))
def postbook(request):
    submitted = False
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            try:
                book.username = request.user
            except Exception:
                pass
            book.save()
            return HttpResponseRedirect('/postbook?submitted=True')
    else:
        form = BookForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request,
                  'bookMng/postbook.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'form': form,
                      'submitted' : submitted
                  }
                  )
@login_required(login_url=reverse_lazy('login'))
def displaybooks(request):
    books = Book.objects.all()
    for b in books:
        b.pic_path = b.picture.url[14:]
    return render(request,
                  'bookMng/displaybooks.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books,
                      'range_5': range(1, 6),  # Add this line to pass the range to the template
                  }
                  )

class Register(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register-success')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)

@login_required(login_url=reverse_lazy('login'))
def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)

    book.pic_path = book.picture.url[14:]
    return render(request,
                  'bookMng/book_detail.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'book': book
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def book_delete(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()
    return render(request,
                  'bookMng/book_delete.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'book': book
                  }
                  )

@login_required(login_url=reverse_lazy('login'))
def mybooks(request):
    books = Book.objects.filter(username=request.user)
    for b in books:
        b.pic_path = b.picture.url[14:]
    return render(request,
                  'bookMng/mybooks.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books
                  }
                  )

@login_required(login_url=reverse_lazy('login'))
def messages(request):
    submitted = False
    messages = Message.objects.all()
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            try:
                message.user = request.user
            except Exception:
                pass
            message.save()
            return HttpResponseRedirect('/messages?submitted=True')
    else:
        form = MessageForm()
        if 'submitted' in request.GET:
            submitted = True

    for message in messages:
        message.user = request.POST.get('user')
        message.message = request.POST.get('message')
        message.date = request.POST.get('date')

    return render(request, 'bookMng/messages.html',{
                      'item_list': MainMenu.objects.all(),
                      'form': form,
                      'submitted': submitted,
                      'messages': messages,
                  })

def search(request):
    books = Book.objects.filter(name__contains=request.GET.get('search'))
    for b in books:
        b.pic_path = b.picture.url[14:]
    return render(request,
                  'bookMng/search.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books
                  }
                  )

@login_required(login_url=reverse_lazy('login'))
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)
    cart_item.quantity += 1  # Increment quantity or set it as per your logic
    cart_item.save()
    return redirect('cart')  # Redirect to the cart view

@login_required(login_url=reverse_lazy('login'))
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    return render(request, 'bookMng/cart.html', {'items': items})

def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('cart')




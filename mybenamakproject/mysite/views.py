# Django Core Imports
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.mail import EmailMessage, send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt

# Forms and Models
from .forms import ContactForm, PortfolioItemForm
from .models import PortfolioItem, Product

# Python Standard Library
import json
import base64


def home(request):
    portfolio_items = PortfolioItem.objects.all()
    return render(request, 'home.html', {'portfolio_items': portfolio_items})


# def portfolio_view(request):
#     portfolio_items = PortfolioItem.objects.all()
#     return render(request, 'home.html', {'portfolio_items': portfolio_items})

from .forms import PortfolioItemForm

def upload_portfolio_item(request):
    if request.method == 'POST':
        form = PortfolioItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to the portfolio page after uploading
    else:
        form = PortfolioItemForm()

    return render(request, 'upload_portfolio_item.html', {'form': form})




from django.contrib import messages

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            # Extract data from form
            name = form.cleaned_data['name']
            user_email = form.cleaned_data['email']
            t_shirt_type = form.cleaned_data['t_shirt_type']
            message = form.cleaned_data['message']
            design = form.cleaned_data['design']
            
            # Create the email content
            subject = f'New Contact Form Submission from {name}'
            body = f'''
                You have a new message from {name} ({user_email}):
                
                Type of T-shirt: {t_shirt_type}
                Message: {message}
                
                Attached Design: {design}
            '''
            
            # Create the email
            email_message = EmailMessage(
                subject,
                body,
                from_email=user_email,
                to=[settings.DEFAULT_FROM_EMAIL],
                reply_to=[user_email],
            )

            # Add the attachment if provided
            if design:
                email_message.attach(design.name, design.read(), design.content_type)

            # Send the email
            try:
                email_message.send()
                messages.success(request, 'Thank you for your message! We will get back to you soon.')  # Set success message
                return redirect('home')
            except Exception as e:
                print(f"Error sending email: {e}")
                messages.error(request, 'There was an error sending your message. Please try again.')  # Set error message
                return redirect('contact')  # Redirect back to contact form

    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})



def newsletter_subscribe(request):
    if request.method == "POST":
        email = request.POST.get('email')
        # Process the email (e.g., save to database, send confirmation, etc.)
        send_mail(
            'Subscription Confirmation',
            'Thank you for subscribing to our newsletter!',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        return redirect('contact_success')  # Redirect to a thank you page
    return redirect('home')


def contact_success(request):
    return render(request, 'contact_success.html')

def contact_thank_you(request):
    return render(request, 'thank_you.html')


def manage_designs(request):
    portfolio_items = PortfolioItem.objects.all()  # Fetch all portfolio items
    return render(request, 'manage_designs.html', {'portfolio_items': portfolio_items})

def delete_design(request, item_id):
    item = get_object_or_404(PortfolioItem, id=item_id)
    if item.image:
        item.image.delete()  # Delete the image file from the filesystem
    item.delete()  # Delete the record from the database
    return redirect('manage_designs')  # Redirect to the portfolio management page

# View for editing a portfolio item
def edit_portfolio_item(request, item_id):
    item = get_object_or_404(PortfolioItem, id=item_id)  # Get the item or 404 if not found
    if request.method == 'POST':
        form = PortfolioItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()  # Save the updated item
            return redirect('manage_portfolio')
    else:
        form = PortfolioItemForm(instance=item)  # Pre-fill the form with existing data
    return render(request, 'edit_portfolio_item.html', {'form': form, 'item': item})




def design_page(request):
    return render(request, 'design.html')

@csrf_exempt
def save_design(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            design_data = data.get('design')
            if not design_data:
                return JsonResponse({'error': 'No design data provided'}, status=400)

            # Decode base64 data
            format, imgstr = design_data.split(';base64,')
            ext = format.split('/')[-1]
            img_data = ContentFile(base64.b64decode(imgstr), name=get_random_string(10) + '.' + ext)

            # Save the image (you may want to adjust this to save to a model)
            with open(f'media/designs/{img_data.name}', 'wb') as f:
                f.write(img_data.read())

            return JsonResponse({'message': 'Design saved successfully!'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)



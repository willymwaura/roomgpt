
from django.http import response
from django.shortcuts import render
import requests
from mainapp.models import User  as CustomUser ,CreditBalance,PaymentsActivated
from django.http import HttpResponse,JsonResponse
from django.shortcuts import redirect
from intasend import APIService
import json


# Create your views here.
def index(request):
    return render(request,'login.html')


def account(request):
    return render(request,'account.html')

def login(request):
    return render(request,'login.html')

def create_account(request):

    password = request.POST.get('password', False)
    email = request.POST.get('email', False)

        # Check if email and password are provided
    if not email or not password:
        message="Email and password are required."
        return render(request, "account.html", {"message": message})

        # Check if user already exists
    if CustomUser.objects.filter(email=email).exists():
        
        message="User with this email already exists.."
        return render(request, "account.html", {"message": message})

        # Create user
    user = CustomUser.objects.create(email=email, password=password)
    CreditBalance.objects.create(user_id=user.id, balance=0)

        # Respond with success message
    return render(request, "login.html")

def auth_login(request):
    email = request.POST.get('email',False)
    password = request.POST.get('password',False)

        # Check if email and password are provided
    if not email or not password:
        
        message= "Email and password are required."
        return render(request, "login.html", {"message": message})

    try:
            # Check if user exists
        user = CustomUser.objects.get(email=email,password=password)
    except CustomUser.DoesNotExist:
        
        message= "User does not exist."
        return render(request, "login.html", {"message": message})

        # Check if password is correct
    if user.password != password:
        
        message= "Incorrect password."
        return render(request, "login.html", {"message": message})

        # If everything is correct, respond with user details
    # Store the user ID in the session
    request.session['user_id'] = user.id
   
    return redirect('dashboard')

def textimage(request):
    # Get the user ID from session
    user_id = request.session.get('user_id')

    if not user_id:
        # User ID is not found in the session, redirect to login
        return redirect('login')

    # Check if the user has sufficient credit balance
    try:
        credit_balance = CreditBalance.objects.get(user_id=user_id)
        if credit_balance.balance < 10:
            # Not enough credit balance, render index.html with a message
            return render(request, "index.html", {"error": "Not enough credit recharge your account.","credit_balance":credit_balance.balance})
        else:
            # Subtract 10 credits from the user's balance
            credit_balance.balance -= 10
            credit_balance.save()
    except CreditBalance.DoesNotExist:
        # User's credit balance record does not exist, handle appropriately
        pass
    credit_balance = CreditBalance.objects.get(user_id=user_id).balance

    # Continue with the request and render the response
    prompt = request.POST.get('prompt', False)
    print(prompt)
    payload = {
    "model": "dall-e-3",
    "prompt": "a big white box with sorrounded with a small black bacground",
    "size": "1024x1024",
    "quality": "standard",
    "n": 1
}

    # Define the endpoint URL
    url = " https://api.openai.com/v1/images/generations"

    # Define your OpenAI API key
    api_key = "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"

    # Set up the headers
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Send the request
    response = requests.post(url, headers=headers, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response JSON
        response_data = response.json()
        # Extract the URL of the generated image
        image_url = response_data["data"][0]["url"]
        print("Generated image URL:", image_url)
        return render(request, "index.html", {"image": image_url ,"credit_balance":credit_balance})
    else:
        return render(request, "index.html", {"error": "kindly try later there is more traffic at the moment" ,"credit_balance":credit_balance})

def imagetoimage(request):
    user_id = request.session.get('user_id')

    if not user_id:
        # User ID is not found in the session, redirect to login
        return redirect('login')

    # Check if the user has sufficient credit balance
    try:
        credit_balance = CreditBalance.objects.get(user_id=user_id)
        if credit_balance.balance < 10:
            # Not enough credit balance, render index.html with a message
            return render(request, "index.html", {"error": "Not enough credit recharge your account .","credit_balance":credit_balance.balance})
        else:
            # Subtract 10 credits from the user's balance
            credit_balance.balance -= 10
            credit_balance.save()
    except CreditBalance.DoesNotExist:
        # User's credit balance record does not exist, handle appropriately
        pass
    credit_balance = CreditBalance.objects.get(user_id=user_id).balance
    print(credit_balance)
    uploaded_image = request.FILES['image']
    print("Uploaded file name:", uploaded_image.name)
    return render(request,"index.html",{"image":"https://images.unsplash.com/photo-1613685301586-4f2b15f0ccd4?q=80&w=1332&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D","credit_balance":credit_balance})

def dashboard(request):
    user_id = request.session.get('user_id')

    if not user_id:
        # User ID is not found in the session, redirect to login
        return redirect('login')
    credit_balance = CreditBalance.objects.get(user_id=user_id).balance
    
    return render(request,"index.html",{"credit_balance":credit_balance})

def checkout(request):
    return render (request,"checkout.html")

def mpesa_checkout(request):
    phone = request.POST.get('phone', False)
    email = request.POST.get('email', False)
    amount = request.POST.get('amount', False)
    print(amount)
    payment_instance=PaymentsActivated(phone=phone,email=email,amount=amount)
    payment_instance.save()
    
    if int(amount) < 50:
        return render (request,"checkout.html",{"error": "minimum amount to pay is 50 kshs."})

        # Check if all required fields are provided
    if not phone or not email or not amount:
        return render(request,"checkout.html",{"error": "Mpesa_number, Email, and Amount are must all be filled."})

    try:
            # Initialize the APIService
        token = "ISSecretKey_live_0bcbeaa2-f210-476b-9bfa-28fae2ee5c0a"
        publishable_key = "ISPubKey_live_ee33ed45-3f7e-46ce-a6a4-d91fae6de1de"
        service = APIService(token=token, publishable_key=publishable_key, test=False)

            # Trigger M-Pesa STK Push
        response = service.collect.mpesa_stk_push(phone_number=phone, email=email, amount=amount, narrative="Payment")
        print(response)

            # Return the response from the M-Pesa STK Push
        return render(request,"loading.html")

    except Exception as e:
            # Return an error if there's an exception
        return render(request,"checkout.html",{"error": "try again later "})
    
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  
def PaymentCallback(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data in the request."}, status=400)
    print(data)
    

        # Check if transaction state is complete
    if data["state"] == "COMPLETE":
        try:
                # Get or create credit balance for the account
            email = data["account"]
            user = CustomUser.objects.get(email=email)

                # Get or create credit balance for the account
            user_id = user.id
            credit_balance, created = CreditBalance.objects.get_or_create(user_id=user_id)
                
                
                # Update credit balance
            credit_balance.balance += float(data["net_amount"])
            credit_balance.save()

            print("payment for user id",user_id,"for amount ",data["net_amount"],"is complete")
        except Exception as e:
                return HttpResponse({"error": str(e)})
    else:
            print({"message": "Transaction state is not complete."})



  
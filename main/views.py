from django.shortcuts import render, redirect
from .models import Customer, Specialty, Contractor, Bid, Review, Project, Proj_imgage
import bcrypt
from django.contrib import messages

def index(request):
    return render(request, 'home.html')

def con_reg_form(request):
    return render(request, 'contractor_reg.html')

def con_register(request):
    errors = Contractor.objects.con_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(con_reg_form)
    
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    con = Contractor.objects.create(
        bname = request.POST['bname'],
        alias = request.POST['alias'],
        email = request.POST['email'],
        city = request.POST['city'],
        state = request.POST['state'],
        zipcode = request.POST['zipcode'],
        password = pw_hash,
    )
    spec = Specialty.objects.create(
        title = request.POST['specialty'],
    )
    spec.contractors.add(con)
    request.session['id'] = con.id
    return redirect(con_home)

def con_login(request):
    user_db = Contractor.objects.filter(email=request.POST['email'])
    if user_db:
        log_user = user_db[0]

        if bcrypt.checkpw(request.POST['password'].encode(), log_user.password.encode()):
            request.session['id'] = log_user.id
            return redirect(con_home)

    messages.error(request, 'Incorrect email or password.')
    return redirect(con_reg_form)

def con_home(request):
    contractor = Contractor.objects.get(id=request.session['id'])
    context = {
        'contractor': contractor,
        'projects' : Project.objects.all()
    }
    return render(request, 'contractor-home.html', context)

def logout(request):
    request.session.flush()
    return redirect(index)

def specialty_add(request):
    Specialty.objects.create(
        title= request.POST['title']
    )
    return redirect(con_home)

def bid_form(request, id):
    proj = Project.objects.get(id=id)
    contractor = Contractor.objects.get(id=request.session['id'])
    bid = Bid.objects.filter(contractor=contractor)[::-1]
    context = {
        'project' : proj,
        'contractor' : contractor,
        'bids' : bid
    }
    return render(request, 'con_view_proj.html', context)

def place_bid(request):
    proj = Project.objects.get(id=request.POST['project'])
    con = Contractor.objects.get(id=request.POST['contractor'])
    bid = Bid.objects.create(
        price = request.POST['price'],
        scope = request.POST['scope'],
        contractor = con,
        project = proj
    )
    return redirect(con_home)

def edit_bid(request, id):
    bid = Bid.objects.get(id=id)
    context = {
        'bid' : bid
    }
    return render(request, 'edit_bid.html', context)

def process_edit(request):
    bid = Bid.objects.get(id=request.POST['bid'])
    bid.price = request.POST['price']
    bid.scope = request.POST['scope']
    bid.save()
    return redirect(con_home)

def project_complete(request,proj_id):
    project=Project.objects.get(id=proj_id)
    bid=Bids.objects.get(id=project.bids.id)
    contractor=Contractors.objects.get(id=bid.contractor.id)
    customer=Customer.objects.get(id=project.customer.id)
    context={
        'project':project,
        'bid':bid,
        'contractor':contractor,
        'customer':customer
    }
    return(request,"project_complete.html",context)

def project_complete_review(request):
    Review.objects.create(
        rating= request.POST['rating'],
        recommend=request.POST['recommend'],
        comments=request.POST['comments'],
        customer=request.POST['customer'],
        contractor=request.POST['contractor'],
        end_date=request.POST['end_date']
    )
    return redirect(cus_home)

# def con_view_bid(request, id):
#     bid = Bid.objects.get(id=id)
#     context = {
#         "bid" : bid
#     }
#     return render(request, 'bid_form.html', context)

    







def cus_reg_form(request):
    return render(request, 'customer_reg.html')

def cus_register(request):
    errors = Customer.objects.cus_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(cus_reg_form)
    
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    cus = Customer.objects.create(
        fname = request.POST['fname'],
        lname = request.POST['lname'],
        email = request.POST['email'],
        city = request.POST['city'],
        state = request.POST['state'],
        zipcode = request.POST['zipcode'],
        password = pw_hash,
    )
    
    request.session['id'] = cus.id
    return redirect('/cus_home')

def cus_login(request):
    user_db = Customer.objects.filter(email=request.POST['email'])
    if user_db:
        log_user = user_db[0]

        if bcrypt.checkpw(request.POST['password'].encode(), log_user.password.encode()):
            request.session['id'] = log_user.id
            return redirect(cus_home)

    messages.error(request, 'Incorrect email or password.')
    return redirect(cus_reg_form)

def cus_home(request):
    cus = Customer.objects.get(id=request.session['id'])
    kola = Bid.objects.filter(accepted=True)
    project_to_exclude = [this.project.id for this in kola]
    context = {
        'customer': cus,
        'myopenproj' : Project.objects.filter(customer=cus).exclude(id__in=project_to_exclude)
    }
    return render(request, 'userpage.html', context)

def submit_project(request):
    cus = Customer.objects.get(id=request.session['id'])
    proj = Project.objects.create(
        title = request.POST['title'],
        location = request.POST['location'],
        measurements = request.POST['measurements'],
        description = request.POST['description'],
        customer = cus
    )
    return redirect(cus_home)

def project_info(request, id):
    cus = Customer.objects.get(id=request.session['id'])
    proj = Project.objects.get(id=id)
    context = {
        'project' : proj,
        'cutomer': cus
    }
    return render(request, 'project_info.html', context)

def add_img(request):
    proj = Project.objects.get(id=request.POST['proj'])
    pic = Proj_imgage.objects.create(
        image = request.FILES['image'],
        project = proj
    )
    return redirect(project_info, proj.id)

def cus_view_bid(request, id):
    cus = Customer.objects.get(id=request.session['id'])
    bid = Bid.objects.get(id=id)
    context = {
        'bid': bid,
        'cutomer': cus
    }
    return render(request, 'view_bid.html', context)

def accept_bid(request, id):
    bid = Bid.objects.get(id=id)
    bid.accepted= True
    bid.save()
    return redirect(cus_home)

def project_complete(request,proj_id):
    project=Project.objects.get(id=proj_id)
    bid=Bid.objects.get(id=project.bids.id)
    contractor=Contractor.objects.get(id=bid.contractor.id)
    customer=Customer.objects.get(id=project.customer.id)
    context={
        'project':project,
        'bid':bid,
        'contractor':contractor,
        'customer':customer
    }
    return(request,"project_complete.html",context)

def project_complete_review(request):
    Review.objects.create(
        rating= request.POST['rating'],
        recommend=request.POST['recommend'],
        comments=request.POST['comments'],
        customer=request.POST['customer'],
        contractor=request.POST['contractor']
    )
        # Need to add in updating status of the Project if that is required
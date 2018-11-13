from django.shortcuts import render, redirect
from Game.interface_control import AssetComunication as ACommunication
from Game.models import Wallet
from django.contrib.auth.decorators import login_required
from django.conf import settings
from Game.models import Transaction, Alarm, LoanOffer, Loan
from django.http import JsonResponse, HttpResponse


@login_required
def loggedin(request):
    return render(request, 'Game/loggedin.html')


@login_required
def game(request):
    return render(request, 'Game/game.html')


@login_required
def assets(request):
    asset_comunication = ACommunication(settings.API_URL)
    asset_list = [a.to_dict() for a in asset_comunication.get_assets()]
    context = {'assets': asset_list}

    # user info
    wallet = Wallet.get_info(request.user)
    context['value_wallet'] = wallet['value_wallet']
    context['liquid'] = wallet['liquid']

    if request.is_ajax():
        return JsonResponse(context)
    else:
        return render(request, 'Game/assets.html', context)


@login_required
def wallet(request):
    user = request.user
    wallet_info = Wallet.get_info(user)
    return render(request, 'Game/wallet.html', wallet_info)


@login_required
def transactions(request):
    user = request.user
    user_wallet = Wallet.objects.get(user=user)
    user_transactions = Transaction.get_info(user_wallet)
    return render(request, 'Game/transactions.html', user_transactions)


@login_required
def history(request, name):
    if request.method == 'POST':

        start = request.POST['start']
        end = request.POST['end']

        asset_comunication = ACommunication(settings.API_URL)
        prices = asset_comunication.get_asset_history(name, start, end)
        prices['name'] = name
        return render(request, 'Game/history.html', prices)
    else:
        return render(request, 'Game/select_dates.html')


@login_required
def ranking(request):
    users = []
    wallets = Wallet.objects.all()
    for w in wallets:
        users.append({'username': w.user.username,
                      'wallet': w.get_info(w.user)['value_wallet'],
                      'ranking': 1})
    users.sort(key=lambda k: k['wallet'], reverse=True)
    index = 0
    for u in users:
        index += 1
        u['ranking'] = index
    return render(request, 'Game/ranking.html', {'users': users})


@login_required
def alarms(request):
    if request.method == 'GET':
        wallet = Wallet.objects.get(user=request.user)
        return render(request, 'Game/alarms.html', Alarm.get_info(wallet))
    else:
        if request.POST['method'] == 'delete':
            wallet = Wallet.objects.get(user=request.user)
            Alarm.safe_delete(wallet=wallet, name=request.POST['name'],
                              atype=request.POST['type'],
                              price=request.POST['price'])
            return HttpResponse(status=200)


@login_required
def set_alarm(request):
    if request.method == 'POST':
        try:
            float(request.POST['threshold'])
        except ValueError:
            return HttpResponse(status=400, reason="Incorrect threshold value")
        if float(request.POST['threshold']) < 0:
            return HttpResponse(status=400, reason="Incorrect threshold value")
        elif not request.POST.getlist('asset'):
            return HttpResponse(status=400,
                                reason="You need to select at least one asset")
        else:
            wallet = Wallet.objects.get(user=request.user)
            return JsonResponse(Alarm.safe_save(wallet=wallet,
                                                price=request.POST[
                                                    'price'],
                                                aname=request.POST['asset'],
                                                threshold=request.POST[
                                                    'threshold'],
                                                atype=request.POST['type']))
    else:
        asset_comunication = ACommunication(settings.API_URL)
        asset_list = [a.to_dict() for a in asset_comunication.get_assets()]
        context = {'assets': asset_list}
        return render(request, 'Game/set_alarm.html', context)


@login_required
def set_loan_offer(request):
    if request.method == 'GET':
        # user info
        context = {}
        wallet = Wallet.get_info(request.user)
        context['value_wallet'] = wallet['value_wallet']
        context['liquid'] = wallet['liquid']
        return render(request, 'Game/loan_offer.html', context)
    else:
        loan = request.POST['liquid-amount']
        interest_rate = request.POST['interest-rate']
        days_due = request.POST['days-due']
        wallet = Wallet.objects.get(user=request.user)

        return render(request, 'Game/loan_offer.html', LoanOffer.safe_save(
            wallet=wallet, offered=loan, interest=interest_rate, days=days_due))


@login_required
def get_all_loan_offers(request):
    if request.method == 'GET':
        loan_offers = LoanOffer.objects.exclude(lender__user=request.user)
        loan_offers = list(
            filter(lambda lo: lo.offered_with_loans > 0, loan_offers))
        context = {'loan_offers': loan_offers}
        return render(request, 'Game/loan_offers.html', context)
    elif request.is_ajax():
        offer_id = int(request.POST['id'])
        loaned = float(request.POST['loaned'])
        offer = LoanOffer.objects.get(id=offer_id)
        borrower = Wallet.objects.get(user=request.user)
        Loan.safe_save(borrower=borrower, loaned=loaned, offer=offer)
        return HttpResponse(200, 'Your loan has been taken successfully')


@login_required
def get_taken_loans(request):
    if request.method == 'GET':
        taken = Loan.objects.filter(borrower__user=request.user)
        wallet_info = Wallet.get_info(request.user)
        context = {'taken': taken,
                   'liquid': wallet_info['liquid'],
                   'value_wallet': wallet_info['value_wallet']}
        return render(request, 'Game/taken_loans.html', context)

@login_required
def get_offered_loans(request):
    if request.method == 'GET':
        loan_offers = LoanOffer.objects.filter(lender__user=request.user)
        context = {'loan_offers': loan_offers}
        return render(request, 'Game/offered_loans.html', context)
    else:
        wallet = Wallet.objects.get(user=request.user)
        if request.POST['method'] == 'delete':
            return JsonResponse(
                LoanOffer.safe_delete(lender=wallet,
                                      id=request.POST['id']))
        if request.POST['method'] == 'modify':
            return JsonResponse(
                LoanOffer.safe_modification(lender=wallet,
                                            id=request.POST['id'],
                                            new_offer=request.POST[
                                                'new_offer']))

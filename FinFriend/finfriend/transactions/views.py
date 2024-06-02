from http.client import HTTPResponse
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import CreateView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Transactions
from .forms import DepositForm,WithdrawForm,LoanRequestForm
from .constants import TRANSACTION_TYPE,DEPOSIT,WITHDRAW,LOAN,LOAN_PAID
from django.contrib import messages
from django.http import HttpResponse
from datetime import datetime
from django.db.models import Sum
from django.shortcuts import get_object_or_404,render,redirect
from django.views import View
from django.urls import reverse_lazy

class TransactionCreateMixin(LoginRequiredMixin,CreateView):
    template_name= 'transactions/transaction_form.html'
    model_name=Transactions
    title=''
    success_url=reverse_lazy('transaction_report')
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account': self.request.user.account
        })
        return kwargs
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
        })
        return context

class DepositMoneyView(TransactionCreateMixin):
    form_class=DepositForm
    title='Deposit' #user j title dekhbe page ar tab ay

    def get_initial(self):
        initial={'transaction_type':DEPOSIT }
        return initial
    
    def form_valid(self, form):
        amount=form.cleaned_data.get('amount')
        account=self.request.user.account
        account.balance+=amount
        account.save(
            update_fields=['balance']
        )
        messages.success(self.request,f"{amount}tk was deposited successfully")
        return super().form_valid(form)

class WithdrawMoneyView(TransactionCreateMixin):
    form_class=WithdrawForm
    title='Withdraw Money'

    def get_initial(self):
        initial={'transaction_type':WITHDRAW}
        return initial
    
    def form_valid(self, form):
        amount=form.cleaned_data.get('amount')
        account=self.request.user.account
        account.balance-=amount
        account.save(
            update_fields=['balance']
        )
        messages.success(self.request,f"{amount}tk was withdrawn successfully")
        return super().form_valid(form)

class LoanRequestView(TransactionCreateMixin):
    form_class=LoanRequestForm
    title='Request For Loan'

    def get_initial(self):
        initial={'transaction_type':LOAN }
        return initial
    
    def form_valid(self, form):
        amount=form.cleaned_data.get('amount')
        current_loan_count=Transactions.objects.filter(account=self.request.user.account,transaction_type=LOAN,loan_approve=True).count()
        if current_loan_count >= 3:
            return HTTPResponse("You have exceeded the loan limit")
        
        messages.success(self.request,f"Loan Request of {amount}tk was sent successfully")
        return super().form_valid(form)
    
class TransactionReportView(LoginRequiredMixin,ListView):
    template_name='transactions/transaction_report.html'
    model=Transactions
    balance=0

    def get_queryset(self):
        queryset=super().get_queryset().filter(account=self.request.user.account)
        start_date_str=self.request.GET.get('start_date')
        end_date_str=self.request.GET.get('end_date')
        if start_date_str and end_date_str:
            start_date=datetime.strptime(start_date_str,"%Y-%m-%d").date()
            end_date=datetime.strptime(end_date_str,"%Y-%m-%d").date()
            queryset=queryset.filter(timestamp__date__gte=start_date,timestamp__date__lte=end_date)

            self.balance=Transactions.objects.filter(timestamp__date__gte=start_date,timestamp__date__lte=end_date).aggregate(Sum('amount'))['amount__sum']
        else:
            self.balance=self.request.user.account.balance
        return queryset.distinct()
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context.update({
            'account':self.request.user.account
        })
        return context

    
class PayLoanView(LoginRequiredMixin, View):
    def get(self, request, loan_id):
        loan = get_object_or_404(Transactions, id=loan_id)
        print(loan)
        if loan.loan_approve:
            user_account = loan.account
                # Reduce the loan amount from the user's balance
                # 5000, 500 + 5000 = 5500
                # balance = 3000, loan = 5000
            if loan.amount < user_account.balance:
                user_account.balance -= loan.amount
                loan.balance_after_transaction = user_account.balance
                user_account.save()
                loan.loan_approved = True
                loan.transaction_type = LOAN_PAID
                loan.save()
                return redirect('loan_list')
            else:
                messages.error(
            self.request,
            f'Loan amount is greater than available balance'
        )

        return redirect('loan_list')
            
class LoanListView(LoginRequiredMixin,ListView):
    model=Transactions
    template_name='transactions/loan_request.html'
    context_object_name="loans" #total loan list loans ay ache

    def get_queryset(self):
        user_account = self.request.user.account
        queryset=Transactions.objects.filter(account=user_account,transaction_type=LOAN)
        return queryset

             
        


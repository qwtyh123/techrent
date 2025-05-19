from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from goods.models import Categories



class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'TechRent - Главная'
        context['content'] = "Магазин аренды бытовой техники TechRent"
        return context


class AboutView(TemplateView):
    template_name = 'main/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'TechRent - О нас'
        context['content'] = "TechRent - О нас"
        context['text_on_page'] = "Добро пожаловать в наш магазин аренды техники! Мы — помогаем клиентам легко и удобно получать необходимое оборудование без необходимости его покупки. Наша миссия — предоставить широкий ассортимент современной техники в аренду по доступным ценам, обеспечивая высокий уровень сервиса и индивидуальный подход к каждому клиенту."
        return context
    
class PayView(TemplateView):
    template_name = 'main/pay.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'TechRent - О нас'
        context['content'] = "Оплата"
        context['text_on_page'] = "Мы предлагаем удобные и безопасные способы оплаты для наших клиентов. Вы можете оплатить аренду техники наличными при получении, а также воспользоваться безналичным расчетом через банковскую карту или электронные платежные системы. Все транзакции защищены современными средствами безопасности, что гарантирует конфиденциальность ваших данных. После подтверждения оплаты вы получите все необходимые документы и инструкции для получения арендованного оборудования. Мы стремимся сделать процесс оплаты максимально простым и прозрачным, чтобы вы могли сосредоточиться на реализации своих задач."


        return context
    
class ContactView(TemplateView):
    template_name = 'main/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'TechRent - О нас'
        context['content'] = "контакт"
        context['text_on_page'] = "Свяжитесь с нами — мы всегда готовы помочь"
        return context


from collections import Counter

from django.shortcuts import render

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter()
counter_click = Counter()


def index(request):
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing

    from_landing = request.GET.get('from-landing', None)

    if from_landing == 'original':
        counter_click.update({'original': 1})
        return render(request, 'index.html')

    elif from_landing == 'test':
        counter_click.update({'test': 1})
        return render(request, 'index.html')

    else:
        return render(request, 'index.html')








def landing(request):
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов

    arg = request.GET.get('ab-test-arg')
    if arg == 'original':
        counter_show.update({'show_original': 1})
        return render(request, 'landing.html')

    elif arg == 'test':
        counter_show.update({'show_test': 1})
        print(counter_show)
        return render(request, 'landing_alternate.html')




def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Для вывода результат передайте в следующем формате:
    try:
        print('TRY')
        stats_test = round(counter_click['test'] / counter_show['show_test'], 1)

    except ZeroDivisionError:
        stats_test = 'Не удалось вычислить'

    try:
        stats_original = round(counter_click['original'] / counter_show['show_original'], 1)
    except ZeroDivisionError:
        stats_original = 'Не удалось вычислить'

    return render(request, 'stats.html', context={
        'test_conversion': stats_test,
        'original_conversion': stats_original,
    })


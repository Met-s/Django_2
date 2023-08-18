from django import template

register = template.Library()

CENSOR_WORDS = ["театр", "Театр", "сведения", "Сведения",
                "момент",  "Момент", "морей", "Морей","даже", "Даже"
                ]


@register.filter()
def censor(value):
    for i in CENSOR_WORDS:
        value = value.replace(i, "*" * len(i))
    return f'{value}'

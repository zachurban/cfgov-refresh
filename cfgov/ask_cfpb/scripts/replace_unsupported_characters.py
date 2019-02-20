from ask_cfpb.models.pages import AnswerPage


unsupported = [u'\x92', u'\x93', u'\x94', u'\x96']


def fix(text):
    text = text.replace(u'\x92', "'")
    text = text.replace(u'\x93', '"')
    text = text.replace(u'\x94', '"')
    text = text.replace(u'\x96', '-')
    return text


def run():
    for page in AnswerPage.objects.all():
        fixed = False

        for string in unsupported:
            if string in page.question:
                page.question = fix(page.question)
                fixed = True
            if string in page.answer:
                page.answer = fix(page.answer)
                fixed = True
            if string in page.snippet:
                page.snippet = fix(page.snippet)
                fixed = True

        if fixed:
            page.save_revision().publish()

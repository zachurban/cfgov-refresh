
from ask_cfpb.models import AnswerPage


def run():
    for page in AnswerPage.objects.all():
        for category in page.answer_base.category.all():
            page.category.add(category)
        for subcategory in page.answer_base.subcategory.all():
            page.subcategory.add(subcategory)

        page.next_step = page.answer_base.next_step
        page.featured = page.answer_base.featured
        page.featured_rank = page.answer_base.featured_rank
        page.statement = page.answer_base.statement
        page.social_sharing_image = page.answer_base.social_sharing_image
        page.answer_id = page.answer_base.id

        if page.language == 'es':
            page.search_tags = page.answer_base.search_tags_es
            page.last_edited = page.answer_base.last_edited_es
        #     for related_question in page.answer_base.related_questions.all():
        #         page.related_questions.add(related_question.spanish_page)
        elif page.language == 'en':
            page.search_tags = page.answer_base.search_tags
            page.last_edited = page.answer_base.last_edited
        #     for related_question in page.answer_base.related_questions.all():
        #         page.related_questions.add(related_question.english_page)

        # page.save()
        revision = page.save_revision()
        revision.publish()

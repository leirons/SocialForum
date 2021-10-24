from profanity_filter import ProfanityFilter
import spacy

def change_all_bad_words(text):
    nlp = spacy.load('en_core_web_sm')
    profanity_filter = ProfanityFilter(nlps={'en': nlp})  # reuse spacy Language (optional)
    nlp.add_pipe(profanity_filter.spacy_component, last=True)
    r = profanity_filter.censor(text)
    return r

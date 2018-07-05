import json
import spacy
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, FormView, ListView

from ner_trainer.models import Entity, Phrase, PhraseEntity
from .forms import ModelTestForm


class EntityList(ListView):
    model = Entity
    template_name = 'entity_list.html'


class EntityCreate(CreateView):
    model = Entity
    template_name = 'entity_form.html'
    fields = ('name', 'label')
    success_url = reverse_lazy('entity-list')

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['name'].widget.attrs['v-model'] = 'name'
        form.fields['label'].widget.attrs['v-model'] = 'label'
        return form


class PhraseList(ListView):
    model = Phrase
    template_name = 'phrase_list.html'


class PhraseCreate(CreateView):
    model = Phrase
    template_name = 'phrase_form.html'
    fields = ('text',)
    success_url = reverse_lazy('phrase-list')


class PhraseListUntagged(PhraseList):
    def get_queryset(self):
        return Phrase.objects.filter(entities__isnull=True)


class PhraseDetail(DetailView):
    model = Phrase
    template_name = 'phrase_detail.html'


class ModelTestView(FormView):
    form_class = ModelTestForm
    template_name = 'model_test.html'

    def form_valid(self, form):
        nlp = spacy.load('spacy_model')
        text = form.cleaned_data['text']
        doc = nlp(text)
        phrase_entities = []
        entity_labels = [ent.label_ for ent in doc.ents]
        entities = Entity.objects.filter(label__in=entity_labels)
        for ent in doc.ents:
            phrase_entities.append({
                'entity': entities.filter(label=ent.label_).first(),
                'text': ent.text,
            })
        return render(self.request, 'model_test.html', context={
            'text': text,
            'form': form,
            'phrase_entities': phrase_entities,
        })


def set_phrase_entities(request, pk):
    phrase_id = pk
    data = json.loads(request.body)
    phrase = Phrase.objects.get(id=phrase_id)
    phrase_entities = []
    for e in data['entities']:
        entity = Entity.objects.get(label=e.pop('entity'))
        phrase_entity = PhraseEntity(
            phrase_id=phrase_id, start_index=e['start_index'], end_index=e['end_index']
        )
        phrase_entity.entity = entity
        phrase_entities.append(phrase_entity)
    # Remove old PhraseEntities
    phrase.entities.all().delete()
    # Add new PhraseEntities
    phrase.entities.bulk_create(phrase_entities)
    return JsonResponse({'ok': 1})

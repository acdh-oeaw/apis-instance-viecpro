from django.db.models import Q


def LegacyRelationTypeAutocompleteQueryset(model, query):
    return model.objects.filter(
        Q(label__icontains=query) | Q(label_reverse__icontains=query)
    )

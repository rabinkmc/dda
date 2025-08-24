from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST


from common.models import MetaData
from students.forms import MetaDataForm
from users.permissions import is_admin


@user_passes_test(is_admin)
def metadata_list(request):
    metadata_qs = MetaData.objects.all()
    query = request.GET.get("q")
    if query:
        metadata_qs = metadata_qs.filter(
            Q(key__icontains=query) | Q(value__icontains=query)
        )

    page_number = request.GET.get("page", 1)
    page_limit = request.GET.get("limit", 10)
    paginator = Paginator(metadata_qs, page_limit)
    page_obj = paginator.get_page(page_number)

    metadata = page_obj.object_list

    return render(
        request,
        "common/metadata_list.html",
        {"metadatas": metadata, "page_obj": page_obj},
    )


@user_passes_test(is_admin)
def metadata_detail(request, pk):
    metadata = get_object_or_404(MetaData, pk=pk)
    return render(request, "common/metadata_detail.html", {"metadata": metadata})


@user_passes_test(is_admin)
def metadata_create(request):
    form = MetaDataForm()
    if request.method == "POST":
        form = MetaDataForm(request.POST)
        if form.is_valid():
            MetaData.objects.create(
                key=form.cleaned_data["key"],
                value=form.cleaned_data["value"],
            )
            return redirect("common:metadata-list")
    return render(
        request, "common/metadata_form.html", {"form": form, "metadata": None}
    )


@user_passes_test(is_admin)
def metadata_update(request, pk):
    metadata = get_object_or_404(MetaData, pk=pk)
    if request.method == "POST":
        form = MetaDataForm(request.POST, instance=metadata)
        if form.is_valid():
            metadata.key = form.cleaned_data["key"]
            metadata.value = form.cleaned_data["value"]
            metadata.save()
            messages.success(request, "Metadata has been saved successfully!")
            return redirect("common:metadata-list")
    else:
        initial_data = {
            "key": metadata.key,
            "value": metadata.value,
        }
        form = MetaDataForm(initial=initial_data)
    return render(
        request, "common/metadata_form.html", {"form": form, "metadata": metadata}
    )


@user_passes_test(is_admin)
@require_POST
def metadata_delete(request, pk):
    metadata = get_object_or_404(MetaData, pk=pk)
    metadata.delete()
    messages.success(request, "Metadata has been deleted successfully!")
    return redirect("common:metadata-list")

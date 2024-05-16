
from django.contrib.auth.decorators import login_required
from django.core.checks import messages
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone

from discussion.models import Opinion
from ias.forms import OpinionForm
from ias.models import AI


@login_required(login_url='common:login')
def opinion_create(request, ai_id):
    ai = get_object_or_404(AI, pk=ai_id)

    if request.method == 'POST':
        comment_text = request.POST.get('comment')  # Assuming the name of the input field is 'comment'

        # Check if comment_text exists before creating the Opinion instance
        if comment_text:
            comment = Opinion.objects.create(
                ai=ai,
                opinion=comment_text,
                create_date=timezone.now(),
                author=request.user  # Assigning the logged-in user as the author
            )

            # Optionally, you can associate the logged-in user with the comment
            # comment.author = request.user
            # comment.save()

            return redirect('ias:ai_detail', ai_id=ai_id)
        else:
            # Handle case when comment is empty
            # You can add error handling or redirect to another page
            pass

    # Handle case when request method is not POST
    # You may need to render a form for submitting comments
    return redirect('ias:ai_detail', ai_id=ai_id)


@login_required(login_url='common:login')
def opinion_modify(request, opinion_id):
    opinion = get_object_or_404(Opinion, pk=opinion_id)
    if request.user != opinion.author:
        messages.error(request, 'No permission to modify')
        return redirect('ias:ai_detail', article_id=opinion.ai.id)
    if request.method == "POST":
        form = OpinionForm(request.POST, instance=opinion)
        if form.is_valid():
            opinion = form.save(commit=False)
            opinion.modify_date = timezone.now()
            opinion.save()
            return redirect('{}#input_{}'.format(
                resolve_url('ias:ai_detail', ai_id=opinion.ai.id), opinion.id
            ))
    else:
        form =  OpinionForm(instance=opinion)
    context = {'ai': opinion.ai, 'opinion': opinion, 'form': form}
    return render(request, 'discussion/opinion_form.html', context)


@login_required(login_url='common:login')
def opinion_delete(request, opinion_id):
    opinion = get_object_or_404(Opinion, pk=opinion_id)
    if request.user != opinion.author:
        messages.error(request, 'No permission to delete')
    else:
        opinion.delete()
    return redirect('ias:ai_detail', ai_id=opinion.ai.id)


@login_required(login_url='common:login')
def opinion_vote(request, opinion_id):
    opinion = get_object_or_404(Opinion, pk=opinion_id)
    if request.user == opinion.voter:
        messages.error(request, 'Not allowed to recommend your answer')
    else:
        opinion.voter.add(request.user)
    return redirect('{}#opinion{}'.format(
        resolve_url('ias:ai_detail', ai_id=opinion.ai.id), opinion.id
    ))
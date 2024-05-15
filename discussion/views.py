
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from discussion.models import Opinion
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

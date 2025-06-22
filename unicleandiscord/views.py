"""Views."""

from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse


@login_required
@permission_required("unicleandiscord.basic_access")
def index(request):
    return HttpResponse("Hello world!")

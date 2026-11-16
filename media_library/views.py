from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from .models import PostAttachment
def attachment(request, attachment_id):
    item = get_object_or_404(PostAttachment.objects.select_related('post'), pk=attachment_id)
    if not item.post.is_published and not item.post.can_manage(request.user): raise Http404
    try: handle = item.file.open('rb')
    except OSError: raise Http404
    inline = item.file_type.startswith('image/') or item.file_type == 'application/pdf'
    response = FileResponse(handle, as_attachment=not inline, filename=item.original_filename, content_type=item.file_type)
    response['X-Content-Type-Options'] = 'nosniff'
    response['Content-Security-Policy'] = "sandbox; default-src 'none'"
    response['Cache-Control'] = 'private, no-store'
    return response

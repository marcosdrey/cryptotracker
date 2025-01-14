def unread_notifications(request):
    if request.user.is_authenticated:
        return {
            'user_has_unread_notifications': request.user.notifications.filter(is_read=False).exists()
        }
    return {'user_has_unread_notifications': False}

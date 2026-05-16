from rest_framework.authentication import SessionAuthentication

class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    Custom authentication class that skips CSRF validation for API requests.
    Since our React app and Django app live on different ports, enforcing
    local CSRF over HTTP causes browser cookie policies to block requests.
    Our strict CORS settings currently protect us.
    """
    def enforce_csrf(self, request):
        return  # Returning nothing explicitly bypasses the check
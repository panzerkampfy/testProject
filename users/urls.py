from django.urls import path

from .views import RegistrationViewSet, FacebookLogin, GoogleLogin, VkLogin, GitHubLogin

urlpatterns = [
    path('registration/', RegistrationViewSet.as_view({'post': 'create'}), name='reg_new_user'),
    path('social_auth/facebook/', FacebookLogin.as_view(), name='fb_login'),
    path('social_auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('social_auth/vk/', VkLogin.as_view(), name='vk_login'),
    path('social_auth/github/', GitHubLogin.as_view(), name='github_login'),
]

from django.urls import path, re_path
from account.views import UserLoginView, UserProfileView, UserRegistrationView, activate, BlogCreateView, GetAllBlogs

# # from django.conf.urls import url
# blog_detail = BlogCreateView.as_view({
#     # 'get': 'retrieve',
#     'post': 'update',  # POST instead PUT
# })

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name="register"),
    path('login/', UserLoginView.as_view(), name="login"),
    path('profile/', UserProfileView.as_view(), name="profile"),
    re_path(r'^verifyuser/$', activate, name='verifyuser'),

    path('blog/', BlogCreateView.as_view()),
    path('blog/<int:pk>', BlogCreateView.as_view()),
    path('allblogs/', GetAllBlogs.as_view())
]

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import CustomUserCreate, BlacklistTokenView, profileUser, UserProfileImage, Getblogs, ProfileFatch, getProfileWithBlog, UploadBlog, DistroyBlog, DeleteProfile, getOtherProfileWithBlog,AddandRemoveLike
urlpatterns = [
    path('register/', CustomUserCreate.as_view(), name='register'),
    path('logout/', BlacklistTokenView.as_view(), name='logout'),
    path('logout/', BlacklistTokenView.as_view(), name='logout'),
    path('profiles/', profileUser.as_view(), name='profiles'),
    path('auth/profile/', ProfileFatch.as_view(), name='userprofile'),
    path('auth/profileblog/',getProfileWithBlog.as_view(), name='userwithblogprofile'),
    path('blogs/', Getblogs.as_view(), name='blogs'),
    path('updateimage/', UserProfileImage.as_view(), name='upadeteProfile'),
    path('postupload/', UploadBlog.as_view(), name='blogupload'),
    path('postdelete/<int:id>', DistroyBlog.as_view(), name='postdelete'),
    path('profiledelete/',DeleteProfile.as_view(),name="profiledelete"),
    path('getotherprofile/<str:username>',getOtherProfileWithBlog.as_view(),name="getotherprofile"),
    path('addremovelike/<int:id>',
         AddandRemoveLike.as_view(), name="addremovelike"),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
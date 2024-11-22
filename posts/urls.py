from django.urls import path
from .views import HomePageView, PostCreateView, PostDetailView, PostUpdateView, PostDeleteView, CreateCommentView, AddReactionView, PostsByTagView

app_name = 'posts'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path("post/create/", PostCreateView.as_view(), name="post_create"),
    path("<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path('<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path("<int:pk>/comment/", CreateCommentView.as_view(), name="create_comment"),
    path('<int:pk>/react/<str:reaction_type>/', AddReactionView.as_view(), name='add_reaction'),
    path("tag/<str:tag_name>/", PostsByTagView.as_view(), name="posts_by_tag"),
]

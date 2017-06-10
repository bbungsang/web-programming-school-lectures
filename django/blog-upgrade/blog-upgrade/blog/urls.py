from django.conf.urls import url
from . import views # 현재 디렉토리 blog/ 에서 views 파일 임포트

urlpatterns = [
    url(r'^$', views.post_list), # views 에서 post_list 라는 함수 자체를 호출
    url(r'^new/$', views.post_new, name='post_new'), # 새 포스팅
    url(r'^(?P<id>\d+)/$', views.post_detail, name='post_detail'), # 포스팅 보기
    url(r'^(?P<id>\d+)/edit/$', views.post_edit, name='post_edit'), # 포스팅 수정
    url(r'^(?P<id>\d+)/delete/$', views.post_delete, name='post_delete'), # 포스팅 삭제
    url(r'^(?P<id>\d+)/comments/$', views.comment_list, name='comment_list'), # 댓글 목록
    url(r'^(?P<post_id>\d+)/comments/(?P<id>\d+)/edit/$', views.comment_edit, name='comment_edit'), # 댓글 수정
    url(r'^(?P<post_id>\d+)/comments/(?P<id>\d+)/delete/$', views.comment_delete, name='comment_delete'), # 댓글 삭제
]
from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content','image']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content','image']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'placeholder': '添加您的评论...'}),
        }
        labels = {
            'content': '',  # 隐藏content标签
            'image': '上传图片'  # 设置image标签为中文
        }
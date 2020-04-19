
# Create your models here.
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.html import strip_tags
import markdown

class Category(models.Model):
	"""
    django 要求模型必须继承 models.Model 类。
    Category 只需要一个简单的分类名 name 就可以了。
    CharField 指定了分类名 name 的数据类型，CharField 是字符型，
    CharField 的 max_length 参数指定其最大长度，超过这个长度的分类名就不能被存入数据库。
    当然 django 还为我们提供了多种其它的数据类型，如日期时间类型 DateTimeField、整数类型 IntegerField 等等。
    django 内置的全部类型可查看文档：
    https://docs.djangoproject.com/en/2.2/ref/models/fields/#field-types
    """
	name = models.CharField(max_length=100)
	class Meta:
		verbose_name = '分类'
		verbose_name_plural = verbose_name
		
	def __str__(self):
		return self.name
	
class Tag(models.Model):
	"""
    标签 Tag 也比较简单，和 Category 一样。
    再次强调一定要继承 models.Model 类！
    """
	name = models.CharField(max_length=100)
	class Meta:
		verbose_name = '标签'
		verbose_name_plural = verbose_name
	def __str__(self):
		return self.name
	
class Post(models.Model):
	"""
    文章的数据库表稍微复杂一点，主要是涉及的字段更多。
    """
	
	#文章标题
	title = models.CharField('标题',max_length=70)
	
	#文章正文 使用TextField
	#存储较短的字符串可用CharField, 但对于文章的正文来说可能会是一大段文本，因此使用TextField来存储大段文本
	body = models.TextField('正文')
	
	#存储时间字段用DateTimeField
	created_time = models.DateTimeField('创建时间',default=timezone.now)
	modified_time = models.DateTimeField('修改时间')
	
	#默认情况下 CharField 要求我们必须存入数据，否则就会报错
	#指定 CharField 的 blank=True 参数值后就可以允许空值了
	excerpt = models.CharField('摘要',max_length=200,blank=True)
	#models.CASCADE 以为级联删除 及某个分类被删除时, 该分类下的所有文章也删除
	category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)
	#标签与文章是多对多
	tags = models.ManyToManyField(Tag,verbose_name='标签', blank=True)
	#文章与作者是一对多
	author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
	
	#将admin界面对应字段汉化
	class Meta:
		verbose_name = '文章'
		verbose_name_plural = verbose_name
	
	def __str__(self):
		return self.title
	#每一个model都有一个save方法 在model被save之前将modified这个值修改
	
	def save(self,*args,**kwargs):
		self.modified_time = timezone.now()
		
		# 首先实例化一个 Markdown 类，用于渲染 body 的文本。
        # 由于摘要并不需要生成文章目录，所以去掉了目录拓展。
		if(self.excerpt==''):
			md = markdown.Markdown(extensions=[
			'markdown.extensions.extra',
			'markdown.extensions.codehilite',
			])
		
			# 先将 Markdown 文本渲染成 HTML 文本
			# strip_tags 去掉 HTML 文本的全部 HTML 标签
			# 从文本摘取前 54 个字符赋给 excerpt
			self.excerpt = strip_tags(md.convert(self.body))[:54]
		super().save(*args, **kwargs)
	
	# 获得要显示文章的url 主要是区分是哪篇文章 所以传入了pk 即 id
	def get_absolute_url(self):
		return reverse('blog:detail',kwargs={'pk':self.pk})
	
		
	
		
	
	
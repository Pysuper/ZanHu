'''
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

# TODO: 信号量机制
from django.db.models.signals import post_save


class Index(models.Model):
    """首页--通用模型类"""
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        """
        TODO
            每当后面三个模型类中有数据生成的时候，都会在这里创建一条数据
            最后在排序的时候，使用这里的数据进行排序，就能对不同模块的数据进行排序了
        """
        ordering = ["-pub_date"]

    # TODO：问题2：如何在调用基类的时候，获取到其他三张表中的数据
    @property
    def content(self):
        return self.content_object.content


class News(models.Model):
    """动态"""
    content = models.CharField(max_length=255)
    pub_date = models.DateTimeField(auto_now_add=True)

    # index = GenericRelation(Index)  # 关联到通用模型类的表

    # TODO: 问题1 ：如何在其他的模型类中，生成一条数据的时候，在基类中也创建一条数据（代码复用性）
    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     content_type = ContentType.objects.get_or_create(self)
    #     # self.index.get_or_create(pub_data=self.pub_date)
    #     Index.objects.get_or_create(
    #         content_type=content_type,
    #         object_id=self.id,
    #         pub_date=self.pub_date
    #     )


class Article(models.Model):
    """文章"""
    title = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    # index = GenericRelation(Index)

    #
    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     content_type = ContentType.objects.get_or_create(self)
    #     # self.index.get_or_create(pub_data=self.pub_date)
    #     Index.objects.get_or_create(
    #         content_type=content_type,
    #         object_id=self.id,
    #         pub_date=self.pub_date
    #     )


class Question(models.Model):
    """问题"""
    title = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    # index = GenericRelation(Index)

    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     content_type = ContentType.objects.get_or_create(self)
    #     # self.index.get_or_create(pub_data=self.pub_date)
    #     Index.objects.get_or_create(
    #         content_type=content_type,
    #         object_id=self.id,
    #         pub_date=self.pub_date
    #     )


def create_index(sender, instance, **kwargs):
    """
    这里使用信号量机制，每当完成一次创建，就关联到ContentType中创建一条数据
    sender: 发送者
    instance：实例对象
    """
    if "created" in kwargs:  # TODO： 每次创建的时候触发
        content_type = ContentType.objects.get_for_model(instance)
        Index.objects.get_or_create(
            content_type=content_type,
            object_id=instance.id,
            pub_date=instance.pub_date
        )


# 固定写法
post_save.connect(create_index, sender=News)
post_save.connect(create_index, sender=Article)
post_save.connect(create_index, sender=Question)

'''

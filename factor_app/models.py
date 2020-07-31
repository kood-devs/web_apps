from django.db import models


# Create your models here.
class PortfolioModel(models.Model):
    # model identifiers
    title = models.CharField('登録ポートフォリオ', max_length=100)

    # weight
    weight_DB = models.FloatField('国内債券', default=0.15)
    weight_DE = models.FloatField('国内株式', default=0.15)
    weight_FB = models.FloatField('先進国債券', default=0.15)
    weight_FE = models.FloatField('先進国株式', default=0.15)
    weight_EB = models.FloatField('新興国債券', default=0.10)
    weight_EE = models.FloatField('新興国株式', default=0.10)
    weight_DR = models.FloatField('国内リート', default=0.10)
    weight_FR = models.FloatField('先進国リート', default=0.10)

    def __str__(self):
        return self.title

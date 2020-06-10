from django.db import models
from django.utils import timezone


class MarketForecastModel(models.Model):
    # model identifiers
    title = models.CharField('モデル名', max_length=100)
    model_defined_date = models.DateField('最終更新日', default=timezone.now)

    # model settings
    forecast_model = models.CharField(
        'アルゴリズム', max_length=100, default='binomial logit')
    train_num = models.IntegerField('学習データ数', default=2600)

    # model result
    weather = models.CharField('予報', max_length=100, default='cloudy')

    def __str__(self):
        return self.title

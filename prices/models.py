from django.db import models
from django.utils.translation import ugettext_lazy as _

TARIFFS = (
	(0, _("General")),
	(1, _("Night")),
	(2, _("Electric vehicle")),
)

class Price(models.Model):
	tariff = models.PositiveIntegerField(_("tariff"), choices=TARIFFS,
		default=0)
	date = models.DateField(_("date"))
	hour = models.PositiveIntegerField(_("hour"), default=0)
	euro = models.FloatField(_("EUR/kwh"))

	class Meta:
		ordering = ['-date', '-hour',]
		verbose_name = _("price")
		verbose_name_plural = _("prices")

	def __unicode__(self):
		return u"%s(%s)" % (self.date, self.hour)

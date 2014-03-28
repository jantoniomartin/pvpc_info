from datetime import date, datetime

from django.conf import settings
from django.db.models import Max, Min, ObjectDoesNotExist
from django.views.generic import TemplateView

from prices.models import Price

ENERGY_TAX = getattr(settings, 'KWH_ENERGY_TAX')


class HomeView(TemplateView):
	template_name = "prices/home.html"

	def get_context_data(self, **kwargs):
		ctx = super(HomeView, self).get_context_data(**kwargs)
		hour = datetime.now().hour
		prices = Price.objects.filter(date = date.today()).order_by(
			'hour', 'tariff').extra(
			select={'taxed': "euro * %s" % ENERGY_TAX}
		)
		try:
			current_general = prices.get(hour=hour, tariff=0)
		except ObjectDoesNotExist:
			self.template_name = 'prices/nodata.html'
			return ctx

		lowest = [0, 0, 0]
		highest = [0, 0, 0]
		table = []
		h = -1
		for p in prices:
			if p.hour != h:
				table.append([])
				h = p.hour
			table[p.hour].append(p.taxed)
			if lowest[p.tariff] == 0 or p.taxed < lowest[p.tariff]:
				lowest[p.tariff] = p.taxed
			if p.taxed > highest[p.tariff]:
				highest[p.tariff] = p.taxed

		cheap = []
		expensive = []
		for i in range(0, 3):
			cheap.append(lowest[i] + (highest[i] - lowest[i]) / 3)
			expensive.append(highest[i] - (highest[i] - lowest[i]) / 3)

		hour_history_qs = Price.objects.filter(
			tariff=0,
			hour=hour,
			date__lte=date.today()
				).order_by('date').extra(
					select={'taxed': "euro * %s" % ENERGY_TAX})[:8]

		hour_history = []
		for price in hour_history_qs:
			hour_history.append([price.date.day, "%.5f" % price.taxed])

		analytics_id = getattr(settings, 'ANALYTICS_ID', None)
		
		ctx.update({
			'hour': hour,
			'current': current_general.taxed,
			'table': table,
			'tax': (ENERGY_TAX - 1) * 100,
			'lg': cheap[0],
			'ln': cheap[1],
			'lv': cheap[2],
			'hg': expensive[0],
			'hn': expensive[1],
			'hv': expensive[2],
			'hour_history': hour_history,
			'analytics_id': analytics_id,
			})
		

		return ctx

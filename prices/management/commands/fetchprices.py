import cStringIO
from datetime import date, timedelta
import pycurl
import re

from django.core.management.base import NoArgsCommand, CommandError

from prices.models import *

class Command(NoArgsCommand):
	help = "Gets the prices from REE."

	def handle_noargs(self, **options):
		tomorrow = date.today() + timedelta(1)
		date1 = tomorrow.strftime("%Y%m%d")
		date2 = tomorrow.strftime("%d/%m/%Y")

		post = "TIPO=D&limiteSuperior=0&nombreBase=PVPC&unidad=&agregacion=DD&nombreFichero=PVPC_DD_%(date1)s&fechaSolicitada=%(date1)s&accion_hc=carga&forzarISO=true&FECHA_PVPC=%(date2)s" % {
				'date1': date1,
				'date2': date2,
				}

		buf = cStringIO.StringIO()

		c = pycurl.Curl()
		c.setopt(
		c.URL, 'http://www.esios.ree.es/web-publica/paginas/consultas/query.jsp'
		)
		c.setopt(c.POST, 1)
		c.setopt(c.POSTFIELDS, post)
		c.setopt(c.WRITEFUNCTION, buf.write)
		c.perform()

		cell = re.compile('[0-9]{1},[0-9]{5}')

		tds = cell.findall(buf.getvalue())

		buf.close()

		for i in range(0, 72):
			if i == 0 or i % 3 == 0:
				tariff = 0
			elif i == 1 or (i - 1) % 3 == 0:
				tariff = 1
			else:
				tariff = 2
			Price.objects.create(
				tariff = tariff,
				date = tomorrow,
				hour = i / 3,
				euro = float(tds[i].replace(',','.'))
			)


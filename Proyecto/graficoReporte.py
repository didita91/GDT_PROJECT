__author__ = 'tere'
from reportlab.graphics.shapes import Drawing, String
from reportlab.graphics.charts.barcharts import HorizontalBarChart
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.lib import colors
from app.models import *

def MyBarChartDrawing(proyecto_id):
        """
Dibuja el grafico de tiempo estimado para el reporte, dentro de un proyecto
:param proyecto_id: identificador de proyecto
:return:
"""

        Dra = Drawing()
        proyecto_actual= Proyecto.objects.get(id=proyecto_id)
        sprint_del_proyecto = Sprint.objects.filter(proyecto = proyecto_id)
        print sprint_del_proyecto
        us_sprint_proyecto = UsSprint.objects.filter(proyecto = proyecto_id)
        print us_sprint_proyecto
        print 'ID DEL PROYECTO'
        print proyecto_id
        cantSprints = sprint_del_proyecto.count()
        print 'ESTE PROYECTO TIENE SPRINTS ='
        print cantSprints
        Datos =[]
        Nombres = []

        for tsprint in sprint_del_proyecto:
                Datos.append(tsprint.duracion)
                Nombres.append('Sprint '+ str(tsprint.nro_sprint))
        print Nombres
        width=400
        height=200
        Dra.height=height
        Dra.width=width
        Dra.add(HorizontalBarChart(), name='chart')
        Dra.add(String(100,180,'Duracion de Sprints del Proyecto en semanas'), name='title')

        #set any shapes, fonts, colors you want here.  We'll just
        #set a title font and place the chart within the drawing
        Dra.chart.x = 50
        Dra.chart.y = 20
        Dra.chart.width = Dra.width - 20
        Dra.chart.height = Dra.height - 40
        Dra.chart.valueAxis.valueMin = 0
        Dra.chart.valueAxis.valueMax = cantSprints+2
        Dra.chart.valueAxis.valueStep = 1
        Dra.chart.categoryAxis.categoryNames = Nombres
        Dra.chart.bars[0].fillColor = colors.darkred
        #h=HorizontalBarChart()
        #h.strokeColor()



        Dra.title.fontName = 'Helvetica-Bold'
        Dra.title.fontSize = 12
        print 'ACA ESTA LA LISTA PARA TU BARRA'
        print Datos

        Dra.chart.data = [Datos]
        print Dra.chart.data
        Dra.save(formats=['png'],outDir='.',fnRoot='barchart')
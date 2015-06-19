#! /bin/bash
#######################################
### Script para realizar las pruebas###
### y Despligue de documentacion    ###
#######################################
clear
######################################
###    DESPLEGAR DOCUMENTACION	   ###
######################################
echo 'Generando html de documentacion'
sleep 1s
export DJANGO_SETTINGS_MODULE=gdt_project.settings
sudo pydoc -w /app/views.py
sleep 1s 
echo '...'
sudo pydoc -w /Proyecto/views.py
sleep 1s
echo 'listo'
sleep 1s
gnome-open file:///$HOME/views.html

#echo 'Correr pruebas'
#sudo python manage.py test


#! /bin/bash
#######################################
### Script para realizar las pruebas###
### y Despligue de documentacion    ###
#######################################
clear
######################################
###    DESPLEGAR DOCUMENTACION	   ###
######################################
source /home/dferreira/entornoIS2/bin/activate
echo 'Generando html de documentacion'
sleep 1s
export DJANGO_SETTINGS_MODULE=gdt_project.settings

pydoc -w app/views.py Proyecto/views.py
echo '...'
sleep 1s
echo 'listo'
sleep 1s

#gnome-open file:////views.html
source /home/dferreira/entornoIS2/bin/activate

echo 'Corriendo pruebas'
sudo python manage.py test


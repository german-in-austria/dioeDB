# command to run script
# python3 manage.py shell < test_scripts/insert_data.py

from PersonenDB.models import tbl_orte
from mioeDB.models import tbl_adm_lvl, tbl_sprache, tbl_mioe_orte, tbl_zeit

# clean tables
tbl_adm_lvl.objects.all().delete()
tbl_sprache.objects.all().delete()
tbl_orte.objects.all().delete()
tbl_zeit.objects.all().delete()

# check if tables are empty
tbl_adm_lvl.objects.all()

# add some data
# administrative lvl
q = tbl_adm_lvl(pk=4,name="Bundesland")
q.save()
q = tbl_adm_lvl(pk=6, name="Politischer Bezirk")
q.save()
q = tbl_adm_lvl(pk=8, name="Gemeinde")
q.save()
q = tbl_adm_lvl(pk=9, name="Ort")
q.save()
q = tbl_adm_lvl(pk=10, name="Stadtteile")
q.save()

# sprachen
q = tbl_sprache(sprache="Deutsch")
q.save()
q = tbl_sprache(sprache="B-M-S")
q.save()
q = tbl_sprache(sprache="Andere")
q.save()

# zeiten
q = tbl_zeit(zeitpunkt=1880)
q.save()
q = tbl_zeit(zeitpunkt=1890)
q.save()
q = tbl_zeit(zeitpunkt=1900)
q.save()


# check if tables got some data
tbl_adm_lvl.objects.all()
tbl_adm_lvl.objects.filter(id=6)
tbl_sprache.objects.all()
tbl_sprache.objects.filter(id=2)




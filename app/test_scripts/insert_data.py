# command to run script
# python3 manage.py shell < test_scripts/insert_data.py

from PersonenDB.models import tbl_orte
from mioeDB.models import (
  tbl_adm_lvl,
  tbl_sprache,
  tbl_zeit,
  tbl_religion,
  tbl_schultyp,
  )

# clean tables
tbl_adm_lvl.objects.all().delete()
tbl_sprache.objects.all().delete()
tbl_zeit.objects.all().delete()
tbl_religion.objects.all().delete()
tbl_schultyp.objects.all().delete()

# other tables also
tbl_orte.objects.all().delete()

print("\nSuccess. All tables cleared.")

# add some data to tables

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

# religionen
q = tbl_religion(relig_name="Christentum")
q.save()
q = tbl_religion(relig_name="Buddhismus")
q.save()
q = tbl_religion(relig_name="Judentum")
q.save()

# schultypen
q = tbl_schultyp(schultyp="I")
q.save()
q = tbl_schultyp(schultyp="II")
q.save()
q = tbl_schultyp(schultyp="VII")
q.save()

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

# check if tables got some data
if (
  tbl_adm_lvl.objects.all()
  and tbl_sprache.objects.all()
  and tbl_zeit.objects.all()
  and tbl_religion.objects.all()
  and tbl_schultyp.objects.all()
  ):
  print("\nSuccess. All tables are filled with data.")
else:
  print("\nError. Please check db. Some of tables are empty")





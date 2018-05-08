from django.db import models
from PersonenDB.models import tbl_orte

# Create your models here.
# m = maskulin, f = feminin, n = neutrum(default)
models.options.DEFAULT_NAMES += ('verbose_genus',)
# Zusätzliche "data-fx-"-Felder für Filter
models.options.DEFAULT_NAMES += ('kategorienListeFilter', 'kategorienListeFXData',)
# Liste der Felder mit IPA Auswahlfeld
models.options.DEFAULT_NAMES += ('ipa',)

class tbl_adm_lvl(models.Model):
  name = models.CharField(
    max_length=255,
    verbose_name="Administrative Einheit")

  def __str__(self):
    return self.name

  class Meta:
    db_table = "MioeDB_tbl_adm_lvl"
    verbose_name = "Administrative Einheit"
    verbose_name_plural = "Administrative Einheit"
    verbose_genus = "f"
    ordering = ('name',)
    default_permissions = ()

class tbl_mioe_orte(models.Model):
  id_ort = models.ForeignKey(
    'PersonenDB.tbl_orte',
    on_delete=models.CASCADE, verbose_name="Ort"
  )
  gid = models.IntegerField(blank=True, null=True, verbose_name="REDE-ID")
  adm_lvl = models.ForeignKey(
    'tbl_adm_lvl',
    on_delete=models.CASCADE, verbose_name="Administrative Einheit"
  )
  histor = models.BooleanField(default=False,verbose_name="Historischer Ort")

  def __str__(self):
    return "{}, {}, Historisch ({})".format(
      self.gid,
      self.adm_lvl.name,
      self.histor,
    )

  class Meta:
    db_table = "MioeDB_tbl_orte"
    verbose_name = "Ort"
    verbose_name_plural = "Orte"
    verbose_genus = "m"
    ordering = ('gid',)
    default_permissions = ()

class tbl_sprache(models.Model):
  sprache = models.CharField(max_length=255, verbose_name="Sprache")

  def __str__(self):
    return self.sprache

  class Meta:
    db_table = "MioeDB_tbl_sprache"
    verbose_name = "Sprache"
    verbose_name_plural = "Sprachen"
    verbose_genus = "f"
    ordering = ('sprache',)
    default_permissions = ()

class tbl_zeit(models.Model):
  zeitpunkt = models.DateField(verbose_name="Zeitpunkt")

  def __str__(self):
    return str(self.zeitpunkt)

  class Meta:
    db_table = "MioeDB_tbl_zeit"
    verbose_name = "Zeitpunkt"
    verbose_name_plural = "Zeitpunkte"
    verbose_genus = "m"
    ordering = ('zeitpunkt',)
    default_permissions = ()

class tbl_religion(models.Model):
  relig_name = models.CharField(max_length=255, verbose_name="Religion")

  def __str__(self):
    return str(self.relig_name)

  class Meta:
    db_table = "MioeDB_tbl_religion"
    verbose_name = "Religion"
    verbose_name_plural = "Religionen"
    verbose_genus = "f"
    ordering = ('relig_name',)
    default_permissions = ()

class tbl_schultyp(models.Model):
  schultyp = models.CharField(max_length=255, verbose_name="Schultyp")

  def __str__(self):
    return str(self.schultyp)

  class Meta:
    db_table = "MioeDB_tbl_schultyp"
    verbose_name = "Schultyp"
    verbose_name_plural = "Schultypen"
    verbose_genus = "m"
    ordering = ('schultyp',)
    default_permissions = ()

class tbl_art_daten(models.Model):
  art_daten = models.CharField(max_length=255, verbose_name="Art von Daten")
  id_sprache = models.ForeignKey(
    'tbl_sprache',
    on_delete=models.CASCADE, verbose_name="Sprache"
  )

  def __str__(self):
    return "{} - {}".format(self.art_daten, self.id_sprache.sprache,)

  class Meta:
    db_table = "MioeDB_tbl_art_daten"
    verbose_name = "Art von Daten"
    verbose_name_plural = "Arten von Daten"
    verbose_genus = "f"
    ordering = ('art_daten',)
    default_permissions = ()

class tbl_mioe_personen(models.Model):
  vorname = models.CharField(max_length=255, verbose_name="Vorname")
  nachname = models.CharField(max_length=255, verbose_name="Nachname")
  funktion = models.CharField(
    blank=True, null=True,
    max_length=255, verbose_name="Funktion")
  geburtsort_orig = models.CharField(
    blank=True, null=True,
    max_length=255, verbose_name="Geburtsort Original")
  geburtsort = models.ForeignKey(
    'tbl_mioe_orte',
    on_delete=models.CASCADE, verbose_name="Geburtsort"
  )

  def __str__(self):
    return "{} - {}".format(self.vorname, self.nachname,)

  class Meta:
    db_table = "MioeDB_tbl_mioe_personen"
    verbose_name = "Mioe Person"
    verbose_name_plural = "Mioe Personen"
    verbose_genus = "f"
    ordering = ('nachname',)
    default_permissions = ()

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

class tbl_wb(models.Model):
  num_wb = models.IntegerField(verbose_name="Wenkerbogen Nummer")
  typ_wb = models.CharField(max_length=1, verbose_name="Wenkerbogen Typ")
  datierung = models.DateField(
    blank=True, null=True, verbose_name="Datierung"
  )
  id_wenkerort = models.ForeignKey(
    'tbl_mioe_orte',
    on_delete=models.CASCADE, verbose_name="Wenkerort"
  )
  schulort_original = models.CharField(
    max_length=255, verbose_name="Schulort (original)",
  )
  id_lehrer = models.ForeignKey(
    'tbl_mioe_personen',
    blank=True, null=True, on_delete=models.CASCADE, verbose_name="Lehrer"
  )
  uebersetzt_von = models.CharField(
    max_length=255, blank=True, null=True, verbose_name="Uebersetzt von"
  )
  uebersetzt_klass = models.CharField(
    max_length=255, blank=True, null=True, verbose_name="Uebersetzt Klass"
  )
  alter_geschl_uebesetzer = models.CharField(
    max_length=255, blank=True, null=True,
    verbose_name="Alter, Geschlecht Uebesetzer"
  )
  alter_geschl_lehrer = models.CharField(
    max_length=255, blank=True, null=True,
    verbose_name="Alter, Geschlecht Lehrer"
  )
  alter_uebesetzer = models.IntegerField(
    blank=True, null=True,
    verbose_name="Alter Uebesetzer"
  )
  geburtsdatum_uebersetzer = models.DateField(
    blank=True, null=True,
    verbose_name="Geburtsdatum Uebesetzer"
  )
  geschlecht_uebersetzer = models.CharField(
    max_length=255, blank=True, null=True,
    verbose_name="Geschlecht Uebesetzer"
  )
  informationen_zu = models.CharField(
    max_length=255, blank=True, null=True,
    verbose_name="Informationen zu"
  )
  andere_sprache_orig = models.CharField(
    max_length=255, blank=True, null=True,
    verbose_name="Andere Sprache (original)"
  )
  andere_sprachen = models.BooleanField(verbose_name="Anderen Sprachen")
  welche_sprachen = models.CharField(
    max_length=255, blank=True, null=True,
    verbose_name="Welche Sprachen"
  )
  sprachen_verhaeltnis = models.CharField(
    max_length=255, blank=True, null=True,
    verbose_name="Sprachen Verhaeltnis"
  )
  kommentar_wb = models.CharField(
    max_length=255, blank=True, null=True,
    verbose_name="Kommentar Wenkerbogen"
  )
  kommentar_wiss = models.CharField(
    max_length=255, blank=True, null=True,
    verbose_name="Kommentar Wiss."
  )
  geprueft = models.BooleanField(verbose_name="Geprueft")

  def __str__(self):
	  return "{} ({})".format(self.num_wb, self.id_wenkerort.id_ort.ort_namekurz)

  class Meta:
    db_table = "MioeDB_tbl_wb"
    verbose_name = "Wenkerbogen"
    verbose_name_plural = "Wenkerbögen"
    verbose_genus = "m"
    ordering = ('num_wb',)
    default_permissions = ()

class tbl_wb_sprache(models.Model):
  id_wb = models.ForeignKey(
    'tbl_wb',
    on_delete=models.CASCADE, verbose_name="Wenkerbogen"
  )
  id_sprache = models.ForeignKey(
    'tbl_sprache',
    on_delete=models.CASCADE, verbose_name="Sprache"
  )
  anteil = models.FloatField(verbose_name="Anteil")

  def __str__(self):
    return "{} - {}%".format(self.id_sprache.sprache, self.anteil)

  class Meta:
    db_table = "MioeDB_tbl_wb_sprache"
    verbose_name = "Wenkerbogen Sprache"
    verbose_name_plural = "Wenkerbogen Sprachen"
    verbose_genus = "f"
    ordering = ('id_wb',)
    default_permissions = ()

class tbl_quelle(models.Model):
  wenkerbogen = models.ForeignKey(
    'tbl_wb',
    blank=True, null=True,
    on_delete=models.CASCADE, verbose_name="Wenkerbogen"
  )
  literatur = models.CharField(
    max_length=255, blank=True, null=True,
    verbose_name="Literatur"
  )

  def __str__(self):
    if self.wenkerbogen is not None:
      return "wb: {}".format(self.wenkerbogen.num_wb)
    else:
      return "lit: {}".format(self.literatur)

  class Meta:
    db_table = "MioeDB_tbl_quelle"
    verbose_name = "Quelle"
    verbose_name_plural = "Quellen"
    verbose_genus = "f"
    ordering = ('id',)
    default_permissions = ()

class tbl_wb_auch_fuer(models.Model):
  id_wb = models.ForeignKey(
    'tbl_wb',
    on_delete=models.CASCADE, verbose_name="Wenkerbogen")
  id_wbort = models.ForeignKey(
    'tbl_mioe_orte',
    on_delete=models.CASCADE, verbose_name="Wenkerort")
  id_lehrer = models.ForeignKey(
    'tbl_mioe_personen',
    on_delete=models.CASCADE, verbose_name="Lehrer")
  kommentar_wb = models.CharField(
    max_length=255, blank=True, null=True,
    verbose_name="Kommentar Wenkerbogen"
  )
  kommentar_wiss = models.CharField(
    max_length=255, blank=True, null=True,
    verbose_name="Kommentar Wiss."
  )

  def __str__(self):
    return "{}: {}, {}".format(
      self.id_wb.num_wb, self.id_wbort.ort_namekurz, self.id_lehrer.nachname,
    )

  class Meta:
    db_table = "MioeDB_tbl_wb_auch_fuer"
    verbose_name = "Wenkerbogen auch fuer"
    verbose_name_plural = "Wenkerbögen auch fuer"
    verbose_genus = "m"
    ordering = ('id_wb',)
    default_permissions = ()

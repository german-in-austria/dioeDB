from django.db import models
from PersonenDB.models import tbl_orte
from datetime import datetime

# Create your models here.
# m = maskulin, f = feminin, n = neutrum(default)
models.options.DEFAULT_NAMES += ('verbose_genus',)
# Zusätzliche "data-fx-"-Felder für Filter
models.options.DEFAULT_NAMES += ('kategorienListeFilter', 'kategorienListeFXData',)
# Liste der Felder mit IPA Auswahlfeld
models.options.DEFAULT_NAMES += ('ipa',)

#TODO what to cascade and what not? best practice
#TODO class Meta default permissions? what must be there?

# --- 1 level tables---
# names of administrativ entities
class tbl_adm_lvl(models.Model):
  name = models.CharField(
    max_length=255,
    verbose_name="Administrative Einheit")

  def __str__(self):
    return "{}".format(self.name)

  class Meta:
    db_table = "MioeDB_tbl_adm_lvl"
    verbose_name = "Administrative Einheit"
    verbose_name_plural = "Administrative Einheit"
    verbose_genus = "f"
    ordering = ('name',)
    default_permissions = ()

# type of the variations
class tbl_variet_typ(models.Model):
  typ_name = models.CharField(max_length=255, verbose_name="Varietätstyp")

  def __str__(self):
    return "{}".format(self.typ_name)

  class Meta:
    db_table = "MioeDB_tbl_variet_typ"
    verbose_name = "Varietätstyp"
    verbose_name_plural = "Varietätstype"
    verbose_genus = "m"
    ordering = ('typ_name',)
    default_permissions = ()

# date attributes
class tbl_zpunkt_attr(models.Model):
  attr_name = models.CharField(
    max_length=255, verbose_name="Zeitpunkt Attribut")

  def __str__(self):
    return "{}".format(self.attr_name)

  class Meta:
    db_table = "MioeDB_tbl_zpunkt_attr"
    verbose_name = "Zeitpunkt Attribut"
    verbose_name_plural = "Zeitpunkt Attribute"
    verbose_genus = "n"
    ordering = ('attr_name',)
    default_permissions = ()

# religions
class tbl_religion(models.Model):
  relig_name = models.CharField(max_length=255, verbose_name="Religion")

  def __str__(self):
    return "{}".format(self.relig_name)

  class Meta:
    db_table = "MioeDB_tbl_religion"
    verbose_name = "Religion"
    verbose_name_plural = "Religionen"
    verbose_genus = "f"
    ordering = ('relig_name',)
    default_permissions = ()

# instituts types (schools ...)
class tbl_institutstyp(models.Model):
  schule = models.BooleanField(verbose_name = "Schule")
  typ = models.CharField(max_length=255, verbose_name="Institutstyp")

  def __str__(self):
    return "{}".format(self.typ)

  class Meta:
    db_table = "MioeDB_tbl_institutstyp"
    verbose_name = "Institutstyp"
    verbose_name_plural = "Institutstypen"
    verbose_genus = "m"
    ordering = ('typ',)
    default_permissions = ()

# --- 2 level tables---
# additional fields for administrativ mioe entries
class tbl_mioe_orte(models.Model):
  id_orte = models.ForeignKey(
    'PersonenDB.tbl_orte',
    on_delete=models.CASCADE, verbose_name="Ort"
  )
  #TODO do we need gid here at all? it is also in wb
  gid = models.IntegerField(
    unique=True, blank=True,
    null=True, verbose_name="REDE-ID")
  adm_lvl = models.ForeignKey(
    'tbl_adm_lvl',
    on_delete=models.CASCADE, verbose_name="Administrative Einheit"
  )
  #TODO add default value false
  histor = models.BooleanField(verbose_name="Historischer Ort")

  def __str__(self):
    return "{}".format(self.id_orte.ort_namelang)

  class Meta:
    db_table = "MioeDB_tbl_orte"
    verbose_name = "MiÖ Ort"
    verbose_name_plural = "MiÖ Orte"
    verbose_genus = "m"
    ordering = ('gid',)
    default_permissions = ()

# variations
class tbl_varietaet(models.Model):
  variet_name = models.CharField(max_length=255, verbose_name="Sprache")
  iso_code = models.CharField(max_length=5, verbose_name="ISO-Code")
  id_typ = models.ForeignKey(
    'tbl_variet_typ',
    on_delete=models.CASCADE, verbose_name="Varietätstyp"
  )
  id_varietaet = models.ForeignKey(
    'tbl_varietaet',
    on_delete = models.CASCADE, verbose_name="Varietät"
  )

  def __str__(self):
    return "{}".format(self.variet_name)

  class Meta:
    db_table = "MioeDB_tbl_varietaet"
    verbose_name = "Varietät"
    verbose_name_plural = "Varietät"
    verbose_genus = "f"
    ordering = ('variet_name',)
    default_permissions = ()

# date in the history
class tbl_zeitpunkt(models.Model):
  datum = models.DateField("Zeitpunkt")
  id_attribut = models.ForeignKey(
    'tbl_zpunkt_attr',
    on_delete = models.CASCADE, verbose_name=("Zeitpunkt Attribut")
  )
  kommentar = models.CharField(max_length=250, verbose_name="Kommentar")

  def __str__(self):
    return "{}".format(self.datum)

  class Meta:
    db_table = "MioeDB_tbl_zeitpunkt"
    verbose_name = "Zeitpunkt"
    verbose_name_plural = "Zeitpunkte"
    verbose_genus = "m"
    ordering = ('datum',)
    default_permissions = ()

# --- 3 level tables---
# type of data
class tbl_art_daten(models.Model):
  art_name = models.CharField(max_length=255, verbose_name="Art von Daten")
  id_varietaet = models.ForeignKey(
    'tbl_varietaet',
    on_delete=models.CASCADE, verbose_name="Varietät"
  )
  id_religion = models.ForeignKey(
    'tbl_religion',
    on_delete=models.CASCADE, verbose_name="Religion"
  )

  def __str__(self):
    return "{} - {} {}".format(
      self.art_name,
      self.id_varietaet.variet_name,
      self.id_religion.relig_name)

  class Meta:
    db_table = "MioeDB_tbl_art_daten"
    verbose_name = "Art von Daten"
    verbose_name_plural = "Arten von Daten"
    verbose_genus = "f"
    ordering = ('art_name',)
    default_permissions = ()

# mioe persons
class tbl_mioe_personen(models.Model):
  id_personen = models.ForeignKey(
    'PersonenDB.tbl_personen',
    on_delete=models.CASCADE, verbose_name="Person"
  )
  funktion = models.CharField(
    blank=True, null=True,
    max_length=255, verbose_name="Funktion"
  )
  geburtsort_angabe = models.CharField(
    blank=True, null=True,
    max_length=255, verbose_name="Geburtsort Angabe"
  )
  geburtsort = models.ForeignKey(
    'tbl_mioe_orte',
    on_delete=models.CASCADE, verbose_name="Geburtsort"
  )

  def __str__(self):
    return "{} - {}".format(
      self.id_personen.nachname,
      self.id_personen.vorname,)

  class Meta:
    db_table = "MioeDB_tbl_mioe_personen"
    verbose_name = "Mioe Person"
    verbose_name_plural = "Mioe Personen"
    verbose_genus = "f"
    ordering = ('id_personen',)
    default_permissions = ()

# polls
class tbl_wb(models.Model):
  num_wb = models.IntegerField(verbose_name="Wenkerbogen Nummer")
  typ_wb = models.CharField(max_length=1, verbose_name="Wenkerbogen Typ")
  anfang_beginn = models.ForeignKey(
    'tbl_zeitpunkt',
    related_name='wb_anfang_beginn',
    blank=True, null=True, verbose_name="Anfang Beginn"
  )
  ende_beginn = models.ForeignKey(
    'tbl_zeitpunkt',
    related_name='wb_ende_beginn',
    blank=True, null=True, verbose_name="Ende Beginn"
  )
  id_mioe_ort = models.ForeignKey(
    'tbl_mioe_orte',
    on_delete=models.CASCADE, verbose_name="MiÖ-Ort"
  )
  gid = models.IntegerField(
    unique=True, blank=True,
    null=True, verbose_name="REDE-ID"
  )
  schulort_orig = models.CharField(
    max_length=255, verbose_name="Schulort (Angabe)",
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
  andere_sprachen = models.BooleanField(verbose_name="Andere Sprachen")
  welche_sprachen = models.CharField(
    max_length=255, blank=True, null=True,
    verbose_name="Welche Sprachen"
  )
  sprachen_verhaeltnis = models.CharField(
    max_length=255, blank=True, null=True,
    verbose_name="Sprachen Verhältnis"
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
  problematisch = models.BooleanField(verbose_name="Problematisch")
  link_rede = models.CharField(
    max_length=255, blank=True, null=True,
    verbose_name="REDE Link"
  )

  def __str__(self):
	  return "{} ({})".format(self.num_wb, self.id_mioe_ort.id_orte.ort_namekurz)

  class Meta:
    db_table = "MioeDB_tbl_wb"
    verbose_name = "Wenkerbogen"
    verbose_name_plural = "Wenkerbögen"
    verbose_genus = "m"
    ordering = ('num_wb',)
    default_permissions = ()

# --- 5 level tables ---
# polls languages
class tbl_wb_sprache(models.Model):
  id_wb = models.ForeignKey(
    'tbl_wb',
    on_delete=models.CASCADE, verbose_name="Wenkerbogen"
  )
  id_varietaet = models.ForeignKey(
    'tbl_varietaet',
    on_delete=models.CASCADE, verbose_name="Varietät"
  )
  anteil = models.FloatField(verbose_name="Anteil")

  def __str__(self):
    return "{} - {}%".format(self.id_varietaet.variet_name, self.anteil)

  class Meta:
    db_table = "MioeDB_tbl_wb_sprache"
    verbose_name = "Wenkerbogen Sprache"
    verbose_name_plural = "Wenkerbögen Sprachen"
    verbose_genus = "f"
    ordering = ('id_wb',)
    default_permissions = ()

# sources of info
class tbl_quelle(models.Model):
  wenkerbogen = models.ForeignKey(
    'tbl_wb',
    blank=True, null=True,
    on_delete=models.CASCADE, verbose_name="Wenkerbogen"
  )
  # does not exist yet. should be foreign key. Char for test purposes
  id_literatur = models.CharField(
    max_length=255, blank=True, null=True,
    verbose_name="Literatur"
  )

  def __str__(self):
    if self.wenkerbogen is not None:
      return "wb: {}".format(self.wenkerbogen.num_wb)
    else:
      return "lit: {}".format(self.id_literatur)

  class Meta:
    db_table = "MioeDB_tbl_quelle"
    verbose_name = "Quelle"
    verbose_name_plural = "Quellen"
    verbose_genus = "f"
    ordering = ('id',)
    default_permissions = ()

# polls are also for
class tbl_wb_auch_fuer(models.Model):
  id_wb = models.ForeignKey(
    'tbl_wb',
    on_delete=models.CASCADE, verbose_name="Wenkerbogen",
  )
  id_wbort = models.ForeignKey(
    'tbl_mioe_orte',
    on_delete=models.CASCADE, verbose_name="Wenkerort",
  )
  id_lehrer = models.ForeignKey(
    'tbl_mioe_personen',
    on_delete=models.CASCADE, verbose_name="Lehrer",
  )
  kommentar_wb = models.CharField(
    max_length=255, blank=True, null=True,
    verbose_name="Kommentar Wenkerbogen",
  )
  kommentar_wiss = models.CharField(
    max_length=255, blank=True, null=True,
    verbose_name="Kommentar Wiss.",
  )

  def __str__(self):
    return "{}: {}, {}".format(
      self.id_wb.num_wb, self.id_wbort.id_orte.ort_namekurz, self.id_lehrer.id_personen.nachname,
  )

  class Meta:
    db_table = "MioeDB_tbl_wb_auch_fuer"
    verbose_name = "Wenkerbogen auch fuer"
    verbose_name_plural = "Wenkerbögen auch fuer"
    verbose_genus = "m"
    ordering = ('id_wb',)
    default_permissions = ()

# --- 5 level tables ---
class tbl_volkszaelung(models.Model):
  id_adm_einheit = models.ForeignKey(
    'tbl_mioe_orte',
    on_delete=models.CASCADE, verbose_name="Administrative Einheit"
  )
  id_quelle = models.ForeignKey(
    'tbl_quelle',
    on_delete=models.CASCADE, verbose_name="Quelle"
  )
  id_erheb_datum = models.ForeignKey(
    'tbl_zeitpunkt',
    on_delete=models.CASCADE, verbose_name="Erhebungsdatum"
  )

  def __str__(self):
    return "{} - {}".format(
      self.id_adm_einheit.id_orte.ort_namekurz,
      self.id_erheb_datum.datum
    )

  class Meta:
    db_table = "MioeDB_tbl_vz"
    verbose_name = "Volkszählung"
    verbose_name_plural = "Volkszählungen"
    verbose_genus = "f"
    ordering = ('id_adm_einheit',)
    default_permissions = ()

# administativ relation
class tbl_adm_zuordnung(models.Model):
  id_ort1 = models.ForeignKey(
    'tbl_mioe_orte',
    related_name="%(class)s_ort1",
    on_delete=models.CASCADE, verbose_name="Administrative Einheit 1"
  )
  id_ort2 = models.ForeignKey(
    'tbl_mioe_orte',
    related_name="%(class)s_ort2",
    on_delete=models.CASCADE, verbose_name="Administrative Einheit 2"
  )
  id_quelle = models.ForeignKey(
    'tbl_quelle',
    on_delete=models.CASCADE, verbose_name="Quelle"
  )
  id_anfang_beginn = models.ForeignKey(
    'tbl_zeitpunkt',
    related_name='adm_anfang_beginn',
    on_delete=models.CASCADE, verbose_name="Anfang Beginn"
  )
  id_ende_beginn = models.ForeignKey(
    'tbl_zeitpunkt',
    related_name='adm_ende_beginn',
    on_delete=models.CASCADE, verbose_name="Ende Beginn"
  )
  id_anfang_ende = models.ForeignKey(
    'tbl_zeitpunkt',
    related_name='adm_anfang_ende',
    on_delete=models.CASCADE, verbose_name="Anfang Ende"
  )
  id_ende_ende = models.ForeignKey(
    'tbl_zeitpunkt',
    related_name='adm_ende_ende',
    on_delete=models.CASCADE, verbose_name="Ende Ende"
  )

  def __str__(self):
    return "{}".format(
      self.id_ort1.id_orte.ort_namelang)

  class Meta:
    db_table = "MioeDB_tbl_adm_zuordnung"
    verbose_name = "Administrative Zuordnung"
    verbose_name_plural = "Administrative Zuordnung"
    verbose_genus = "f"
    ordering = ('id',)
    default_permissions = ()

# names variations
class tbl_name_var(models.Model):
  id_anfang_beginn = models.ForeignKey(
    'tbl_zeitpunkt',
    related_name='nv_anfang_beginn',
    on_delete=models.CASCADE, verbose_name="Anfang Beginn"
  )
  id_ende_beginn = models.ForeignKey(
    'tbl_zeitpunkt',
    related_name='nv_ende_beginn',
    on_delete=models.CASCADE, verbose_name="Ende Beginn"
  )
  id_anfang_ende = models.ForeignKey(
    'tbl_zeitpunkt',
    related_name='nv_anfang_ende',
    on_delete=models.CASCADE, verbose_name="Anfang Ende"
  )
  id_ende_ende = models.ForeignKey(
    'tbl_zeitpunkt',
    related_name='nv_ende_ende',
    on_delete=models.CASCADE, verbose_name="Ende Ende"
  )
  id_mioe_ort = models.ForeignKey(
    'tbl_mioe_orte',
    on_delete=models.CASCADE, verbose_name="Ort"
  )
  var_name = models.CharField(max_length=255, verbose_name="Namensvariation")
  id_varietaet = models.ForeignKey(
    'tbl_varietaet',
    on_delete=models.CASCADE, verbose_name="Varietät"
  )
  id_quelle = models.ForeignKey(
    'tbl_quelle',
    on_delete=models.CASCADE, verbose_name="Quelle"
  )

  def __str__(self):
    return "bis {} war {} - {}".format(
      self.id_zietpunkt.datum,
      self.id_mioe_ort.id_orte.ort_namekurz,
      self.var_name
    )

  class Meta:
    db_table = "MioeDB_tbl_name_var"
    verbose_name = "Namensvariation"
    verbose_name_plural = "Namensvariationen"
    verbose_genus = "f"
    ordering = ('id_mioe_ort',)
    default_permissions = ()

# --- 6 level tables ---
# teaching institutions
class tbl_institutionen(models.Model):
  id_ort = models.ForeignKey(
    'tbl_mioe_orte',
    on_delete=models.CASCADE, verbose_name="Ort"
  )
  id_institutstyp = models.ForeignKey(
    'tbl_institutstyp',
    on_delete=models.CASCADE, verbose_name="Institutstyp"
  )
  anz_klassen = models.IntegerField(verbose_name="Anzahl von Klassen")
  id_quelle = models.ForeignKey(
    'tbl_volkszaelung',
    on_delete=models.CASCADE, verbose_name="Quelle"
  )
  kommentar = models.CharField(
    max_length=255, blank=True, null=True,
    verbose_name="Kommentar"
  )

  def __str__(self):
    return "{}: {} mit {} Klassen".format(
      self.id_ort.id_orte.ort_namekurz,
      self.id_institutstyp.typ,
      self.id_quelle.id_erheb_datum.datum)

  class Meta:
    db_table = "MioeDB_tbl_instatutionen"
    verbose_name = "Institution"
    verbose_name_plural = "Institutionen"
    verbose_genus = "f"
    ordering = ('id_ort',)
    default_permissions = ()

# population data
class tbl_vz_daten(models.Model):
  id_vz = models.ForeignKey(
    'tbl_volkszaelung',
    on_delete=models.CASCADE, verbose_name="Volkszählung"
  )
  id_mioe_ort = models.ForeignKey(
    'tbl_mioe_orte',
    on_delete=models.CASCADE, verbose_name="Ort"
  )
  id_art = models.ForeignKey(
    'tbl_art_daten',
    on_delete=models.CASCADE, verbose_name="Art von Daten"
  )
  anzahl = models.IntegerField(verbose_name="Anzahl")

  def __str__(self):
    return "{} {}: {} - {}".format(
      self.id_volkszaelung.id_erheb_datum.datum,
      self.id_mioe_ort.id_orte.ort_namekurz,
      self.id_art.art_name,
      self.anzahl
    )

  class Meta:
    unique_together = ("id_vz", "id_mioe_ort", "id_art")
    db_table = "MioeDB_tbl_vz_daten"
    verbose_name = "Volkszählungsdaten"
    verbose_name_plural = "Volkszählungsdaten"
    verbose_genus = "f"
    ordering = ('id_mioe_ort',)
    default_permissions = ()

# --- 7 level tables ---
# language institutions
class tbl_sprache_institut(models.Model):
  id_institution = models.ForeignKey(
    'tbl_institutionen',
    on_delete=models.CASCADE, verbose_name="Institutionen pro Sprache"
  )
  id_varietaet = models.ForeignKey(
    'tbl_varietaet',
    on_delete=models.CASCADE, verbose_name="Varietät"
  )
  anz_schule = models.IntegerField(verbose_name="Anzahl von Schulen")

  def __str__(self):
    return "{}: {} mit {} Klassen".format(
      self.id_institution.id_ort.id_orte.ort_namekurz,
      self.id_varietaet.variet_name,
      self.anz_schule)

  class Meta:
    db_table = "MioeDB_tbl_sprache_institut"
    verbose_name = "Institutionen pro Sprache"
    verbose_name_plural = "Institutionen pro Sprache"
    verbose_genus = "f"
    ordering = ('id_institution',)
    default_permissions = ()
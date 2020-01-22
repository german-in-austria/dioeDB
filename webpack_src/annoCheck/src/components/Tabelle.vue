<template>
  <div class="annocheck-tabelle">
    <div class="clearfix">
      <div class="form-inline float-left">
        <div class="form-group">
          <label for="annocheck-tabelle-seite">Seite</label>
          <div class="input-group">
            <div class="input-group-btn">
              <button class="btn btn-default" type="button" @click="seite > 1 ? seite-- : false" title="Vorherige Seite" :disabled="seite <= 1"><span class="glyphicon glyphicon-chevron-left"></span></button>
            </div>
            <input type="text" v-model="seite" min="1" :max="maxSeiten" class="form-control" id="annocheck-tabelle-seite">
            <div class="input-group-btn">
              <button class="btn btn-default" type="button" @click="seite < maxSeiten ? seite++ : false" title="Nächste Seite" :disabled="seite >= maxSeiten"><span class="glyphicon glyphicon-chevron-right"></span></button>
            </div>
          </div>
          <b> / {{ maxSeiten }}</b> - Einträge: <b>{{ zaehler.toLocaleString('de-DE') }}</b>
        </div>
      </div>
      <div class="form-inline float-right">
        <div class="form-group">
          <label for="annocheck-tabelle-eps">Einträge pro Seite</label>
          <select class="form-control" v-model="eintraegeProSeite" id="annocheck-tabelle-eps">
            <option :value="anz" v-for="anz in [10, 15, 25, 50, 100, 250]" :key="'eps' + anz">{{ anz }}</option>
          </select>
        </div>
        <button @click="zeigeSpaltenAuswahl = !zeigeSpaltenAuswahl" @blur="spaltenAuswahlBlur" ref="zeigeSpaltenAuswahlBtn" class="btn btn-default" type="button" title="Ansicht"><span class="glyphicon glyphicon-eye-open"></span></button>
        <div class="zsa" v-if="zeigeSpaltenAuswahl" ref="zeigeSpaltenAuswahl">
          <button v-for="(feldoption, feld) in tabellenfelder" :key="'vthtf' + feld" @blur="spaltenAuswahlBlur" ref="zeigeSpaltenAuswahlBtns" @click="feldoption.show = !feldoption.show" :class="feldoption.show ? 'zsa-show' : ''"><span :class="'glyphicon glyphicon-eye-' + (feldoption.show ? 'open' : 'close')"></span> {{ feld }}</button>
        </div>
        <button @click="maxColWidth = !maxColWidth" class="btn btn-default" type="button" title="Maximale Spaltenbreite"><span :class="'glyphicon ' + (maxColWidth ? 'glyphicon-text-height' : 'glyphicon-text-width')"></span></button>
        <button @click="reload()" class="btn btn-default" type="button"><span class="glyphicon glyphicon-refresh"></span></button>
      </div>
    </div>
    <div class="table-responsive">
      <table class="table table-hover" style="white-space:pre">
        <thead>
          <tr>
            <th>#</th>
            <th v-for="(feldoption, feld) in sichtbareTabellenfelder" :key="'thtf' + feld" :title="feldoption.sortby || feld">
              <template v-if="feldoption.local && feld === 'Tagebenen'">
                <span v-if="!showAllTagEbenen && filterfelder.tagebene > 0 && filterfelder.tagebenenName">Tagebene: {{ filterfelder.tagebenenName }}</span>
                <span v-else>Tagebenen</span>
                <label class="ml10" style="margin-bottom:0"><input type="checkbox" v-model="showAllTagEbenen">Alle Ebenen.</label>
              </template>
              <button @click="spalteSortieren(feldoption.sortby || feld)" class="sort-btn" v-else-if="!feldoption.dontSort">{{ feldoption.displayName || feld }} <span :class="'glyphicon glyphicon-sort-by-attributes' + (spaltenSortierung.asc ? '' : '-alt')" v-if="spaltenSortierung.spalte === (feldoption.sortby || feld)"></span></button>
              <template v-else>{{ feldoption.displayName || feld }}</template>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(eintrag, key) in eintraege.data.list"
            :key="'ez' + eintrag"
            @click="editAntwort(eintrag)"
            :class="'edit-antwort' + (maxColWidth ? ' max-col-width' : '')"
          >
            <th scope="row">{{ lSeite * eintraegeProSeite + key + 1 }}</th>
            <td v-for="(feldoption, feld) in sichtbareTabellenfelder" :key="'ez' + eintrag + 'thtf' + feld">
              <span v-html="fxFeld(eintrag, feld)" v-if="feldoption.local"/>
              <div v-else>{{ eintrag[feld] }}</div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="text-right">Anfrage Dauer: {{ (ladeZeit / 1000).toFixed(2) }} Sekunden</div>
    <div>
      <i><b>R</b> = Reihung</i><br>
      <i><b>aId</b> = Antworten Id</i><br>
      <i><b>Tr.</b> = Transkript</i><br>
      <i><b>aT</b> = Antworten Type:</i>&nbsp; <b>s</b> = Satz, <b>t</b> = Token, <b>b</b> = Tokenset Bereich, <b>l</b> = Tokenset Liste<br>
    </div>
    <AntwortenEdit @closed="antwortenEdit = null" :eintrag="antwortenEdit" :http="http" :tagsData="tagsData" :infTrans="infTrans" :filterfelder="filterfelder" @changed="debouncedReload()" v-if="antwortenEdit" />
    <div class="loading" v-if="loading">Lade ...</div>
  </div>
</template>

<script>
/* global _ Popper */
import AntwortenEdit from './AntwortenEdit'

export default {
  name: 'Tabelle',
  props: ['tabellenfelder', 'suchfelder', 'filterfelder', 'eintraege', 'http', 'tagsData', 'infTrans'],
  data () {
    return {
      seite: 1,
      lSeite: 0,
      zaehler: 0,
      eintraegeProSeite: 15,
      ladeZeit: 0.0,
      ladeZeitStart: 0.0,
      loading: false,
      downloading: false,
      zeigeSpaltenAuswahl: false,
      popper: null,
      spaltenSortierung: { spalte: 'Reihung', asc: true },
      rereload: false,
      showAllTagEbenen: true,
      antwortenEdit: null,
      maxColWidth: true
    }
  },
  computed: {
    aSeite () {
      return this.seite - 1
    },
    maxSeiten () {
      return Math.ceil(this.zaehler / this.eintraegeProSeite)
    },
    sichtbareTabellenfelder () {    // Liste der Spalten die nicht ausgeblendet sind
      let sichtbareTabellenfelder = {}
      Object.keys(this.tabellenfelder).forEach(key => {
        if (this.tabellenfelder[key].show) {
          sichtbareTabellenfelder[key] = this.tabellenfelder[key]
        }
      }, this)
      return sichtbareTabellenfelder
    },
    countSelected () {
      let count = 0
      this.eintraege.data.list.forEach((aEintrag) => {
        if (aEintrag.selected && aEintrag.selected.length === aEintrag.tokens.length) {
          count += 1
        }
      }, this)
      return count
    }
  },
  mounted () {
    console.log(this.tabellenfelder)
    this.reload()
  },
  methods: {
    editAntwort (eintrag) {
      console.log('editAntwort', eintrag.id, eintrag)
      this.antwortenEdit = eintrag
    },
    fxFeld (eintrag, feld) {
      if (feld === 'Tagebenen') {
        let out = ''
        eintrag[feld].forEach(aEbene => {
          if (this.showAllTagEbenen || this.filterfelder.tagebene < 1 || this.filterfelder.tagebene === aEbene.eId) {
            out += (this.showAllTagEbenen || this.filterfelder.tagebene < 1 ? '<b>' + aEbene.e + ':</b> ' : '') + aEbene.t + '<br>'
          }
        })
        return out
      }
      return 'Unbekannt: ' + feld
    },
    selectAll (set = null) {
      if (set === null) {   // Toggle
        set = !(this.countSelected === this.eintraege.data.list.length)
      }
      this.eintraege.data.list.forEach((aEintrag) => {
        this.selectAllTokens(aEintrag, set)
      }, this)
    },
    selectToken (eintrag, token, set = null) {
      if (set === null) {   // Toggle
        set = !(eintrag.selected && eintrag.selected.indexOf(token.id) > -1)
      }
      if (set) {
        if (!eintrag.selected) {
          this.$set(eintrag, 'selected', [])
        }
        if (eintrag.selected.indexOf(token.id) < 0) {
          eintrag.selected.push(token.id)
        }
      } else {
        if (eintrag.selected && eintrag.selected.indexOf(token.id) > -1) {
          eintrag.selected.splice(eintrag.selected.indexOf(token.id), 1)
        }
      }
    },
    selectAllTokens (eintrag, set = null) {
      if (set === null) {   // Toggle
        set = !(eintrag.selected && eintrag.selected.length === eintrag.tokens.length)
      }
      this.$set(eintrag, 'selected', [])
      if (set) {
        eintrag.tokens.forEach((aToken) => {
          eintrag.selected.push(aToken.id)
        }, this)
      }
    },
    debouncedReload: _.debounce(function () {   // Einträge verzögert laden
      this.reload()
    }, 300),
    reload: _.debounce(function () {  // Einträge laden
      if (!this.loading) {
        this.rereload = false
        this.loading = true
        this.ladeZeitStart = performance.now()
        this.http.post('', {
          getEntries: true,
          seite: this.aSeite,
          eps: this.eintraegeProSeite,
          filter: JSON.stringify({ ebene: this.filterfelder.tagebene, tag: this.filterfelder.tag, nichttag: this.filterfelder.nichtTag, inf: this.filterfelder.informant, trans: this.filterfelder.transkript, aufgabenset: this.filterfelder.aufgabenset, aufgabe: this.filterfelder.aufgabe }),
          sortierung: JSON.stringify(this.spaltenSortierung)
        }).then((response) => {
          console.log(response.data)
          this.eintraege.data.list = response.data.eintraege
          this.eintraege.data.tokenSets = this.getAllTokenSets(this.eintraege.data.list)
          this.zaehler = response.data.zaehler
          this.lSeite = response.data.seite
          this.seite = this.lSeite + 1
          this.ladeZeit = performance.now() - this.ladeZeitStart
          this.loading = false
          if (this.rereload) { this.reload() }
        }).catch((err) => {
          console.log(err)
          alert('Fehler!')
          this.ladeZeit = performance.now() - this.ladeZeitStart
          this.loading = false
          if (this.rereload) { this.reload() }
        })
      } else {
        this.rereload = true
      }
    }, 100),
    spalteSortieren (feld) {
      if (this.spaltenSortierung.spalte === feld) {
        this.spaltenSortierung.asc = !this.spaltenSortierung.asc
      } else {
        this.spaltenSortierung = { spalte: feld, asc: true }
      }
      this.reload()
    },
    spaltenAuswahlBlur: _.debounce(function () {
      this.$nextTick(() => {
        if (this.$refs.zeigeSpaltenAuswahlBtns && this.$refs.zeigeSpaltenAuswahlBtns.indexOf(document.activeElement) < 0) {
          this.zeigeSpaltenAuswahl = false
        }
      })
    }, 20),
    getAllTokenSets (aEintraege) {
      let allTokenSets = {}
      aEintraege.forEach((aEintrag) => {
        if (aEintrag.tokens) {
          aEintrag.tokens.forEach((aToken) => {
            if (aToken.tokensets) {
              aToken.tokensets.forEach((aTokenSet) => {
                if (!allTokenSets[aTokenSet.id]) {
                  allTokenSets[aTokenSet.id] = aTokenSet
                }
              }, this)
            }
          }, this)
        }
      }, this)
      return allTokenSets
    },
    close () {
      this.$emit('close')
    }
  },
  watch: {
    zeigeSpaltenAuswahl (nVal) {
      this.$nextTick(() => {
        if (nVal) {
          this.popper = new Popper(this.$refs.zeigeSpaltenAuswahlBtn, this.$refs.zeigeSpaltenAuswahl, {
            placement: 'right-start',
            modifiers: {
              offset: { offset: '0,-100%' }
            }
          })
        } else if (this.popper) {
          this.popper.destroy()
        }
      })
    },
    'filterfelder.tagebene' () { this.reload() },
    'filterfelder.tag' () { this.reload() },
    'filterfelder.nichtTag' () { this.reload() },
    'filterfelder.informant' () { this.reload() },
    'filterfelder.transkript' () { this.reload() },
    'filterfelder.aufgabenset' () { this.reload() },
    'filterfelder.aufgabe' () { this.reload() },
    eintraegeProSeite () { this.reload() },
    seite (nVal) {
      this.seite = this.maxSeiten < 1 ? 1 : isNaN(nVal) ? parseInt(nVal.replace(/\D/, '')) : this.seite < 1 ? 1 : (this.seite > this.maxSeiten ? this.maxSeiten : this.seite)
      if (this.lSeite !== this.aSeite) {
        this.debouncedReload()
      }
    }
  },
  components: {
    AntwortenEdit
  }
}
</script>

<style scoped>
.annocheck-tabelle {
  position: relative;
  margin-top: 10px;
  margin-bottom: 150px;
}
.form-inline > .form-group {
  margin-right: 10px;
}
.form-inline > .form-group > label {
  margin-right: 5px;
}
.float-left {
  float: left;
}
#annocheck-tabelle-seite {
  text-align: right;
  width: 70px;
  padding-left: 0;
  padding-right: 0;
  text-align: center;
}
td {
  white-space: nowrap;
}
.zsa {
  background: #fff;
  box-shadow: 3px 3px 5px rgba(0,0,0,0.3);
  border: 1px solid #ccc;
  padding: 15px;
}
.zsa > button {
  background: none;
  border: none;
  display: block;
  width: 100%;
  text-align: left;
  color: #999;
}
.zsa > button.zsa-show {
  color: #333;
}
.sort-btn {
  background: none;
  border: none;
  display: block;
  width: 100%;
  text-align: left;
  padding: 0;
}
.auswahl-btn {
  border: none;
  background: none;
  padding: 0;
  margin: 0;
  outline: none!important;
}
.auswahl-btn:focus {
  color: #337ab7;
}
.tokens {
  position: relative;
  z-index: 1;
}
.edit-antwort {
  cursor: pointer;
}
.edit-antwort.max-col-width > td > div {
  white-space: normal;
  max-width: 500px;
  width: max-content;
}
</style>

<template>
  <div class="annocheck-filtern form-horizontal">
    <div class="row">
      <div class="col col-md-6">
        <div class="form-group">
          <label for="tagebene" class="col-sm-4 control-label">Tag Ebene</label>
          <div class="col-sm-8">
            <v-select v-model="filterfelder.tagebene" :options="tagebenenListe.filter(tl => tl.pk > 0)" :reduce="tl => tl.pk" label="title" placeholder="Alle">
              <template v-slot:option="tl">
                {{ tl.title }}{{ tl.count > -1 ? ' - ' + tl.count.toLocaleString() : '' }}
              </template>
              <template #selected-option="tl">
                {{ tl.title }}{{ tl.count > -1 ? ' - ' + tl.count.toLocaleString() : '' }}
              </template>
              <template v-slot:no-options="{ search, searching }">
                <template v-if="searching">Keine Ergebnisse für "<em>{{ search }}</em>" gefunden.</template>
                <em v-else style="opacity: 0.5">Um Suche zu starten ist eine Eingabe notwendig.</em>
              </template>
            </v-select>
          </div>
        </div>
        <div class="form-group">
          <label for="tag" class="col-sm-4 control-label">Tag</label>
          <div class="col-sm-8">
            <v-select v-model="filterfelderTag" :options="tagListe" :reduce="t => t.key" label="title" placeholder="Alle" :disabled="tagsData.data.loading || tagsData.data.loadingTags">
              <template v-slot:option="t">
                {{ t.title }}
              </template>
              <template #selected-option="t">
                {{ (tagsData.data.loading || tagsData.data.loadingTags ? 'Lade Tags ...' : t.title) }}
              </template>
              <template v-slot:no-options="{ search, searching }">
                <template v-if="searching">Keine Ergebnisse für "<em>{{ search }}</em>" gefunden.</template>
                <em v-else style="opacity: 0.5">Um Suche zu starten ist eine Eingabe notwendig.</em>
              </template>
            </v-select>
          </div>
        </div>
        <div class="form-group">
          <label for="ntag" class="col-sm-4 control-label">Nicht Tag</label>
          <div class="col-sm-8">
            <v-select v-model="filterfelderNichtTag" :options="tagListe" :reduce="t => t.key" label="title" placeholder="Keine" :disabled="tagsData.data.loading || tagsData.data.loadingTags">
              <template v-slot:option="t">
                {{ t.title }}
              </template>
              <template #selected-option="t">
                {{ (tagsData.data.loading || tagsData.data.loadingTags ? 'Lade Tags ...' : t.title) }}
              </template>
              <template v-slot:no-options="{ search, searching }">
                <template v-if="searching">Keine Ergebnisse für "<em>{{ search }}</em>" gefunden.</template>
                <em v-else style="opacity: 0.5">Um Suche zu starten ist eine Eingabe notwendig.</em>
              </template>
            </v-select>
          </div>
        </div>
        <div class="form-group">
          <label for="informant" class="col-sm-4 control-label">Informant</label>
          <div class="col-sm-8">
            <v-select v-model="filterfelder.informant" :options="informantenListe.filter(inf => inf.pk > 0)" :reduce="inf => inf.pk" label="kuerzelAnonym" placeholder="Alle">
              <template v-slot:option="inf">
                {{inf.kuerzelAnonym}}{{ inf.count > -1 ? ' - ' + inf.count.toLocaleString() : '' }}
              </template>
              <template #selected-option="inf">
                {{inf.kuerzelAnonym}}{{ inf.count > -1 ? ' - ' + inf.count.toLocaleString() : '' }}
              </template>
              <template v-slot:no-options="{ search, searching }">
                <template v-if="searching">Keine Ergebnisse für "<em>{{ search }}</em>" gefunden.</template>
                <em v-else style="opacity: 0.5">Um Suche zu starten ist eine Eingabe notwendig.</em>
              </template>
            </v-select>
          </div>
        </div>
      </div>
      <div class="col col-md-6">
        <div class="form-group">
          <label for="transkript" class="col-sm-4 control-label">Transkript</label>
          <div class="col-sm-8">
            <v-select v-model="filterfelder.transkript" :options="transcriptsListe.filter(ts => ts.pk !== 0)" :reduce="ts => ts.pk" label="name" placeholder="Alle">
              <template v-slot:option="ts">
                {{ts.name}}{{ ts.count > -1 ? ' - ' + ts.count.toLocaleString() : '' }}
              </template>
              <template #selected-option="ts">
                {{ts.name}}{{ ts.count > -1 ? ' - ' + ts.count.toLocaleString() : '' }}
              </template>
              <template v-slot:no-options="{ search, searching }">
                <template v-if="searching">Keine Ergebnisse für "<em>{{ search }}</em>" gefunden.</template>
                <em v-else style="opacity: 0.5">Um Suche zu starten ist eine Eingabe notwendig.</em>
              </template>
            </v-select>
          </div>
        </div>
        <div class="form-group">
          <label for="aufgabensets" class="col-sm-4 control-label">Aufgabensets</label>
          <div class="col-sm-8">
            <v-select v-model="filterfelder.aufgabenset" :options="aufgabensetListe.filter(as => as.pk > 0)" :reduce="as => as.pk" label="name" placeholder="Alle">
              <template v-slot:option="as">
                {{as.name}}{{ as.count > -1 ? ' - ' + as.count.toLocaleString() : '' }}
              </template>
              <template #selected-option="as">
                {{as.name}}{{ as.count > -1 ? ' - ' + as.count.toLocaleString() : '' }}
              </template>
              <template v-slot:no-options="{ search, searching }">
                <template v-if="searching">Keine Ergebnisse für "<em>{{ search }}</em>" gefunden.</template>
                <em v-else style="opacity: 0.5">Um Suche zu starten ist eine Eingabe notwendig.</em>
              </template>
            </v-select>
          </div>
        </div>
        <div class="form-group">
          <label for="aufgaben" class="col-sm-4 control-label">Aufgaben</label>
          <div class="col-sm-8">
            <v-select v-model="filterfelder.aufgabe" :options="aufgabenListe.filter(a => a.pk > 0)" :reduce="a => a.pk" label="name" placeholder="Alle">
              <template v-slot:option="a">
                {{a.name}}{{ a.count > -1 ? ' - ' + a.count.toLocaleString() : '' }}
              </template>
              <template #selected-option="a">
                {{a.name}}{{ a.count > -1 ? ' - ' + a.count.toLocaleString() : '' }}
              </template>
              <template v-slot:no-options="{ search, searching }">
                <template v-if="searching">Keine Ergebnisse für "<em>{{ search }}</em>" gefunden.</template>
                <em v-else style="opacity: 0.5">Um Suche zu starten ist eine Eingabe notwendig.</em>
              </template>
            </v-select>
          </div>
        </div>
        <div class="form-group">
          <div class="col-sm-offset-4 col-sm-8">
            <div class="form-inline">
              <div class="checkbox">
                <label>
                  <input type="checkbox" v-model="showCount"> Anzahl anzeigen
                </label>
              </div>
              <!-- <div class="checkbox">
                <label class="ml10">
                  <input type="checkbox" v-model="showCountTrans" :disabled="!showCount"> Transkript
                </label>
              </div> -->
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="loading" v-if="loading">Lade ...<div>{{ loadInfos }}</div></div>
  </div>
</template>

<script>
export default {
  name: 'Filtern',
  props: ['filterfelder', 'http', 'tagsData', 'infTrans'],
  data () {
    return {
      loading: false,
      loadInfos: '',
      mvDurchschnitt: 0.0,
      mvLastUpdate: 'Unbekannt ...',
      tagebenenListe: [],
      tagebenenObj: {},
      informantenListe: [],
      transcriptsListe: [],
      aufgabensetListe: [],
      aufgabenListe: [],
      showCount: false,
      showCountTrans: false,
      filterfelderTag: 0,
      filterfelderNichtTag: 0
    }
  },
  computed: {
    tagListe () {
      let aTagListe = []
      if (!this.tagsData.data.loading && !this.tagsData.data.loadingTags) {
        let gTag = function (aThis, sTag, deep = 0, filtered = null) {
          if (filtered < 1 || !sTag.tezt || sTag.tezt.indexOf(filtered) > -1) {
            let sTagListe = [{pk: sTag.pk, title: (deep > 0 ? '- '.repeat(deep) : '') + sTag.t + ((sTag.tl && sTag.t !== sTag.tl) ? ' (' + sTag.tl + ')' : '')}]
            if (sTag.c) {
              sTag.c.forEach(sTagId => {
                sTagListe = [...sTagListe, ...gTag(aThis, aThis.tagsData.data.tagsCache.tags[sTagId], deep + 1, filtered)]
              })
            }
            return sTagListe
          } else {
            return []
          }
        }
        this.tagsData.data.tagsCache.tagsReihung.forEach(aTagId => {
          let aTag = this.tagsData.data.tagsCache.tags[aTagId]
          if (!aTag.p) {
            if (this.filterfelder.tagebene < 1 || !aTag.tezt || aTag.tezt.indexOf(this.filterfelder.tagebene) > -1) {
              aTagListe = [...aTagListe, ...gTag(this, aTag, 0, this.filterfelder.tagebene)]
            }
          }
        })
      }
      aTagListe.forEach((t, dg) => {
        t.key = dg
      })
      // console.log('aTagListe', aTagListe)
      return aTagListe
    }
  },
  mounted () {
    console.log('filterfelder', this.filterfelder)
    this.updateFilterfelderTag()
    this.updateFilterfelderNichtTag()
    this.getFilterData()
  },
  methods: {
    updateFilterfelderNichtTag () {
      this.filterfelderNichtTag = null
      this.tagListe.forEach(t => {
        if (t.pk === this.filterfelder.nichtTag) {
          this.filterfelderNichtTag = t.key
        }
      })
      if (this.filterfelderNichtTag < 1) {
        this.filterfelder.nichtTag = 0
      }
    },
    updateFilterfelderTag () {
      this.filterfelderTag = null
      this.tagListe.forEach(t => {
        if (t.pk === this.filterfelder.tag) {
          this.filterfelderTag = t.key
        }
      })
      if (this.filterfelderTag < 1) {
        this.filterfelder.tag = 0
      }
    },
    getFilterData () {    // Informationen für Filter laden
      this.loading = true
      this.loadInfos = 'Filter Daten'
      let aFilter = JSON.stringify({
        ebene: this.filterfelder.tagebene || 0,
        tag: this.filterfelder.tag || 0,
        nichttag: this.filterfelder.nichtTag || 0,
        inf: this.filterfelder.informant || 0,
        trans: this.filterfelder.transkript || 0,
        aufgabenset: this.filterfelder.aufgabenset || 0,
        aufgabe: this.filterfelder.aufgabe || 0
      })
      console.log('aFilter', aFilter)
      this.http.post('', {
        getFilterData: true,
        showCount: this.showCount,
        showCountTrans: this.showCountTrans,
        filter: aFilter
      }).then((response) => {
        this.tagebenenListe = response.data['tagEbenen']
        this.tagebenenListe.forEach(aTagebene => {
          this.tagebenenObj[aTagebene.pk] = aTagebene
        })
        this.informantenListe = response.data['informanten']
        this.transcriptsListe = response.data['transcripts']
        this.aufgabensetListe = response.data['aufgabensets']
        this.aufgabenListe = response.data['aufgaben']
        console.log('getFilterData', response.data)
        this.loading = false
      }).catch((err) => {
        console.log(err)
        alert('Fehler!')
        this.loading = false
      })
    }
  },
  watch: {
    'filterfelder.tagebene' () {
      this.filterfelder.tagebenenName = this.filterfelder.tagebene > 0 ? this.tagebenenObj[this.filterfelder.tagebene].title : null
      this.getFilterData()
    },
    'filterfelder.tag' () { this.getFilterData() },
    'filterfelder.nichtTag' () { this.getFilterData() },
    'filterfelder.informant' () { this.getFilterData() },
    'filterfelder.transkript' () { this.getFilterData() },
    'filterfelder.aufgabenset' (nVal, oVal) {
      if (nVal !== oVal) {
        this.filterfelder.aufgabe = 0
      }
      this.getFilterData()
    },
    'filterfelder.aufgabe' () { this.getFilterData() },
    filterfelderTag () {
      this.filterfelder.tag = this.filterfelderTag > 0 ? this.tagListe[this.filterfelderTag].pk : 0
    },
    filterfelderNichtTag () {
      this.filterfelder.nichtTag = this.filterfelderNichtTag > 0 ? this.tagListe[this.filterfelderNichtTag].pk : 0
    },
    tagListe () {
      this.updateFilterfelderTag()
      this.updateFilterfelderNichtTag()
    },
    showCount () { this.getFilterData() },
    showCountTrans () { this.getFilterData() }
  }
}
</script>

<style scoped>
.annocheck-filtern {
  position: relative;
}
.loading {
  position: absolute;
  left: -10px;
  right: -10px;
  top: -10px;
  bottom: -10px;
  font-size: 50px;
  line-height: 1;
  padding: 25px;
}
.loading > div {
  font-size: 16px;
  line-height: 1;
}
.v-select >>> .vs__selected-options {
  flex-wrap: nowrap;
  min-width: 0;
}
.v-select >>> .vs__selected {
  display: block;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}
.v-select.vs--searchable >>> .vs__dropdown-toggle {
  max-width: 100%;
}
.v-select.vs--searchable >>> .vs__dropdown-menu {
  min-width: 100%;
  width: inherit;
}
</style>

<template>
  <div class="annocheck-filtern form-horizontal">
    <div class="row">
      <div class="col col-md-6">
        <div class="form-group">
          <label for="tagebene" class="col-sm-4 control-label">Tag Ebene</label>
          <div class="col-sm-8">
            <select class="form-control" v-model="filterfelder.tagebene" id="tagebene">
              <option :value="tagebene.pk"
                v-for="tagebene in tagebenenListe"
                :key="'te' + tagebene.pk"
                :disabled="tagebene.count == 0"
              >{{ tagebene.title }}{{ tagebene.count > -1 ? ' - ' + tagebene.count.toLocaleString() : '' }}</option>
            </select>
          </div>
        </div>
        <div class="form-group">
          <label for="tag" class="col-sm-4 control-label">Tag</label>
          <div class="col-sm-8">
            <select class="form-control" v-model="filterfelder.tag" id="tag" :disabled="tagsData.data.loading || tagsData.data.loadingTags">
              <option value="0">{{ (tagsData.data.loading || tagsData.data.loadingTags ? 'Lade Tags ...' : 'Alle') }}</option>
              <option :value="tag.pk"
                v-for="(tag, tKey) in tagListe"
                :key="'t' + tKey + '-' + tag.pk"
              >{{ tag.title }}</option>
            </select>
          </div>
        </div>
        <div class="form-group">
          <label for="ntag" class="col-sm-4 control-label">Nicht Tag</label>
          <div class="col-sm-8">
            <select class="form-control" v-model="filterfelder.nichtTag" id="ntag" :disabled="tagsData.data.loading || tagsData.data.loadingTags">
              <option value="0">{{ (tagsData.data.loading || tagsData.data.loadingTags ? 'Lade Tags ...' : 'Alle') }}</option>
              <option :value="tag.pk"
                v-for="(tag, tKey) in tagListe"
                :key="'nt' + tKey + '-' + tag.pk"
              >{{ tag.title }}</option>
            </select>
          </div>
        </div>
        <div class="form-group">
          <label for="informant" class="col-sm-4 control-label">Informant</label>
          <div class="col-sm-8">
            <select class="form-control" v-model="filterfelder.informant" id="informant">
              <option :value="informant.pk"
                v-for="informant in informantenListe"
                :key="'inf' + informant.pk"
                :disabled="informant.count == 0"
              >{{informant.kuerzelAnonym}}{{ informant.count > -1 ? ' - ' + informant.count.toLocaleString() : '' }}</option>
            </select>
          </div>
        </div>
      </div>
      <div class="col col-md-6">
        <div class="form-group">
          <label for="transkript" class="col-sm-4 control-label">Transkript</label>
          <div class="col-sm-8">
            <select class="form-control" v-model="filterfelder.transkript" id="transkript">
              <option :value="transcript.pk"
                v-for="transcript in transcriptsListe"
                :key="'ts' + transcript.pk"
                :disabled="transcript.count == 0"
              >{{transcript.name}}{{ transcript.count > -1 ? ' - ' + transcript.count.toLocaleString() : '' }}</option>
            </select>
          </div>
        </div>
        <div class="form-group">
          <label for="aufgabensets" class="col-sm-4 control-label">Aufgabensets</label>
          <div class="col-sm-8">
            <select class="form-control" v-model="filterfelder.aufgabenset" id="aufgabensets">
              <option :value="aufgabeset.pk"
                v-for="aufgabeset in aufgabensetListe"
                :key="'as' + aufgabeset.pk"
                :disabled="aufgabeset.count == 0"
              >{{aufgabeset.name}}{{ aufgabeset.count > -1 ? ' - ' + aufgabeset.count.toLocaleString() : '' }}</option>
            </select>
          </div>
        </div>
        <div class="form-group">
          <label for="aufgaben" class="col-sm-4 control-label">Aufgaben</label>
          <div class="col-sm-8">
            <select class="form-control" v-model="filterfelder.aufgabe" id="aufgaben">
              <option :value="aufgabe.pk"
                v-for="aufgabe in aufgabenListe"
                :key="'a' + aufgabe.pk"
                :disabled="aufgabe.count == 0"
              >{{aufgabe.name}}{{ aufgabe.count > -1 ? ' - ' + aufgabe.count.toLocaleString() : '' }}</option>
            </select>
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
      showCount: true,
      showCountTrans: false
    }
  },
  computed: {
    tagListe () {
      let aTagListe = []
      if (!this.tagsData.data.loading && !this.tagsData.data.loadingTags) {
        let gTag = function (aThis, sTag, deep = 0) {
          let sTagListe = [{pk: sTag.pk, title: (deep > 0 ? '- '.repeat(deep) : '') + sTag.t + ((sTag.tl && sTag.t !== sTag.tl) ? ' (' + sTag.tl + ')' : '')}]
          if (sTag.c) {
            sTag.c.forEach(sTagId => {
              sTagListe = [...sTagListe, ...gTag(aThis, aThis.tagsData.data.tagsCache.tags[sTagId], deep + 1)]
            })
          }
          return sTagListe
        }
        this.tagsData.data.tagsCache.tagsReihung.forEach(aTagId => {
          let aTag = this.tagsData.data.tagsCache.tags[aTagId]
          if (!aTag.p) {
            if (this.filterfelder.tagebene < 1 || !aTag.tezt || aTag.tezt.indexOf(this.filterfelder.tagebene) > -1) {
              aTagListe = [...aTagListe, ...gTag(this, aTag)]
            }
          }
        })
      }
      // console.log(aTagListe)
      return aTagListe
    }
  },
  mounted () {
    console.log('filterfelder', this.filterfelder)
    this.getFilterData()
  },
  methods: {
    getFilterData () {    // Informationen für Filter laden
      this.loading = true
      this.loadInfos = 'Filter Daten'
      this.http.post('', {
        getFilterData: true,
        showCount: this.showCount,
        showCountTrans: this.showCountTrans,
        filter: JSON.stringify({ ebene: this.filterfelder.tagebene, tag: this.filterfelder.tag, nichttag: this.filterfelder.nichtTag, inf: this.filterfelder.informant, trans: this.filterfelder.transkript, aufgabenset: this.filterfelder.aufgabenset, aufgabe: this.filterfelder.aufgabe })
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
</style>

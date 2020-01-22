<template>
  <div class="annosent-filtern form-horizontal">
    <div class="form-group">
      <div class="col-sm-offset-4 col-sm-8">
        <button class="form-control-static btn btn-success w100" @click="loadMatViewData(true)" :title="mvDurchschnitt > 0 ? 'Letzter Refresh: ' + mvLastUpdate + ' Uhr, Durchschnittliche Dauer ca. ' + mvDurchschnitt + ' Sekunden' : ''"><b>Refresh Materialized View</b></button>
      </div>
    </div>
    <div class="form-group">
      <label for="informant" class="col-sm-4 control-label">Informant</label>
      <div class="col-sm-8">
        <select class="form-control" v-model="filterfelder.informant" id="informant">
          <option value="0">Alle</option>
          <option :value="informant.pk" v-for="informant in infTransListFiltered" :key="'inf' + informant">{{informant.modelStr}} - {{informant.transcriptsPKs.length}} Transkripte</option>
        </select>
      </div>
    </div>
    <div class="form-group">
      <label for="transkript" class="col-sm-4 control-label">Transkript</label>
      <div class="col-sm-8">
        <select class="form-control" v-model="filterfelder.transkript" id="transkript">
          <option value="0">Alle</option>
          <option :value="transcript.pk" v-for="transcript in transcriptsListFiltered" :key="'ts' + transcript">{{transcript.name}}</option>
        </select>
      </div>
    </div>
    <div class="form-group">
      <label for="tagebene" class="col-sm-4 control-label">Tag Ebene</label>
      <div class="col-sm-8">
        <select class="form-control" v-model="filterfelder.tagebene" id="tagebene">
          <option value="0">Auswählen</option>
          <option :value="tagebene.pk" v-for="tagebene in tagebenenListe" :key="'te' + tagebene">{{ tagebene.t }}</option>
        </select>
      </div>
    </div>
    <div class="form-group">
      <label for="tagebene" class="col-sm-4 control-label" title="Bearbeitungsmodus">Modus</label>
      <div class="col-sm-8">
        <select class="form-control" v-model="filterfelder.bearbeitungsmodus" id="bearbeitungsmodus">
          <option value="direkt">Direkt</option>
          <option value="auswahl">Auswahl</option>
        </select>
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
      mvLastUpdate: 'Unbekannt ...'
    }
  },
  computed: {
    tagebenenListe () {
      return this.tagsData.data.ready ? this.tagsData.data.baseCache.tagebenenList : []
    },
    infTransListFiltered () {
      if (this.filterfelder.transkript > 0) {
        let infTransList = []
        this.infTrans.data.infTransList.forEach(informant => {
          if (informant.transcriptsPKs.indexOf(this.filterfelder.transkript) > -1) {
            infTransList.push(informant)
          }
        }, this)
        return infTransList
      }
      return this.infTrans.data.infTransList
    },
    transcriptsListFiltered () {
      if (this.filterfelder.informant > 0) {
        let transcriptsList = []
        this.infTrans.data.transcriptsList.forEach(transcript => {
          if (this.infTrans.data.infTransObj[this.filterfelder.informant].transcriptsPKs.indexOf(transcript.pk) > -1) {
            transcriptsList.push(transcript)
          }
        }, this)
        return transcriptsList
      }
      return this.infTrans.data.transcriptsList
    }
  },
  mounted () {
    console.log(this.filterfelder)
    this.loadMatViewData()
    this.getTranscriptsInfList()
  },
  methods: {
    getTranscriptsInfList () {    // Informationen zu Informanten und Transkripten laden
      this.loading = true
      this.loadInfos = ''
      this.http.post('/annotationsdb/startvue', { getTranscriptsInfList: 1 })
        .then((response) => {
          this.infTrans.data.infTransList = response.data['informanten']
          this.infTrans.data.infTransObj = {}
          for (let aInfKey in this.infTrans.data.infTransList) {
            this.infTrans.data.infTransList[aInfKey].transcriptsPKs = this.infTrans.data.infTransList[aInfKey].transcriptsPKs.filter(function (el) { return el != null })   // Null Werte filtern!
            // Objekt mit PK als Property erstellen
            if (this.infTrans.data.infTransList.hasOwnProperty(aInfKey)) {
              let aInf = this.infTrans.data.infTransList[aInfKey]
              this.infTrans.data.infTransObj[aInf.pk] = aInf
            }
          }
          this.infTrans.data.transcriptsList = response.data['transcripts']
          this.infTrans.data.transcriptsObj = {}
          for (let aTransKey in this.infTrans.data.transcriptsList) {
            // Objekt mit PK als Property erstellen
            if (this.infTrans.data.transcriptsList.hasOwnProperty(aTransKey)) {
              let aTrans = this.infTrans.data.transcriptsList[aTransKey]
              this.infTrans.data.transcriptsObj[aTrans.pk] = aTrans
            }
          }
          this.infTrans.data.loaded = true
          this.loading = false
        })
        .catch((err) => {
          console.log(err)
          alert('Fehler!')
          this.loading = false
        })
    },
    loadMatViewData (refresh = false) {   // Informationen zu letzten Materialized View Refreshes laden
      if (!this.loading || !refresh) {
        if (refresh) {
          this.loading = true
          this.loadInfos = 'Die letzten 5 Aktuallisierungen haben durchschnittlich ' + this.mvDurchschnitt.toFixed(1) + ' Sekunden gedauert ...'
        }
        this.http.post('', {
          getMatViewData: 1,
          refresh: refresh
        }).then((response) => {
          this.mvDurchschnitt = response.data.mvDurchschnitt
          this.mvLastUpdate = response.data.mvLastUpdate
          if (refresh) {
            this.loading = false
          }
        }).catch((err) => {
          console.log(err)
          alert('Fehler!')
          if (refresh) {
            this.loading = false
          }
        })
      }
    }
  }
}
</script>

<style scoped>
.annosent-filtern {
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

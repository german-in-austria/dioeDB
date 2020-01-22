<template>
  <Modal ref="modal" :modalData="modalData" :blocked="changed" @closed="$emit('closed')" :locked="locked">
    <template v-slot:title>Antwort bearbeiten: <b>ID {{ eintrag.id }}</b></template>

    <div class="form-horizontal">
      <div class="form-group">
        <label class="col-sm-2 control-label">Antwort</label>
        <div class="col-sm-10">
          <p class="form-control-static">{{ eintrag.id + (eintrag.deleteIt ? ' - Wird gelöscht !!!' : '') }}
            <template v-if="!(eintrag.tags && eintrag.tags.length > 0)">
              <button type="button" @click="$set(eintrag, 'deleteIt', true); changed = true" class="btn btn-danger btn-xs ml10 mt-5" v-if="!eintrag.deleteIt"><span class="glyphicon glyphicon-trash" aria-hidden="true"></span></button>
              <button type="button" @click="$set(eintrag, 'deleteIt', false); changed = true" class="btn btn-danger btn-xs ml10 mt-5" v-else><span class="glyphicon glyphicon-trash" aria-hidden="true"></span></button>
            </template>
          </p>
        </div>
      </div>
      <template v-if="tokenSatz && tokenSatz.length > 0">
        <div class="satzview">
          <span
            v-for="sToken in tokenSatz"
            :key="'st' + sToken.id"
            :title="'ID: ' + sToken.id"
            :class="'s-tok s-tok-tt' + sToken.token_type_id_id + (sToken.id === eintrag.ist_token_id ? ' s-tok-act' : '')"
          >{{
              ((!sToken.fragment_of_id && sToken.token_type_id_id !== 2) ? ' ' : '') +
              (sToken.ortho === null ? (!sToken.text_in_ortho ? sToken.text : sToken.text_in_ortho) : sToken.ortho)
           }}</span>
        </div>
      </template>
      <template v-else-if="tokenSetsSatz && tokenSetsSatz.length > 0">
        <div class="satzview">
          <span
            v-for="sToken in tokenSetsSatz"
            :key="'st' + sToken.id"
            :title="'ID: ' + sToken.id"
            :class="'s-tok s-tok-tt' + sToken.token_type_id_id + (sToken.tb === 1 ? ' s-tok-act' : '')"
          >{{
              ((!sToken.fragment_of_id && sToken.token_type_id_id !== 2) ? ' ' : '') +
              (sToken.ortho === null ? (!sToken.text_in_ortho ? sToken.text : sToken.text_in_ortho) : sToken.ortho)
          }}</span>
        </div>
      </template>
      <template v-else-if="eintrag.aOrtho">
        <div class="satzview">
          {{ eintrag.aOrtho }}
        </div>
      </template>
      <template v-if="tagsData.data.ready && eintrag && !eintrag.deleteIt">
        <Tagsystem :tagsData="tagsData" :tags="eintrag.tags" @changed="tagChange" :http="http" mode="edit" v-if="eintrag.tags" />
        <div v-else-if="tagsData.data.ready && tagsData.data.tagsCache && tagsData.data.tagsCache.tags">
          {{ processRawTags(eintrag, eintrag.antwortentags_raw) }}
        </div>
        <div v-else>Tags laden noch ...</div>
      </template>
    </div>

    <div class="loading" v-if="loading">Lade ...</div>

    <template v-slot:addButtons>
      <button type="button" class="btn btn-primary" :disabled="!changed" @click="saveTokenData">Speichern</button>
    </template>
    <template v-slot:closeButtonsText>{{ ((changed) ? 'Verwerfen' : 'Schließen') }}</template>
  </Modal>
</template>

<script>
/* global tagsystem _ */
import Modal from './Modal'

export default {
  name: 'AntwortenEdit',
  props: ['eintrag', 'http', 'tagsData', 'infTrans', 'filterfelder'],
  data () {
    return {
      changed: false,
      locked: false,
      loading: false,
      tokenSatz: [],
      tokenSetsSatz: []
    }
  },
  mounted () {
    console.log(this.eintrag, this.filterfelder)
    this.getTokenSatz()
    this.getTokenSetsSatz()
  },
  beforeDestroy () {
    if (this.changed) {
      this.$emit('changed')
    }
  },
  methods: {
    getTokenSetsSatz () {
      if (this.eintrag.ist_tokenset_id > 0) {
        let aTokenSetsIds = [this.eintrag.ist_tokenset_id]
        this.http.post('', {
          getTokenSetsSatz: true,
          tokenSetsIds: aTokenSetsIds
        }).then((response) => {
          console.log('getTokenSetsSatz', response.data)
          this.tokenSetsSatz = response.data.aTokenSetSatz[Object.keys(response.data.aTokenSetSatz)[0]]
          this.tokenSetsSatz.sort((a, b) => (a.token_reihung > b.token_reihung) ? 1 : ((b.token_reihung > a.token_reihung) ? -1 : 0))
        }).catch((err) => {
          console.log(err)
          alert('Fehler!')
        })
      }
    },
    getTokenSatz () {
      if (this.eintrag.ist_token_id > 0) {
        this.http.post('', {
          getTokenSatz: true,
          tokenId: this.eintrag.ist_token_id
        }).then((response) => {
          console.log('getTokenSatz', response.data)
          this.tokenSatz = response.data.aTokenSatz
          this.tokenSatz.sort((a, b) => (a.token_reihung > b.token_reihung) ? 1 : ((b.token_reihung > a.token_reihung) ? -1 : 0))
        }).catch((err) => {
          console.log(err)
          alert('Fehler!')
        })
      }
    },
    saveTokenData () {
      // Änderungen speichern.
      this.loading = true
      this.locked = true
      let sAntworten = []
      // Antworten mit Tags für Speicherung sammeln
      if (this.eintrag) {
        let sAntwort = _.cloneDeep(this.eintrag)
        delete sAntwort.antwortentags_raw
        delete sAntwort.aOrtho
        delete sAntwort.aSaetze
        delete sAntwort.aTokens
        delete sAntwort.aTokensText
        delete sAntwort.vSatz
        delete sAntwort.nSatz
        delete sAntwort.Tagebenen
        delete sAntwort.Reihung
        delete sAntwort.Transkript
        delete sAntwort.tId
        delete sAntwort.zu_Aufgabe_id
        delete sAntwort.aufVar
        delete sAntwort.aufBe
        delete sAntwort.antType
        delete sAntwort.aInf
        delete sAntwort.ist_token_id
        delete sAntwort.ist_tokenset_id
        sAntwort.tags = this.getFlatTags(sAntwort.tags)
        sAntworten.push(sAntwort)
      }
      console.log('sAntworten', sAntworten)
      // Speichern
      this.http.post('', {
        saveAntworten: true,
        antworten: JSON.stringify(sAntworten)
      }).then((response) => {
        console.log(response.data)
        this.loading = false
        this.locked = false
        this.$nextTick(() => {
          this.$refs.modal.close()
        })
      }).catch((err) => {
        console.log(err)
        alert('Fehler!')
        this.loading = false
        this.locked = false
      })
    },
    tagChange () {
      this.changed = true
    },
    processRawTags (antwort, rawTags) {
      let outTags = []
      if (rawTags && rawTags.length > 0) {
        // console.log('rawTags', rawTags)
        let cTags = this.tagsData.data.tagsCache.tags
        let getTagFamilie = function (tags) {
          let afam = []
          let oTags = []
          tags.forEach((tag) => {
            let pClose = 0
            if (afam.length) {
              let wDg = 0
              let childOfPreviousTag = false
              do {
                if (afam.length && cTags[tag.id_Tag_id].p && cTags[tag.id_Tag_id].p.length) {
                  childOfPreviousTag = cTags[tag.id_Tag_id].p.indexOf(afam[afam.length - 1]) > -1
                }
                if (!childOfPreviousTag) {
                  pClose += 1
                  afam.pop()
                }
                wDg += 1
              } while (afam.length && !childOfPreviousTag && wDg < 99)
            }
            oTags.push({t: tag.id_Tag_id, i: tag.id, c: pClose})
            afam.push(tag.id_Tag_id)
          }, this)
          // console.log('oTags', JSON.parse(JSON.stringify(oTags)))
          return oTags
        }
        let tagsByEbene = {}
        rawTags.forEach((tag) => {
          if (!tagsByEbene[tag.id_TagEbene_id]) {
            tagsByEbene[tag.id_TagEbene_id] = []
          }
          tagsByEbene[tag.id_TagEbene_id].push(tag)
        }, this)
        // console.log('tagsByEbene', tagsByEbene)
        Object.keys(tagsByEbene).forEach((ebenenId) => {
          let gTF = getTagFamilie(tagsByEbene[ebenenId])
          let pTags = []
          if (gTF) {
            pTags = this.processTags(gTF).tags
          }
          outTags.push({e: parseInt(ebenenId), 'tags': pTags})
        }, this)
        // console.log('outTags', outTags)
      }
      this.$set(antwort, 'tags', outTags)
      return 'Verarbeite Tokens ...'
    },
    processTags: function (pTags, pPos = 0) {
      var xTags = []
      var xPos = pPos
      var xClose = 0
      while (xPos < pTags.length && xClose < 1) {
        if (pTags[xPos].c > 0) {
          xClose = pTags[xPos].c
          pTags[xPos].c -= 1
          xPos = xPos - 1
        } else {
          var prData = this.processTags(pTags, xPos + 1)
          var zTags = prData.tags
          var zPos = prData.pos
          xTags.push({'id': pTags[xPos].i, 'tag': pTags[xPos].t, 'tags': zTags})
          xPos = zPos + 1
        }
      }
      return {'tags': xTags, 'pos': xPos}
    },
    getFlatTags (aTags) {
      let fTags = []
      aTags.forEach(function (val) {
        fTags.push({'e': val.e, 't': this.getFlatTagsX(val.tags)})
      }, this)
      return fTags
    },
    getFlatTagsX (aTags) {
      let fTags = []
      aTags.forEach(function (val) {
        let aTag = {'i': val.id, 't': val.tag}
        fTags.push(aTag)
        if (val.tags) {
          this.getFlatTagsX(val.tags).forEach(function (sval) {
            fTags.push(sval)
          })
        }
      }, this)
      return fTags
    },
    getFirstObjectOfValueInPropertyOfArray (arr, property, value, returnObj) {
      let rObj = ((returnObj) ? {} : null)
      if (Array.isArray(arr)) {
        arr.some(function (aVal, aKey) {
          if (aVal[property] && aVal[property] === value) {
            rObj = aVal
            return true
          }
        })
      }
      return rObj
    }
  },
  computed: {
  },
  watch: {
  },
  components: {
    Modal,
    Tagsystem: tagsystem.TagsystemVue
  }
}
</script>

<style scoped>
.loading {
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}
.satzview {
  padding: 10px 50px;
  margin: 10px 0px;
  border-top: 1px solid #ddd;
  border-bottom: 1px solid #ddd;
}
.s-tok {
  color: #888;
}
.s-tok-act {
  font-weight: bold;
  color: #333;
}
</style>

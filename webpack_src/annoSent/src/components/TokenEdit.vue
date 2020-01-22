<template>
  <Modal ref="modal" :modalData="modalData" :blocked="changed" @closed="$emit('closed')" :locked="locked">
    <template v-slot:title>Token bearbeiten: <b>{{ token.text }}</b> ({{ token.id }})</template>

    <div class="form-horizontal">
      <div class="form-group">
        <label for="aTokenID" class="col-sm-2 control-label">ID</label>
        <div class="col-sm-2"><p class="form-control-static" id="aTokenID">{{ token.id }}</p></div>
        <label for="aTokenIDInf" class="col-sm-2 control-label">ID_Inf</label>
        <div class="col-sm-2"><p class="form-control-static" id="aTokenIDInf">{{ tokenInfModel }}</p></div>
        <label for="aTokenType" class="col-sm-2 control-label">token_type</label>
        <div class="col-sm-2"><p class="form-control-static" id="aTokenType">{{ token.token_type_id_id }}</p></div>
      </div>
      <div class="form-group">
        <label for="aTokenReihung" class="col-sm-2 control-label">token_reihung</label>
        <div class="col-sm-2"><p class="form-control-static" id="aTokenReihung">{{ token.token_reihung }}</p></div>
        <label for="aTokenSentenceID" class="col-sm-2 control-label">sentence_id</label>
        <div class="col-sm-2"><p class="form-control-static" id="aTokenSentenceID">{{ tokenSatzModel }}</p></div>
        <label for="aTokenSequenceInSentence" class="col-sm-2 control-label" title="sequence_in_sentence">seq_in_sentence</label>
        <div class="col-sm-2"><p class="form-control-static" id="aTokenSequenceInSentence">{{ token.sequence_in_sentence }}</p></div>
      </div>
      <div class="form-group">
        <label for="aTokenEventID" class="col-sm-2 control-label">event_id</label>
        <div class="col-sm-2"><p class="form-control-static" id="aTokenEventID">{{ tokenEvent }}</p></div>
        <label for="aTokenLikelyError" class="col-sm-2 control-label">likely_error</label>
        <div class="col-sm-2"><p class="form-control-static" id="aTokenLikelyError">{{ token.likely_error ? 'Ja' : 'Nein' }}</p></div>
      </div>
      <div class="form-group">
        <label for="aTokenText" class="col-sm-2 control-label">text</label>
        <div class="col-sm-4"><p class="form-control-static" id="aTokenText">{{ token.text }}</p></div>
        <label for="aTokenOrtho" class="col-sm-2 control-label">ortho</label>
        <div class="col-sm-4"><p class="form-control-static" id="aTokenOrtho">{{ token.ortho }}</p></div>
      </div>
      <div class="form-group">
        <label for="aTokenTextInOrtho" class="col-sm-2 control-label">text_in_ortho</label>
        <div class="col-sm-4"><p class="form-control-static" id="aTokenTextInOrtho">{{ token.text_in_ortho }}</p></div>
        <label for="aTokenfragmentof" class="col-sm-2 control-label">fragment_of</label>
        <div class="col-sm-4"><p class="form-control-static" id="aTokenfragmentof">{{ tokenFragmentOf }}</p></div>
      </div>
      <!-- <div class="form-group" v-if="transcript.aTokens.aTokenFragmenteObj[aToken.pk]"><label class="col-sm-3 control-label">Fragmente</label><div class="col-sm-9"><ul class="form-control-static hflist">
          <li v-for="aToFragKey in transcript.aTokens.aTokenFragmenteObj[aToken.pk]" :key="'aTFO' + aToFragKey">{{ transcript.aTokens.tokensObj[aToFragKey].t }} ({{ aToFragKey }})</li>
      </ul></div></div> -->
      <br><h4><b>Token:</b></h4><hr>
      <div class="form-group">
        <label class="col-sm-2 control-label">Antwort</label>
        <div class="col-sm-10">
          <p class="form-control-static" v-if="token.antworten && token.antworten.length > 0">{{ token.antworten[0].id + (0 > token.antworten[0].id ? ' - Neu' : '') + (token.antworten[0].deleteIt ? ' - Wird gelöscht !!!' : '') }}
            <template v-if="!(token.antworten[0].tags && token.antworten[0].tags.length > 0) && (token.antworten.length !== 0)">
              <button type="button" @click="$set(token.antworten[0], 'deleteIt', true); changed = true" class="btn btn-danger btn-xs ml10 mt-5" v-if="!token.antworten[0].deleteIt"><span class="glyphicon glyphicon-trash" aria-hidden="true"></span></button>
              <button type="button" @click="$set(token.antworten[0], 'deleteIt', false); changed = true" class="btn btn-danger btn-xs ml10 mt-5" v-else><span class="glyphicon glyphicon-trash" aria-hidden="true"></span></button>
            </template>
          </p>
          <button type="button" @click="addTokenAntwort()" class="btn btn-primary" v-else>Antwort erstellen</button>
        </div>
      </div>
      <template v-if="tokenSatz && tokenSatz.length > 0">
        <div class="satzview">
          <span
            v-for="sToken in tokenSatz"
            :key="'st' + sToken.id"
            :title="'ID: ' + sToken.id"
            :class="'s-tok s-tok-tt' + sToken.token_type_id_id + (sToken.id === token.id ? ' s-tok-act' : '')"
          >{{
              ((!sToken.fragment_of_id && sToken.token_type_id_id !== 2) ? ' ' : '') +
              (sToken.ortho === null ? (!sToken.text_in_ortho ? sToken.text : sToken.text_in_ortho) : sToken.ortho)
           }}</span>
        </div>
      </template>
      <template v-if="tagsData.data.ready && token.antworten && token.antworten.length > 0 && !token.antworten[0].deleteIt">
        <Tagsystem :tagsData="tagsData" :tags="token.antworten[0].tags" @changed="tagChange" :http="http" mode="edit" v-if="token.antworten[0].tags" />
        <div v-else-if="tagsData.data.ready && tagsData.data.tagsCache && tagsData.data.tagsCache.tags">
          {{ processRawTags(token.antworten[0], token.antworten[0].antwortentags_raw) }}
        </div>
        <div v-else>Tags laden noch ...</div>
        <hr>
      </template>
      <template v-if="tokenSetsBereiche.length > 0">
        <br><h4><b>Tokensets:</b> Bereiche</h4><hr>
        <div v-for="tokenSet in tokenSetsBereiche" :key="'tsb' + tokenSet">
          <div class="form-group">
            <label class="col-sm-2 control-label">TokenSet ID</label>
            <div class="col-sm-4"><p class="form-control-static">{{ tokenSet.id }}</p></div>
            <label class="col-sm-2 control-label">Antwort</label>
            <div class="col-sm-4">
              <p class="form-control-static" v-if="tokenSet.antworten && tokenSet.antworten.length > 0">{{ tokenSet.antworten[0].id + (0 > tokenSet.antworten[0].id ? ' - Neu' : '') + (tokenSet.antworten[0].deleteIt ? ' - Wird gelöscht !!!' : '') }}
                <template v-if="!(tokenSet.antworten[0].tags && tokenSet.antworten[0].tags.length > 0) && (tokenSet.antworten.length !== 0)">
                  <button type="button" @click="$set(tokenSet.antworten[0], 'deleteIt', true); changed = true" class="btn btn-danger btn-xs ml10 mt-5" v-if="!tokenSet.antworten[0].deleteIt"><span class="glyphicon glyphicon-trash" aria-hidden="true"></span></button>
                  <button type="button" @click="$set(tokenSet.antworten[0], 'deleteIt', false); changed = true" class="btn btn-danger btn-xs ml10 mt-5" v-else><span class="glyphicon glyphicon-trash" aria-hidden="true"></span></button>
                </template>
              </p>
              <button type="button" @click="addTokenSetAntwort(tokenSet)" class="btn btn-primary" v-else>Antwort erstellen</button>
            </div>
          </div>
          <template v-if="tokenSet.satz && tokenSet.satz.length > 0">
            <div class="satzview">
              <span
                v-for="sToken in tokenSet.satz"
                :key="'st' + sToken.id"
                :title="'ID: ' + sToken.id"
                :class="'s-tok s-tok-tt' + sToken.token_type_id_id + (sToken.tb === 1 ? ' s-tok-act' : '')"
              >{{
                  ((!sToken.fragment_of_id && sToken.token_type_id_id !== 2) ? ' ' : '') +
                  (sToken.ortho === null ? (!sToken.text_in_ortho ? sToken.text : sToken.text_in_ortho) : sToken.ortho)
              }}</span>
            </div>
          </template>
          <template v-if="tagsData.data.ready && tokenSet.antworten && tokenSet.antworten.length > 0 && !tokenSet.antworten[0].deleteIt">
            <Tagsystem :tagsData="tagsData" :tags="tokenSet.antworten[0].tags" @changed="tagChange" :http="http" mode="edit" v-if="tokenSet.antworten[0].tags" />
            <div v-else-if="tagsData.data.ready && tagsData.data.tagsCache && tagsData.data.tagsCache.tags">
              {{ processRawTags(tokenSet.antworten[0], tokenSet.antworten[0].antwortentags_raw) }}
            </div>
            <div v-else>Tags laden noch ...</div>
            <hr>
          </template>
        </div>
      </template>
      <template v-if="tokenSetsListen.length > 0">
        <br><h4><b>Tokensets:</b> Listen</h4><hr>
        <div v-for="tokenSet in tokenSetsListen" :key="'tsl' + tokenSet">
          <div class="form-group">
            <label class="col-sm-2 control-label">TokenSet ID</label>
            <div class="col-sm-4"><p class="form-control-static">{{ tokenSet.id }}</p></div>
            <label class="col-sm-2 control-label">Antwort</label>
            <div class="col-sm-4">
              <p class="form-control-static" v-if="tokenSet.antworten && tokenSet.antworten.length > 0">{{ tokenSet.antworten[0].id + (0 > tokenSet.antworten[0].id ? ' - Neu' : '') + (tokenSet.antworten[0].deleteIt ? ' - Wird gelöscht !!!' : '') }}
                <template v-if="!(tokenSet.antworten[0].tags && tokenSet.antworten[0].tags.length > 0) && (tokenSet.antworten.length !== 0)">
                  <button type="button" @click="$set(tokenSet.antworten[0], 'deleteIt', true); changed = true" class="btn btn-danger btn-xs ml10 mt-5" v-if="!tokenSet.antworten[0].deleteIt"><span class="glyphicon glyphicon-trash" aria-hidden="true"></span></button>
                  <button type="button" @click="$set(tokenSet.antworten[0], 'deleteIt', false); changed = true" class="btn btn-danger btn-xs ml10 mt-5" v-else><span class="glyphicon glyphicon-trash" aria-hidden="true"></span></button>
                </template>
              </p>
              <button type="button" @click="addTokenSetAntwort(tokenSet)" class="btn btn-primary" v-else>Antwort erstellen</button>
            </div>
          </div>
          <template v-if="tokenSet.satz && tokenSet.satz.length > 0">
            <div class="satzview">
              <span
                v-for="sToken in tokenSet.satz"
                :key="'st' + sToken.id"
                :title="'ID: ' + sToken.id"
                :class="'s-tok s-tok-tt' + sToken.token_type_id_id + ((getFirstObjectOfValueInPropertyOfArray(tokenSet.tokentoset, 'id_token_id', sToken.id, false)) ? ' s-tok-act' : '')"
              >{{
                  ((!sToken.fragment_of_id && sToken.token_type_id_id !== 2) ? ' ' : '') +
                  (sToken.ortho === null ? (!sToken.text_in_ortho ? sToken.text : sToken.text_in_ortho) : sToken.ortho)
              }}</span>
            </div>
          </template>
          <template v-if="tagsData.data.ready && tokenSet.antworten && tokenSet.antworten.length > 0 && !tokenSet.antworten[0].deleteIt">
            <Tagsystem :tagsData="tagsData" :tags="tokenSet.antworten[0].tags" @changed="tagChange" :http="http" mode="edit" v-if="tokenSet.antworten[0].tags" />
            <div v-else-if="tagsData.data.ready && tagsData.data.tagsCache && tagsData.data.tagsCache.tags">
              {{ processRawTags(tokenSet.antworten[0], tokenSet.antworten[0].antwortentags_raw) }}
            </div>
            <div v-else>Tags laden noch ...</div>
            <hr>
          </template>
        </div>
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
  name: 'TokenEdit',
  props: ['token', 'eintrag', 'http', 'tagsData', 'infTrans', 'filterfelder'],
  data () {
    return {
      changed: false,
      locked: false,
      loading: false,
      tokenSatz: []
    }
  },
  mounted () {
    console.log(this.token, this.filterfelder)
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
      if (this.token.tokensets && this.token.tokensets.length > 0) {
        let aTokenSetsIds = []
        this.token.tokensets.forEach((ts) => {
          aTokenSetsIds.push(ts.id)
        }, this)
        this.http.post('', {
          getTokenSetsSatz: true,
          tokenSetsIds: aTokenSetsIds
        }).then((response) => {
          console.log(response.data)
          this.token.tokensets.forEach((ts) => {
            if (response.data.aTokenSetSatz[ts.id]) {
              this.$set(ts, 'satz', response.data.aTokenSetSatz[ts.id])
              ts.satz.sort((a, b) => (a.token_reihung > b.token_reihung) ? 1 : ((b.token_reihung > a.token_reihung) ? -1 : 0))
            }
          }, this)
        }).catch((err) => {
          console.log(err)
          alert('Fehler!')
        })
      }
    },
    getTokenSatz () {
      this.http.post('', {
        getTokenSatz: true,
        tokenId: this.token.id
      }).then((response) => {
        console.log(response.data)
        this.tokenSatz = response.data.aTokenSatz
        this.tokenSatz.sort((a, b) => (a.token_reihung > b.token_reihung) ? 1 : ((b.token_reihung > a.token_reihung) ? -1 : 0))
      }).catch((err) => {
        console.log(err)
        alert('Fehler!')
      })
    },
    saveTokenData () {
      // Änderungen speichern.
      this.loading = true
      this.locked = true
      let sAntworten = []
      // Antworten mit Tags für Speicherung sammeln
      if (this.token.antworten && this.token.antworten[0]) {
        let sAntwort = _.cloneDeep(this.token.antworten[0])
        delete sAntwort.antwortentags_raw
        sAntwort.tags = this.getFlatTags(sAntwort.tags)
        sAntworten.push(sAntwort)
      }
      if (this.token.tokensets && this.token.tokensets.length > 0) {
        this.token.tokensets.forEach((ts) => {
          if (ts.antworten && ts.antworten[0]) {
            let sAntwort = _.cloneDeep(ts.antworten[0])
            delete sAntwort.antwortentags_raw
            sAntwort.tags = this.getFlatTags(sAntwort.tags)
            sAntworten.push(sAntwort)
          }
        }, this)
      }
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
    addTokenAntwort () {
      if (!Array.isArray(this.token.antworten)) {
        this.token.antworten = []
      }
      this.token.antworten.push({id: -1, ist_token_id: this.token.id, von_Inf_id: this.token.ID_Inf_id, tags: []})
      this.changed = true
    },
    addTokenSetAntwort (tokenset) {
      if (!Array.isArray(tokenset.antworten)) {
        tokenset.antworten = []
      }
      tokenset.antworten.push({id: -1, ist_tokenset_id: tokenset.id, von_Inf_id: this.token.ID_Inf_id, tags: []})
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
    tokenEvent () {
      // TODO: {{ aToken.eObj.s }} - {{ aToken.eObj.e }} - ID: {{ aToken.e }}
      return this.token.event_id_id ? this.token.event_id_id : null
    },
    tokenFragmentOf () {
      // TODO: Text des Tokenfragments ...
      return this.token.fragment_of_id ? 'ID: ' + this.token.fragment_of_id : null
    },
    tokenInfModel () {
      return this.infTrans.data.loaded && this.infTrans.data.infTransObj[this.token.ID_Inf_id] ? this.infTrans.data.infTransObj[this.token.ID_Inf_id].modelStr : this.token.ID_Inf_id
    },
    tokenTransciptModel () {
      return this.infTrans.data.loaded && this.infTrans.data.transcriptsObj[this.token.transcript_id_id] ? this.infTrans.data.transcriptsObj[this.token.transcript_id_id].name : this.token.transcript_id_id
    },
    tokenSatzModel () {
      // TODO: {{ transcript.aSaetze[aToken.s].t }} - ID: {{ aToken.s }}
      return this.token.sentence_id_id ? 'ID: ' + this.token.sentence_id_id : null
    },
    tokenSetsBereiche () {
      let tsb = []
      if (this.token.tokensets && this.token.tokensets.length > 0) {
        this.token.tokensets.forEach((ts) => {
          if (ts.id_bis_token_id) {
            tsb.push(ts)
          }
        }, this)
      }
      return tsb
    },
    tokenSetsListen () {
      let tsb = []
      if (this.token.tokensets && this.token.tokensets.length > 0) {
        this.token.tokensets.forEach((ts) => {
          if (!ts.id_bis_token_id) {
            tsb.push(ts)
          }
        }, this)
      }
      return tsb
    }
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

<template>
  <Modal ref="modal" :modalData="modalData" :blocked="changed" @closed="$emit('closed')" :locked="locked">
    <template v-slot:title>Token Set bearbeiten: ({{ tokenSet.id }}) - {{ tokenSet.id_von_token_id ? 'Bereich' : 'Liste' }}</template>

    <div class="form-horizontal">
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
        <template v-if="satz && satz.length > 0">
          <div class="satzview">
            <span
              v-for="sToken in satz"
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
        </template>
    </div>

    <div class="loading" v-if="loading">Lade ...</div>

    <template v-slot:addButtons>
      <button type="button" class="btn btn-primary" :disabled="!changed" @click="saveTokenSetData">Speichern</button>
    </template>
    <template v-slot:closeButtonsText>{{ ((changed) ? 'Verwerfen' : 'Schließen') }}</template>
  </Modal>
</template>

<script>
/* global tagsystem _ */
import Modal from './Modal'

export default {
  name: 'TokenSetEdit',
  props: ['tokenSet', 'satz', 'http', 'tagsData', 'filterfelder'],
  data () {
    return {
      changed: false,
      locked: false,
      loading: false
    }
  },
  mounted () {
  },
  beforeDestroy () {
    if (this.changed) {
      this.$emit('changed')
    }
  },
  methods: {
    saveTokenSetData () {
      // Änderungen speichern.
      this.loading = true
      this.locked = true
      let sAntworten = []
      // Antworten mit Tags für Speicherung sammeln
      if (this.tokenSet.antworten && this.tokenSet.antworten[0]) {
        let sAntwort = _.cloneDeep(this.tokenSet.antworten[0])
        delete sAntwort.antwortentags_raw
        sAntwort.tags = this.getFlatTags(sAntwort.tags)
        sAntworten.push(sAntwort)
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
    addTokenSetAntwort (tokenset) {
      if (this.satz[0]) {
        if (!Array.isArray(tokenset.antworten)) {
          tokenset.antworten = []
        }
        tokenset.antworten.push({id: -1, ist_tokenset_id: tokenset.id, von_Inf_id: this.satz[0].ID_Inf_id, tags: []})
        this.changed = true
      } else {
        alert('Fehler! Token Set enthält keine Tokens!')
      }
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

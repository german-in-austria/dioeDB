<template>
  <div class="annosent-auswahl form-horizontal">
    <div class="form-group">
      <label for="seltokensets" class="col-sm-3 control-label">Token Set</label>
      <div class="col-sm-9">
        <div class="input-group">
          <select class="form-control" v-model="eintraege.data.selTokenSet" id="seltokensets">
            <option value="0">Auswählen ({{ Object.keys(eintraege.data.tokenSets).length }})</option>
            <option :value="-1" v-if="filterfelder.bearbeitungsmodus === 'auswahl'">Neues Token Set</option>
            <option
              :value="aTokenSet.id"
              v-for="aTokenSet in eintraege.data.tokenSets"
              :key="'ts' + aTokenSet.id"
            >
              ID: {{ aTokenSet.id + ', ' + (aTokenSet.id_von_token_id ? 'Bereich' : 'Liste' ) + (aTokenSet.antworten ? ', Antworten vorhanden' : '' ) }}
            </option>
          </select>
          <span class="input-group-btn">
            <button class="btn btn-default" @click="newTokenSet" type="button" title="Neues Tokenset erstellen."><span class="glyphicon glyphicon-file" aria-hidden="true"></span></button>
          </span>
        </div>
      </div>
    </div>
    <template v-if="filterfelder.bearbeitungsmodus === 'direkt'">
      <template v-if="satz[eintraege.data.selTokenSet] && Object.keys(satz[eintraege.data.selTokenSet]).length > 0 && eintraege.data.tokenSets[eintraege.data.selTokenSet]">
        <div :class="'satzview' + (!satzOpen ? ' closed' : '')">
          <div>
            <span
              v-for="sToken in satz[eintraege.data.selTokenSet]"
              :key="'st' + sToken.id"
              :title="'ID: ' + sToken.id"
              :class="'s-tok s-tok-tt' + sToken.token_type_id_id + ((getFirstObjectOfValueInPropertyOfArray(eintraege.data.tokenSets[eintraege.data.selTokenSet].tokentoset, 'id_token_id', sToken.id, false)) ? ' s-tok-act' : '')"
            >{{
                ((!sToken.fragment_of_id && sToken.token_type_id_id !== 2) ? ' ' : '') +
                (sToken.ortho === null ? (!sToken.text_in_ortho ? sToken.text : sToken.text_in_ortho) : sToken.ortho)
            }}</span>
          </div>
          <button @click="satzOpen = !satzOpen"><span :class="'glyphicon glyphicon-chevron-' + (satzOpen ? 'up' : 'down')" aria-hidden="true"></span></button>
        </div>
      </template>
      <div class="form-group" v-if="eintraege.data.selTokenSet > 0">
        <div class="col-sm-12">
          <button class="form-control-static btn btn-success w100" @click="showTokenSetEdit = true" title="Tags des aktuellen Token Sets bearbeiten.">Tags bearbeiten</button>
        </div>
      </div>
    </template>
    <template v-else-if="filterfelder.bearbeitungsmodus === 'auswahl'">
      <template v-if="eintraege.data.selTokenSet > 0">
        <div class="form-group">
          <div class="col-sm-offset-3 col-sm-9">
            <div class="btn-group w100">
              <button class="btn btn-primary" @click="selTokensOfSet" title="Momentane Auswahl verwerfen und Tokens des aktuellen Sets auswählen." style="width: calc(100% - 40px); padding-left:52px;">Tokens auswählen</button>
              <button class="btn btn-primary" @click="autoSelect = !autoSelect" title="Bei Wechsel des Token Sets automatisch auswählen." style="width:40px;"><span :class="'glyphicon glyphicon-' + (autoSelect ? 'check' : 'unchecked')" aria-hidden="true"></span></button>
            </div>
          </div>
        </div>
        <div class="form-group">
          <div class="col-sm-offset-3 col-sm-9">
            <button class="form-control-static btn btn-success w100" @click="showTokenSetEdit = true" title="Tags des aktuellen Token Sets bearbeiten." :disabled="!tokenSetSelectGleich && tokenSetAlleTokensVorhanden">Tags bearbeiten</button>
          </div>
        </div>
        <div class="form-group">
          <div class="col-sm-offset-3 col-sm-9">
            <div class="btn-group w100">
              <button class="btn btn-warning" @click="saveTokenSet" title="Aktuelles Token Set ändern und speichern!" :disabled="tokenSetSelectGleich" style="width: calc(100% - 40px); padding-left:52px;" v-if="tokenSetAlleTokensVorhanden">Token Set ändern</button>
              <button class="btn btn-default" @click="saveTokenSet" title="Es werden nicht alle Tokens angezeigt!" disabled style="width: calc(100% - 40px); padding-left:52px;" v-else>Token Set ändern</button>
              <button class="btn btn-danger" @click="deleteTokenSet" title="Aktuelles Token Set löschen!" style="width:40px;"><span class="glyphicon glyphicon-trash" aria-hidden="true"></span></button>
            </div>
          </div>
        </div>
      </template>
      <template v-else-if="eintraege.data.selTokenSet === -1">
        <div class="form-group">
          <div class="col-sm-offset-3 col-sm-9">
            <button class="form-control-static btn btn-primary w100" @click="selNone" title="Token Auswahl aufheben. (Strg + d)" :disabled="tokenSelectFlat.length < 1">Token Auswahl aufheben</button>
          </div>
        </div>
        <div class="form-group">
          <div class="col-sm-offset-3 col-sm-9">
            <button class="form-control-static btn btn-primary w100" @click="saveTokenSet" title="Aktuelles Token Set erstellen und speichern!" :disabled="tokenSelectFlat.length < 1">Token Set erstellen</button>
          </div>
        </div>
      </template>
    </template>
    <TokenSetEdit @closed="showTokenSetEdit = null" :tokenSet="eintraege.data.tokenSets[this.eintraege.data.selTokenSet]" :satz="satz[this.eintraege.data.selTokenSet]" :http="http" :tagsData="tagsData" :filterfelder="filterfelder" @changed="debouncedReload()" v-if="showTokenSetEdit && eintraege.data.selTokenSet > 0" />
    <div class="loading" v-if="$parent.$refs.tabelle && $parent.$refs.tabelle.loading">Lade ...</div>
  </div>
</template>

<script>
/* global _ */
import TokenSetEdit from './TokenSetEdit'

export default {
  name: 'Auswahl',
  props: ['eintraege', 'filterfelder', 'http', 'tagsData'],
  data () {
    return {
      satz: {},
      satzOpen: false,
      autoSelect: true,
      showTokenSetEdit: false,
      newTokenSetId: null
    }
  },
  mounted () {
    // console.log(this.eintraege.data.tokenSets)
    this.getTokenSetsSatz()
  },
  methods: {
    saveTokenSet () {
      if (this.eintraege.data.selTokenSet < 0 || confirm('Soll das Token Set mit ID "' + this.eintraege.data.tokenSets[this.eintraege.data.selTokenSet].id + '", das auf ' + this.eintraege.data.tokenSets[this.eintraege.data.selTokenSet].tokentoset.length + ' Tokens, jetzt ' + this.tokenSelectFlat.length + ' Tokens, verweist, wirklich geändert werden?')) {
        this.loading = true
        // Token Set speichern
        this.http.post('', {
          saveTokenSet: true,
          tokens: JSON.stringify(this.tokenSelectFlat),
          tokenSetId: (this.eintraege.data.selTokenSet > 0 ? this.eintraege.data.tokenSets[this.eintraege.data.selTokenSet].id : -1)
        }).then((response) => {
          console.log(response.data)
          this.loading = false
          this.newTokenSetId = response.data.tokenset_id
          this.$parent.$refs.tabelle.reload()
        }).catch((err) => {
          console.log(err)
          alert('Fehler!')
          this.loading = false
        })
      }
    },
    deleteTokenSet () {
      if (confirm('Soll das Token Set mit ID "' + this.eintraege.data.tokenSets[this.eintraege.data.selTokenSet].id + '", das auf ' + this.eintraege.data.tokenSets[this.eintraege.data.selTokenSet].tokentoset.length + ' Tokens verweist, wirklich unwiderruflich gelöschen werden?')) {
        this.loading = true
        // Token Set löschen
        this.http.post('', {
          delTokenSet: true,
          tokenSetId: this.eintraege.data.tokenSets[this.eintraege.data.selTokenSet].id
        }).then((response) => {
          console.log(response.data)
          this.loading = false
          this.$parent.$refs.tabelle.reload()
        }).catch((err) => {
          console.log(err)
          alert('Fehler!')
          this.loading = false
        })
      }
    },
    selNone () {
      this.eintraege.data.list.forEach((aEintrag) => {
        this.$set(aEintrag, 'selected', [])
      }, this)
    },
    selTokensOfSet () {
      if (this.eintraege.data.selTokenSet > 0 && this.eintraege.data.tokenSets[this.eintraege.data.selTokenSet] && this.eintraege.data.tokenSets[this.eintraege.data.selTokenSet].tokentoset) {
        this.eintraege.data.list.forEach((aEintrag) => {
          this.$set(aEintrag, 'selected', [])
          this.eintraege.data.tokenSets[this.eintraege.data.selTokenSet].tokentoset.forEach((tsid) => {
            aEintrag.tokens.forEach((aToken) => {
              if (tsid.id_token_id === aToken.id) {
                aEintrag.selected.push(aToken.id)
              }
            }, this)
          }, this)
        }, this)
      }
    },
    getTokenSetsSatz () {
      if (this.eintraege.data.tokenSets && Object.keys(this.eintraege.data.tokenSets).length > 0) {
        this.http.post('', {
          getTokenSetsSatz: true,
          tokenSetsIds: Object.keys(this.eintraege.data.tokenSets)
        }).then((response) => {
          // console.log('getTokenSetsSatz', response.data)
          this.satz = response.data.aTokenSetSatz
          Object.keys(this.satz).forEach((tsid) => {
            this.satz[tsid].sort((a, b) => (a.token_reihung > b.token_reihung) ? 1 : ((b.token_reihung > a.token_reihung) ? -1 : 0))
          }, this)
        }).catch((err) => {
          console.log(err)
          alert('Fehler!')
        })
      }
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
    },
    debouncedReload: _.debounce(function () {   // Einträge verzögert laden
      this.$parent.$refs.tabelle.reload()
    }, 300),
    newTokenSet () {
      this.filterfelder.bearbeitungsmodus = 'auswahl'
      this.eintraege.data.selTokenSet = -1
    }
  },
  computed: {
    tokenSelectFlat () {
      let aSelTokens = []
      this.eintraege.data.list.forEach((aEintrag) => {
        if (Array.isArray(aEintrag.selected)) {
          aSelTokens = [...aSelTokens, ...aEintrag.selected]
        }
      }, this)
      return aSelTokens
    },
    tokenSetAlleTokensVorhanden () {
      let avTokens = []
      if (this.eintraege.data.list && this.eintraege.data.selTokenSet > 0 && this.eintraege.data.tokenSets[this.eintraege.data.selTokenSet] && this.eintraege.data.tokenSets[this.eintraege.data.selTokenSet].tokentoset) {
        this.eintraege.data.list.forEach((aEintrag) => {
          avTokens = [...avTokens, ...aEintrag.tokenids]
        }, this)
        return this.eintraege.data.tokenSets[this.eintraege.data.selTokenSet].tokentoset.every((val) => avTokens.indexOf(val.id_token_id) > -1)
      }
      return false
    },
    tokenSetSelectGleich () {
      if (this.eintraege.data.selTokenSet > 0 && this.eintraege.data.tokenSets[this.eintraege.data.selTokenSet] && this.eintraege.data.tokenSets[this.eintraege.data.selTokenSet].tokentoset) {
        let aSelTokens = this.tokenSelectFlat
        aSelTokens = aSelTokens.sort()
        let aSelTokenSetTokens = []
        this.eintraege.data.tokenSets[this.eintraege.data.selTokenSet].tokentoset.forEach((aToken) => {
          aSelTokenSetTokens.push(aToken.id_token_id)
        }, this)
        aSelTokenSetTokens = aSelTokenSetTokens.sort()
        return aSelTokenSetTokens.length === aSelTokens.length && aSelTokenSetTokens.every((value, index) => value === aSelTokens[index])
      } else if (this.eintraege.data.selTokenSet < 0) {
        return false
      }
      return true
    }
  },
  watch: {
    'eintraege.data.tokenSets' (nVal) {
      this.$nextTick(() => {
        this.getTokenSetsSatz()
        if (this.newTokenSetId) {
          this.eintraege.data.selTokenSet = this.newTokenSetId
          this.newTokenSetId = null
        } else if (!this.eintraege.data.tokenSets[this.eintraege.data.selTokenSet] && this.eintraege.data.selTokenSet !== -1) {
          this.eintraege.data.selTokenSet = 0
        }
        this.selTokensOfSet()
      })
    },
    'eintraege.data.selTokenSet' (nVal) {
      if (nVal > 0 && this.autoSelect) {
        this.$nextTick(() => {
          this.selTokensOfSet()
        })
      }
    }
  },
  components: {
    TokenSetEdit
  }
}
</script>

<style scoped>
.annosent-auswahl {
  position: relative;
}
.satzview {
  position: relative;
  padding: 0;
  margin: 10px 0px;
  border-top: 1px solid #ddd;
  border-bottom: 1px solid #ddd;
}
.satzview > div {
  padding: 10px 50px;
}
.satzview.closed > div {
  overflow-y: auto;
  max-height: 104px;
}
.satzview > button {
  position: absolute;
  top: -8px;
  left: 10px;
  background: #ddd;
  border: none;
  border-radius: 100%;
  width: 15px;
  height: 15px;
  font-size: 10px;
  padding: 0;
}
.s-tok {
  color: #888;
}
.s-tok-act {
  font-weight: bold;
  color: #333;
}
.loading {
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  padding-top: 30px;
}
</style>

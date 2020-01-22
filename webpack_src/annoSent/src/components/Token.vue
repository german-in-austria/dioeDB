<template>
  <button
    :class="'token token-type-' +
            (token.token_type_id_id + (token.fragment_of_id || token.token_type_id_id === 2 ? '' : ' space')) +
            (tokenIsFragment ? ' isfragment' : '') +
            (nextTokenIsFragment ? ' hasfragment' : '') +
            (activeTokenSet ? ' mark-active-tokenset' : '') +
            (inSelTokenSet ? ' mark-active-seltokenset' : '') +
            (selected ? ' selected' : '')"
    @mouseenter="fxData.hoverToken = token" @mouseleave="fxData.hoverToken = null"
    @click="filterfelder.bearbeitungsmodus === 'auswahl' ? $emit('selectToken') : $emit('tokenEdit')"
  >
    <div :class="'mark-tokenset' + (token.tokensets && token.tokensets.length > 0 ? ' has-antwort' : '') + (token.antworten && token.antworten.length > 0 ? ' sib-antwort' : '')" />
    <div :class="'mark-token' + (token.antworten && token.antworten.length > 0 ? ' has-antwort' : '') + (token.tokensets && token.tokensets.length > 0 ? ' sib-antwort' : '')" />
    <span class="space" v-if="!this.token.fragment_of_id && this.token.token_type_id_id !== 2">&nbsp;</span>{{ tokenText }}</button>
</template>

<script>
export default {
  name: 'Token',
  props: ['token', 'tokens', 'eintrag', 'eintraege', 'filterfelder', 'fxData'],
  computed: {
    selected () {
      return this.filterfelder.bearbeitungsmodus === 'auswahl' && this.eintrag.selected && this.eintrag.selected.indexOf(this.token.id) > -1
    },
    nextToken () {
      let isAToken = false
      let nToken = null
      this.tokens.some((aToken) => {
        if (aToken.id === this.token.id) {
          isAToken = true
        } else if (isAToken) {
          nToken = aToken
          return true
        }
      }, this)
      return nToken
    },
    nextTokenIsFragment () {
      return this.nextToken ? this.nextToken.fragment_of_id : null
    },
    tokenIsFragment () {
      return this.token.fragment_of_id
    },
    tokenText () {
      let aTokenText = (this.token.ortho === null ? (!this.token.text_in_ortho ? this.token.text : this.token.text_in_ortho) : this.token.ortho)
      if (this.nextToken && this.nextTokenIsFragment) {
        let foTokenText = (this.nextToken.ortho === null ? (!this.nextToken.text_in_ortho ? this.nextToken.text : this.nextToken.text_in_ortho) : this.nextToken.ortho)
        if (aTokenText.substr(aTokenText.length - foTokenText.length) === foTokenText) {
          aTokenText = aTokenText.substr(0, aTokenText.length - foTokenText.length)
        }
      }
      return aTokenText
    },
    activeTokenSet () {
      let found = false
      if (this.fxData.hoverToken && this.fxData.hoverToken.tokensets) {
        this.fxData.hoverToken.tokensets.some((aTokenset) => {
          if (aTokenset.tokentoset) {
            aTokenset.tokentoset.some((aToken) => {
              if (aToken.id_token_id === this.token.id) {
                found = true
                return true
              }
            }, this)
          }
          return found
        }, this)
      }
      return found
    },
    inSelTokenSet () {
      let found = false
      if (this.eintraege.data.tokenSets[this.eintraege.data.selTokenSet]) {
        if (this.eintraege.data.tokenSets[this.eintraege.data.selTokenSet].tokentoset) {
          this.eintraege.data.tokenSets[this.eintraege.data.selTokenSet].tokentoset.some((aToken) => {
            if (aToken.id_token_id === this.token.id) {
              found = true
              return true
            }
          }, this)
        }
      }
      return found
    }
  },
  mounted () {
  },
  methods: {
  }
}
</script>

<style scoped>
.token {
  position: relative;
  padding: 3px 1px;
  background-color: #fafafa;
  border: 1px solid #fafafa;
  border-radius: 4px;
  margin: -4px 0;
  margin-right: 1px;
}
.token.space {
  margin-left: 5px;
}
.token > span.space {
  font-size: 0;
}
.token.isfragment {
  border-left: none;
  border-top-left-radius: 0;
  border-bottom-left-radius: 0;
}
.token.hasfragment {
  border-right: none;
  border-top-right-radius: 0;
  border-bottom-right-radius: 0;
}
.token:hover, .token:focus {
  background-color: #eef;
  border-color: #ddf;
  outline: none;
}
.token.mark-active-tokenset {
  border-color: #337ab7;
  background-color: #eef7ff;
}
.token.mark-active-seltokenset {
  border-color: #c23636;
}
.token.mark-active-seltokenset.mark-active-tokenset {
  border-color: #8e3dbd;
}
.token.selected.mark-active-seltokenset {
  border-color: #5cb85c;
}
.token.selected:after, .token:hover:after, .token:focus:after {
  content: '';
  position: absolute;
  left: -3px;
  top: -3px;
  right: -3px;
  bottom: -3px;
  background: #337ab7;
  z-index: -1;
  border-radius: 5px;
}
.token.selected.mark-active-seltokenset:after {
  background: #5cb85c;
}
.token:hover:after, .token:focus:after {
  background: #8e3dbd;
}
/* .token.selected:hover:after, .token.selected:focus:after {
  background: #33aeb7;
} */
.mark-tokenset, .mark-token {
  background-color: #337ab7;
  position: absolute;
  bottom: 2px;
  height: 2px;
  left: 1px;
  width: 50%;
  width: calc(50% - 1px);
  opacity: 0;
}
.mark-token {
  background-color: #5cb85c;
  left: inherit;
  right: 1px;
}
.mark-token.sib-antwort, .mark-tokenset.sib-antwort {
  opacity: 0.25;
}
.mark-tokenset.has-antwort, .mark-token.has-antwort {
  opacity: 1;
}

</style>

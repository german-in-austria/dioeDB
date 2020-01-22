<template>
  <div class="annosent-suchen row">
    <div class="col col-md-12">
      <div class="form-horizontal">
        <div class="form-group" v-for="suchfeld in suchfelder" :key="'sl-' + suchfeld.name">
          <label :for="'suche-' + suchfeld.name" class="col-sm-2 control-label">{{ suchfeld.name }}</label>
          <div class="col-sm-10">
            <div class="input-group igfx">
              <div>
                <input type="text" v-model="suchfeld.value" class="form-control" :id="'suche-' + suchfeld.name" style="border-radius:4px 0 0 4px;" :placeholder="valPlaceholder(suchfeld.methode)">
              </div>
              <div style="width:80px;">
                <select class="form-control" v-model="suchfeld.kannmuss" :id="'kannmuss-' + suchfeld.name">
                  <option value="kann">kann</option>
                  <option value="muss">muß</option>
                  <option value="nicht">nicht</option>
                </select>
              </div>
              <div style="width:149px;">
                <select class="form-control" v-model="suchfeld.methode" :id="'methode-' + suchfeld.name" style="border-radius:0 4px 4px 0;">
                  <option value="ci">case-insensetive</option>
                  <option value="cs">case-sensetive</option>
                  <option value="iregex">iRegEx</option>
                  <option value="regex">RegEx</option>
                </select>
              </div>
            </div>
          </div>
        </div>
        <div class="form-group">
          <div class="col-md-12">
            <button class="btn btn-primary float-right" type="button" @click="$emit('suche')" style="width:224px;">Suchen</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Suchen',
  props: ['suchfelder'],
  mounted () {
    console.log(this.suchfelder)
  },
  methods: {
    valPlaceholder (methode) {    // Placeholder für Suchfeld entsprechend der ausgewählten Methode anpassen
      let aPH = 'hat'
      if (methode === 'regex' || methode === 'iregex') {
        aPH = '\\yh(a|ä)tte\\y'
      }
      return 'z.B. "' + aPH + '"'
    }
  }
}
</script>

<style scoped>
.igfx {
  width: 100%;
}
.igfx > * {
  display: table-cell;
  width: auto;
}
</style>

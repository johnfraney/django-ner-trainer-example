Vue.component('phrase-container', {
  props: {
    entities: {
      type: Array,
      required: true
    },
    phrase: {
      type: Object,
      required: true
    },
    phraseEntities: {
      type: Array
    }
  },
  methods: {
    wrapPhraseEntityRange (phraseEntity) {
      // Create a new range if wrapping a phrase outside of a selection
      let range = document.createRange()
      // The phrase's text is the firstChild of #phrase
      let elem = this.$refs.phrase
      range.setStart(elem.firstChild, phraseEntity.start_index)
      range.setEnd(elem.firstChild, phraseEntity.end_index)
      let entityAbbr = document.createElement('abbr')
      let entityName = ''
      for (let e of this.entities) {
        if (e.label === phraseEntity.entity) {
          entityName = e.name
          break
        }
      }
      entityAbbr.title = entityName
      range.surroundContents(entityAbbr)
    },

    wrapPhraseEntities () {
      this.$nextTick(() => {
        if (this.phraseEntities.length > 0 && this.phrase.text.length > 0) {
          let phraseEntitiesCopy = [...this.phraseEntities]
          let reversedPhraseEntities = phraseEntitiesCopy.sort((a, b) => {
            return b.start_index - a.start_index
          })
          for (let entity of reversedPhraseEntities) {
            this.wrapPhraseEntityRange(entity)
          }
        }
      })
    }
  },

  watch: {
    phraseEntities (phraseEntities) {
      this.$refs.phrase.innerHTML = this.phrase.text
      this.wrapPhraseEntities()
    }
  },
  template: `<p ref="phrase">{{ phrase.text }}</p>`,
})

<template lang="html">
  <div class="">
    <p> {{ message }} </p>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Home',
  data () {
    return {
      message: 'Nuevo mensaje desde VUE JS'
    }
  },
  methods: {
    getMensaje () {
      const path = 'http://localhost:5000/api/mensaje'
      axios.get(path).then((respuesta) => {
        this.message = respuesta.data
      })
        .catch((error) => {
          console.error(error)
        })
    }
  },
  created () {
    this.getMensaje()
  }
}
</script>

<style lang="css" scoped>

</style>

<template>
  <div id = "imgintro">
    <img :src = "globais.TEMA" alt="erro">
  </div>
</template>

<script>
    import data from "../Data/data"

    export default {
        name: "imgintro",
        data() {
            return {
                globais: data
            }
        }
    }
</script>

<style>
    #imgintro {
        max-height: 400px;
        overflow: hidden;
    }

    #imgintro img {
        width: 100%;
    }
</style>
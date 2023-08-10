<template>
  <table id = "tablelist">
    <tr>
        <td v-for = "campo in campos" :key = "campo"> {{ campo }} </td>
    </tr>
    <tr v-for = "registro in globais[entidade]" :key = "registro.id">
        <td v-for = "campo in campos" :key = "campo"> {{ registro[campo] }} </td>
    </tr>
  </table>
</template>

<script>
    import data from "../Data/data"
    
    export default {
        name: "tablelist",
        data() {
            return {
                globais: data
            }
        },
        props: {
            entidade: {
                required: true,
                type: String
            },
            campo: {
                required: true,
                type: String
            }
        },
        mounted() {
            console.log(this.globais[this.entidade])
        }
    }
</script>

<style>
  #tablelist {
    width: 100%;
  }

  #tablelist tr {
    background: #888;
  }

  #tablelist tr:nth-child(odd) {
    background: #555;
  }

  #tablelist tr td {
    text-align: center;
  }
</style>
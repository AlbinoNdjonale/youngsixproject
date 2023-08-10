<template>
   <div id="singles">
    <Header/>

    <Reprodutor  all = "Single" msg = "devirtate com as nossas singles"/>
      
   </div>
</template>

<script>
    import data from "../Data/data"

    // Importando Bases
    import Header from "../Base/header";
    import Reprodutor from "../Base/reprodutor";

    export default {
        name: "singles",
        data() {
            return {
                globais: data
            }
        },
        components: {
            Header,
            Reprodutor
        },
        created() {
            this.globais.alterTitle("Singles")
        }
    }
</script>
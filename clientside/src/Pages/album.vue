<template>
    <div id="album">
     <Header/>

     <Reprodutor  :all = "`Album - ${album}`" :msg = "`devirta-se com o album ${album}`" :album = "album"/>
       
    </div>
 </template>
 
 <script>
     import data from "../Data/data"

     // Importando Bases
     import Header from "../Base/header";
     import Reprodutor from "../Base/reprodutor";
 
     export default {
         name: "album",
         data() {
            return {
                globais: data
            }
         },
         props: {
            album: {
                required: true,
                type: String
            }
         },
         components: {
             Header,
             Reprodutor
         },
         created() {
             this.globais.alterTitle("Album")
         }
     }
 </script>
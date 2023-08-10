<template>
    <div id="ep">
     <Header/>

     <Reprodutor  :all = "`Ep - ${ep}`" :msg = "`devirta-se com a ep ${ep}`" :ep = "ep"/>
       
    </div>
 </template>
 
 <script>
     import data from "../Data/data"

     // Importando Bases
     import Header from "../Base/header";
     import Reprodutor from "../Base/reprodutor";
 
     export default {
         name: "ep",
         data() {
            return {
                globais: data
            }
         },
         props: {
            ep: {
                required: true,
                type: String
            }
         },
         components: {
             Header,
             Reprodutor
         },
         created() {
             this.globais.alterTitle("Ep")
         }
     }
 </script>
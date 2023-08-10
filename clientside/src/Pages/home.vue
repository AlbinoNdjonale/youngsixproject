<template>
  <div id = "home">
    <Header/>

    <main id = "main">
        <ImgIntro/>
        
        <div class = "space">
            <section id = "welcome">
                <article>
                    <h2> Sejá bem vindo </h2>
                    ao blog da {{ globais.infoOfGroup.nome }}, aqui
                    você vera tudo que o grupo tem de novo,
                    como singles, ep's, albums e eventos. Vejá a baixo uma lista das coisas que tu podes
                    acessar.
                </article>
            </section>

            <nav id = "preview">
                <router-link to = "/singles">Singles</router-link>
                <router-link to = "/eps">Ep's</router-link>
                <router-link to = "/albums">Albums</router-link>
                <router-link to = "/eventus">Eventus</router-link>
                <router-link to = "/fotos">Fotos</router-link>
            </nav>
        </div>
    </main>
  </div>
</template>

<script>
    import data from "../Data/data"

    // Importando Bases
    import Header from "../Base/header";
    import ImgIntro from '../Base/imgintro';

    export default {
        name: "home",
        data() {
            return {
                globais: data
            }
        },
        components: {
            Header,
            ImgIntro
        },
        created() {
            this.globais.alterTitle("Pagina Inicial")
        }
    }
</script>

<style>
    
</style>
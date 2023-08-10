<template>
  <div id="ip">
    <Header/>

    <main id = "main">
        <ImgIntro/>

        <div class="space">
            <section id="welcome">
                <article>
                    <h2> Ep's </h2>
                    devirta-se com as nossas ep's
                </article>
            </section>

            <nav id = "preview">
                <router-link v-for="ep in globais.eps" :key = "ep.id" :to = "`ep/${ep.nome}`">
                    {{ ep.nome }}
                </router-link>
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
        name: "ep",
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
            this.globais.alterTitle("Ep's")
        }
    }
</script>
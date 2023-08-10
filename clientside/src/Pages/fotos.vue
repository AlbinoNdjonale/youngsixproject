<template>
  <div id="fotos">
    <Header/>

    <main id = "main">
        <ImgIntro/>

        <div class="space">

            <section id = "welcome">
                <article>
                    <h2> Fotos </h2>
                    Maravilha-se com as nossas fotos.
                </article>
            </section>

            <section id = "imgs">
                <div v-for = "foto in globais.fotos" :key = "foto.id" class="img">
                    <header> {{ foto.titulo }} </header>
                    <main>
                        <img :src = "foto.path" alt="">
                    </main>
                    <footer> <small> Publicado aos {{ foto.data }} </small> </footer>
                </div>
            </section>
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
        name: "fotos",
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
            this.globais.alterTitle("Fotos")
        }
    }
</script>

<style>
   #imgs {
    display: flex;
    flex-wrap: wrap;
    align-items: baseline;
   }

   #imgs .img header, #imgs .img footer {
    background: #333;
    color: #eee;
    padding: 5px;
   }

   #imgs .img {
    flex: 1;
    text-align: center;
    min-width: 200px;
    max-width: 500px;
    border-radius: 0.7rem;
    background: #fff;
    margin: 5px;
    transition: 1s;
    cursor: pointer;
    overflow: hidden;
   }

   #imgs .img img {
    max-width: 100%;
    max-height: 300px;
   }
</style>
<template>
    <div id="ip">
      <Header/>
  
      <main id = "main">
          <ImgIntro/>
  
          <div class="space">
              <section id="welcome">
                  <article>
                      <h2> Albums </h2>
                      devirta-se com os nossos albums
                  </article>
              </section>
  
              <nav id = "preview">
                  <router-link v-for="album in globais.albums" :key = "album" :to = "`album/${album.nome}`">
                      {{ album.nome }}
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
              this.globais.alterTitle("Albums")
          }
      }
  </script>
<template>
    <div id="membros">
      <Header/>
  
      <main id = "main">
          <ImgIntro/>
  
          <div class="space">
  
              <section id = "welcome">
                  <article>
                      <h2> Membros </h2>
                      Vejá todos os membros do grupo {{ globais.infoOfGroup.nome }}.
                  </article>
              </section>
  
              <section id = "imgs">
                  <div v-for = "usuario in globais.usuarios" :key = "usuario.id" class="img">
                      <header> {{ usuario.nome }} </header>
                      <main>
                          <img :src = "usuario.capa" alt="">
                      </main>
                      <footer> <small> Contacto {{ usuario.contacto }} </small> </footer>
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
          name: "membros",
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
              this.globais.alterTitle("Membros")
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
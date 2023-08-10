<template>
    <header id = "heade">
        <div id = "extern">
          <h1> {{ globais.infoOfGroup.nome }} </h1>

          <nav id = "menu">
            <router-link to = "/">Home</router-link>
            <router-link to = "/singles">Singles</router-link>
            <router-link to = "/eps">Ep's</router-link>
            <router-link to = "/albums">Albums</router-link>
            <router-link to = "/eventus">Eventus</router-link>
            <router-link to = "/fotos">Fotos</router-link>
            <router-link to = "/membros">Membros</router-link>
          </nav>

          <img id = "contextmenu" src="../img/menu.png" @click = "extendmenu">
        </div>
        <nav id = "menu1" :style="{display: displayextend}">
          <router-link to = "/">Home</router-link>
          <router-link to = "/singles">Singles</router-link>
          <router-link to = "/eps">Ep's</router-link>
          <router-link to = "/albums">Albums</router-link>
          <router-link to = "/eventus">Eventus</router-link>
          <router-link to = "/fotos">Fotos</router-link>
          <router-link to = "/membros">Membros</router-link>
        </nav>
    </header>
</template>

<script>
    import data from "../Data/data"

    export default {
        name: "heade",
        data() {
            return {
                globais: data,
                displayextend: 'none'
            }
        },
        methods: {
          extendmenu() {
            this.displayextend = this.displayextend == "none" ? "grid" : "none"
          }
        }
    }
</script>

<style>
  #heade {
    background: #333;
    position: fixed;
    width: 100%;
    z-index: 10;
  }

  #extern {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 5px;
  }

  #heade h1 {
    color: #eee;
    padding: 3px 15px;
  }

  #menu {
    width: 45%;
    display: flex;
    justify-content: space-between;
    text-align: center;
  }

  #menu1 {
    text-align: center;
  }

  #menu a, #menu1 a {
    color: #eee;
    width: 100%;
    border-radius: 0.3rem;
    padding: 5px;
  }

  #menu a:hover, #menu1 a:hover {
    color: #333;
    background: #eee;
    transition: 1s;
  }

  #menu1 a {
    border-radius: 0;
    padding: 5px;
    text-decoration: none;
  }

  #contextmenu {
    width: 40px;
    cursor: pointer;
    display: none;
  }

  @media screen and (max-width: 730px) {
      #menu {
        display: none;
      }

      #contextmenu {
        display: block;
      }
  }
</style>
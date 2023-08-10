<template>
    <h1 v-if = "processando"> Processando </h1>
    <router-view v-else/>
</template>

<script>
    import Vue from "vue"
    import VueRouter from "vue-router"
    import axios from "./DataBack/config"
    import { Component } from "vue"
    import data from "./Data/data"

    // Importando Paginas
    import Home from "./Pages/home"
    import Singles from "./Pages/singles"
    import Eps from "./Pages/eps"
    import Ep from "./Pages/ep"
    import Albums from "./Pages/albums"
    import Album from "./Pages/album"
    import Eventus from "./Pages/eventus"
    import Fotos from "./Pages/fotos"
    import Membros from "./Pages/membros"
    import Admin from "./Pages/admin"
    import Login from "./Pages/login"
    import Edit from "./Pages/edit"

    const admin = {
      render(h) {
        return h("div")
      },
      created() {
        if (data.usuario) {
          let page = localStorage.getItem("lastPageAdmin")
          if (page) this.$router.replace(page)
          else this.$router.replace("/admin/musicas/nome")
        } else this.$router.replace("/login")
      }
    }

    const router = new VueRouter({
        mode: "history",
        routes: [
            {path: "/", component: Home},
            {path: "/singles", component: Singles},
            {path: "/eps", component: Eps},
            {path: "/ep/:ep", component: Ep, props: true},
            {path: "/albums", component: Albums},
            {path: "/album/:album", component: Album, props: true},
            {path: "/eventus", component: Eventus},
            {path: "/fotos", component: Fotos},
            {path: "/membros", component: Membros},
            {path: "/admin", component: admin},
            {path: "/admin/:aba/:campo", component: Admin, props: true, children: [
              {path: ":id", component: Edit, props: true}
            ]},
            {path: "/login", component: Login}
        ]
    })

    Vue.use(VueRouter)

    export default {
        name: "rotas",
        data() {
          return {
            processando: true
          }
        },
        router,
        created() {
            let usuario = localStorage.getItem("user")
            if (usuario) {
              usuario = JSON.parse(usuario)
              axios
                .post("api/login", usuario)
                .then(res => {
                  if (res.data) {
                    data.usuario = res.data.usuario
                    data.authorization = res.data.authorization
                    this.processando = false
                  } else {
                    localStorage.removeItem("user")
                    this.processando = false
                  }
                })
            } else {
              this.processando = false
            }

            axios
              .get("api/getpath/TEMA.jpg")
              .then(res => {
                data.TEMA = res.data.path
              })

            axios
              .get("api/getcomentarios")
              .then(res => {
                data.comentarios = res.data
              })

            axios
              .get("api/info")
              .then(res => { data.infoOfGroup = res.data })

            axios
              .get("api/getmusics")
              .then(res => {
                data.musicas = res.data
              })

            axios
              .get("api/getgroup/eps")
              .then(res => {
                data.eps = res.data
              })

            axios
            .get("api/getgroup/albums")
              .then(res => {
                data.albums = res.data
              })

            axios
              .get("api/geteventus")
              .then(res => {
                data.eventus = res.data
              })

            axios
              .get("api/getimgs")
              .then(res => {
                data.fotos = res.data
              })

            axios
              .get("api/getusuarios")
              .then(res => {
                data.usuarios = res.data
              })
        }
    }
</script>

<style>
  * {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-weight: 300;
    margin: 0;
    padding: 0;
  }

  body {
    background: #eee;
  }

  #main {
    position: relative;
    top: 50px;
  }

  .space {
    padding: 5px;
  }

  #welcome, #preview {
    background: #fff;
    max-width: 700px;
    margin: 7px auto;
    padding: 10px;
    border-radius: 0.7rem;
  }

  #welcome article {
    max-width: 330px;
  }

  #preview {
        background: #333;
        display: flex;
        flex-direction: column;
        padding: 5px;
        border-radius: 0.7rem;
    }

    #preview a {
        color: #eee;
        text-decoration: none;
        padding: 5px;
    }

    #preview a:hover {
        text-decoration: underline;
        background: #555;
        border-radius: 0.7rem;
    }
</style>
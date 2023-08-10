<template>
    <div id="admin">
        <Header/>

        <main id = "main">
            <div class = "space">

                <section id = "info">
                    <h3>
                        {{ globais.usuario.nome }}
                    </h3>

                    <div :style = "{padding: '4px', textAlign: 'center'}">
                        <h2 @click = "openSelectFile" :style = "{cursor: 'pointer'}"> TEMA </h2>
                        <input @change = "selectFile" type="file" id = "TEMA" :style = "{display: 'none'}">
                        <button @click = "alterTema" v-if = "file" :style = "{padding: '4px', cursor: 'pointer'}">
                            ALTERAR TEMA
                        </button>
                    </div>
                </section>

                <section id = "context">
                    <header>
                        <router-link to = "/admin/musicas/nome" id = "musicas"> Musicas </router-link>
                        <router-link to = "/admin/eps/nome" id = "eps"> Ep </router-link>
                        <router-link to = "/admin/albums/nome" id = "albums"> Albums </router-link>
                        <router-link to = "/admin/eventus/titulo" id = "eventus"> Eventus </router-link>
                        <router-link to = "/admin/fotos/titulo" id = "fotos"> Imagems </router-link>
                        <router-link to = "/admin/usuarios/nome" id = "usuarios"> Usuários </router-link>
                    </header>

                    <main>
                        <section>
                           <h2> {{ aba.toUpperCase() }} </h2>
                        </section>

                        <div v-if = "campo != 'edit' && campo != 'insert'">
                            <section id = "add">
                                <router-link :to = "`/admin/${aba}/insert`">
                                    <button>
                                        INSERIR
                                    </button>
                                </router-link>
                            </section>
                            <nav>
                                <router-link :to = "`/admin/${aba}/edit/${registro.id}`" v-for = "registro in globais[aba]" :key = "registro.id" href = "#">
                                    {{ registro[campo] }}
                                </router-link>
                            </nav>
                        </div>

                        <div v-else-if = "campo == 'insert'">
                            <form @submit = "insert">
                                <section v-for = "attrs in entidades[aba]" :key = "attrs.campo">
                                    <label :for = "attrs.campo"> {{ attrs.campo }} </label>
                                    <input :id = "attrs.campo" v-if = "attrs.tipo == 'str'" v-model = "attrs.model">
                                    <input :id = "attrs.campo" v-if = "attrs.tipo == 'date'" v-model = "attrs.model" type = "date">
                                    <textarea :id = "attrs.campo" :style = "{maxWith: '100%'}" v-if = "attrs.tipo == 'texto'" v-model = "attrs.model">
                                    </textarea>
                                    <select :id = "attrs.campo" v-if = "attrs.tipo == 'combo'" v-model = "attrs.model">
                                        <option></option>
                                        <option v-for = "value in attrs.value" :key = "value.id" :value = "value.id">
                                            {{ value.nome }}
                                        </option>
                                    </select>
                                    <div v-if = "attrs.tipo == 'bool'">
                                        <input :id = "attrs.campo" type = "checkbox" v-model = "attrs.model">
                                    </div>
                                    <div v-if = "attrs.tipo == 'file'">
                                        <input :id = "attrs.campo" type = "file">
                                    </div>
                                </section>
                                <section>
                                    <button>
                                        INSERIR
                                    </button>
                                </section>
                            </form>
                        </div>

                        <router-view v-else />
                    </main>

                    <footer>

                    </footer>
                </section>
            </div>
        </main>
    </div>
</template>

<script>
    import axios from "../DataBack/config"
    import data from "../Data/data"

    // Importando Bases
    import Header from "../Base/header";

    export default {
        name: "admin",
        data() {
            return {
                globais: data,
                file: null,
                entidades: {
                    musicas: [
                        {campo: "nome", tipo: "file"},
                        {campo: "autores", tipo: "str", model: ""},
                        {campo: "participantes", tipo: "str", model: ""},
                        {campo: "ep", tipo: "combo", value: data.eps, model: ""},
                        {campo: "album", tipo: "combo", value: data.albums, model: ""},
                        {campo: "single", tipo: "bool", model: ""}
                    ],
                    eps: [
                        {campo: "nome", tipo: "str", model: ""}
                    ],
                    albums: [
                        {campo: "nome", tipo: "str", model: ""}
                    ],
                    eventus: [
                        {campo: "titulo", tipo: "str", model: ""},
                        {campo: "capa", tipo: "file"},
                        {campo: "conteudo", tipo: "texto", model: ""},
                        {campo: "dataevent", tipo: "date", model: ""}
                    ],
                    fotos: [
                        {campo: "path", tipo: "file"},
                        {campo: "titulo", tipo: "str", model: ""}
                    ],
                    usuarios: [
                        {campo: "nome", tipo: "str", model: ""},
                        {campo: "contacto", tipo: "str", model: ""},
                        {campo: "capa", tipo: "file"},
                        {campo: "senha", tipo: "str", model: ""}
                    ]
                },
                campos: {
                    musicas : "nome",
                    eps     : "nome",
                    albums  : "nome",
                    eventus : "titulo",
                    fotos   : "titulo",
                    usuarios: "nome"
                },
                realynames: {
                    musicas : "musicas",
                    eps     : "eps",
                    albums  : "albums",
                    eventus : "eventos",
                    fotos   : "img",
                    usuarios: "usuario"
                }
            }
        },
        props: {
            aba: {
                required: true,
                type: String
            },
            campo: {
                required: true,
                type: String
            }
        },
        components: {
            Header
        },
        methods: {
            insert(e) {
                e.preventDefault()

                let body = new FormData()
                for (let attrs of this.entidades[this.aba]) {
                    if (attrs.model == undefined) {
                        let anexo = document.getElementById(attrs.campo)
                        body.append(attrs.campo, anexo.files[0])
                    } else {
                        body.append(attrs.campo, attrs.model != "" ? attrs.model : null)
                    }
                }

                axios({
                    method : "POST",
                    url    : `/api/insert/${this.realynames[this.aba]}`,
                    headers: {
                        Authorization: this.globais.authorization
                    },
                    data   : body
                }).then(res => {
                    this.globais[this.aba].push(res.data)
                    this.$router.replace(`/admin/${this.aba}/${this.campos[this.aba]}`)
                })
            },

            openSelectFile() {
                document.getElementById("TEMA").click()
            },

            selectFile(e) {
                let selF = e.target
                this.file = selF.files[0]
            },

            alterTema() {
                let body = new FormData()
                body.append("TEMA", this.file)
                this.file = null

                axios({
                    method : "POST",
                    url    : "/api/altertema",
                    headers: {
                        Authorization: this.globais.authorization
                    },
                    data   : body
                }).then(res => {
                    this.globais.TEMA = res.data.path
                })
            }
        },
        created() {
            if (!this.globais.usuario)
                this.$router.replace("/login")
            else {
                localStorage.setItem("lastPageAdmin", this.$route.path)
                this.globais.alterTitle("Admin")
            }
        }
    }
</script>

<style>
  #info {
    background: #333;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-radius: 0.4rem;
    padding: 10px;
    margin: 10px 0;
    color: #eee;
  }

  #info h2 {
    color: #44f;
  }

  #context {
    border-radius: 0.4rem;
    overflow: hidden;
  }

  #context header {
    display: flex;
    flex-wrap: wrap;
    background: #333;
    padding: 5px;
    display: flex;
    justify-content: space-between;
  }

  #context header a {
    color: #eee;
    padding: 5px;
    cursor: pointer;
    flex: 1;
    text-align: center;
    border-radius: 0.4rem;
    font-weight: bold;
    margin: 2px;
  }

  #context header a:hover {
    color: #333;
    background: #eee;
    transition: 1s;
  }

  #context #add {
    padding: 5px;
    text-align: right;
  }

  #context #add button {
    padding: 7px;
    cursor: pointer;
    font-weight: 500;
    color: #eee;
    background: #44f;
    border: none;
    border-radius: .3rem;
  }

  #context nav {
    background: #333;
    display: grid;
  }

  #context nav a {
    padding: 5px;
    text-decoration: none;
    color: #eee;
  }

  #context nav a:hover {
    color: #333;
    background: #ccc;
    transition: 1s;
  }

  #context form {
    padding: 5px;
    background: #333;
    color: #eee;
    max-width: 600px;
    margin: auto;
  }

  #context form section {
    margin-bottom: 5px;
  }

  #context form section label {
    font-weight: bold;
  }

  #context form section {
    display: grid;
  }

  #context form section input, #context form section select {
    padding: 5px;
    outline: none;
    border: none;
    font-weight: bold;
    border-radius: 0.3rem;
  }

  #context form section button {
    color: #eee;
    padding: 4px;
    cursor: pointer;
    background: #44f;
    border-radius: 0.3rem;
    font-weight: 600;
    border: none;
  }
</style>
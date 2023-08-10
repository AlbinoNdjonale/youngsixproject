<template>
  <main id = "main">
    <section class = "space">

        <section id="welcome">
            <article>
                <h2> {{ all }} </h2>
                {{ msg }}
            </article>
        </section>

        <section id = "play">
            <header>
                <h3> {{ nomeDaMusic }} </h3>
            </header>

            <main>
                <audio controls :src = "currentMusic" id = "currentMusic">
                </audio>
            </main>

            <footer>
                <small>
                    de: {{ de }} 
                    <span v-if = "participante">ft {{ participante }}</span>
                </small>

                <small :style = "{ marginLeft: '20px' }">
                    views: {{ views }}
                </small>
            </footer>
        </section>
    </section>

    <section class = "space">
            <nav id = "listMusic">
                <div
                  class = "ItemMusic"
                  v-for = "musica in globais.musicas"
                  v-if = "(ep == null && album == null && musica.single == 1) ||
                    (musica.album == null && musica.ep != null && musica.ep.nome == ep) ||
                    (musica.album != null && musica.ep == null && musica.album.nome == album)"
                  :key = "musica.id">

                    <div :style = "{background: '#777'}">
                        <div
                          class = "musica"
                          @click = "Play(musica)"
                          :id = "musica.id">
                            <div>
                                <span>{{ musica.nome }}</span>
                                <section>
                                    <small :style = "{ marginLeft: '10px' }">Views: {{ musica.views }}</small>
                                </section>
                            </div>
                            <div>
                                <small>
                                    <em>
                                        De: {{ FormatNomes(musica.autores) }}
                                        <span v-if = "musica.participantes">ft {{ FormatNomes(musica.participantes) }}</span>
                                    </em>
                                </small>
                                <small :style = "{ marginLeft: '10px' }">
                                    {{  FormatData(musica.data) }}
                                </small>
                            </div>
                        </div>
                        <div class = "contcoment">
                            <img @click = "displaycoment(musica.id)" :src = "img.comentImg" alt = "erro">
                        </div>
                    </div>

                    <section
                      class = "comentarea"
                      :id = "`comenta${musica.id}`">
                        <div :style = "{padding: '5px'}">
                            <div v-for = "comentario in globais.comentarios" :key = "comentario.id">
                                <article v-if = "comentario.entidadename == 'musicas' && comentario.entidadeid == musica.id">
                                    <div class = "cont">{{ comentario.conteudo }}</div>
                                    <small>
                                        <em>
                                            {{ comentario.data }}
                                        </em>
                                    </small>
                                </article>
                            </div>
                        </div>
                        <form @submit = "e => comentar(e, musica.id)">
                            <textarea placeholder = "escreva um comentário" rows="1" :id = "`area${musica.id}`"></textarea>
                            <button>
                                COMENTAR
                            </button>
                        </form>
                    </section>

                </div>
            </nav>
    </section>
  </main>
</template>

<script>
    import axios from "../DataBack/config"
    import data from "../Data/data"

    import comentImg from "../img/comentar.png"

    export default {
        name: "reprodutor",
        data() {
            return {
                globais: data,
                currentMusic: "",
                nomeDaMusic: "****",
                de: "****",
                participante: null,
                views: 0,
                img: {
                    comentImg
                }
            }
        },
        props: {
            all: {
                required: true,
                type: String
            },
            msg: {
                required: true,
                type: String
            },
            ep: {
                required: false,
                type: String
            },
            album: {
                required: false,
                type: String
            }
        },
        methods: {
            FormatNomes(nomes) {
                return nomes.split(",").map(item => {
                    return item.trim()
                }).join(" & ")

            },
            FormatData(data) {
                return data.split("-").reverse().join("/")
            },
            FormatPath(musica) {
                return musica.replaceAll(" ", "_")+".mp3"
            },

            Visualizar(musica) {
                axios.post(`api/visualizar/${musica.id}`)
                .then(res => {
                    musica.views = res.data
                    this.views   = res.data
                })
            },

            Play(musica) {
                axios
                  .get(`api/getpath/${this.FormatPath(musica.nome)}`)
                  .then(res => {
                    this.currentMusic = res.data.path
                    this.nomeDaMusic = musica.nome
                    this.de = this.FormatNomes(musica.autores)
                    this.views = musica.views
                    if (musica.participantes) {
                        this.participante = this.FormatNomes(musica.participantes)
                    } else {
                        this.participante = null
                    }
                  }).then(() => {
                    let lsmusic = document.getElementsByClassName("musica")
                    for (let music of lsmusic) {
                        music.style.background = "#fff"
                        music.style.color = "#000"
                    }
                    document.getElementById(musica.id).style.background = "#555"
                    document.getElementById(musica.id).style.color = "#eee"
                    let currentMusic = document.getElementById("currentMusic")
                    currentMusic.addEventListener("ended", () => this.Visualizar(musica))
                    currentMusic.play()
                  })
            },

            comentar(e, id) {
                e.preventDefault()
                let conteudo = document.getElementById(`area${id}`)
                  .value
                
                if (conteudo.trim() != "") {
                    axios.post(`api/comentar/musicas/${id}`, { conteudo })
                        .then(res => {
                            document.getElementById(`area${id}`).value = ""
                            this.globais.comentarios.push(res.data)
                        })
                }
            },

            displaycoment(id) {
                let el = document.getElementById(`comenta${id}`)

                el.style.display = el.style.display == "block"?"none":"block"
            },
        }
    }
</script>

<style>
    #play {
        background: #fff;
        border-radius: 0.7rem;
        max-width: 450px;
        margin: auto;
        box-shadow: 1px 1px 2px 2px #333;
    }

    #play header {
        padding: 4px;
        text-align: center;
    }

    #play main {
        display: flex;
        justify-content: center;
        border-top: 1px solid #333;
        border-bottom: 1px solid #333;
    }

    #play main audio {
        width: 100%;
        height: 23px;
    }

    #play footer {
        padding: 4px;
        display: flex;
        justify-content: space-between;
    }

    #listMusic {
        background: #333;
        padding: 5px;
        border-radius: 0.7rem;
        height: 40vh;
        overflow: auto;
        max-width: 700px;
        margin: auto;
    }

    .musica {
        background: #fff;
        padding: 4px;
        border-radius: 0.6rem;
        cursor: pointer;
    }

    .musica div {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    #listMusic .comentarea {
       max-height: 146px;
       background: #777;
       text-align: center;
       display: none;
       overflow: auto;
    }

    #listMusic .comentarea article {
      background: #fff;
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      margin-bottom: 4px;
      border-radius: 0.4rem;
      padding: 4px;
    }

    #listMusic .comentarea article .cont {
      word-break: break-all;
    }

    #listMusic .comentarea form {
      background: #aaa;
      position: sticky;
      padding: 4px;
      bottom: 0;
      justify-content: space-between;
      display: flex;
      align-items: baseline;
    }

    #listMusic .comentarea form textarea {
      min-width: 50%;
      max-width: 85%;
      border: none;
      outline: none;
      background: transparent;
    }

    #listMusic .comentarea form button {
      padding: 4px;
      cursor: pointer;
      border: none;
      border-radius: 1rem;
      background: #44f;
      color: #eee;
    }

    #listMusic .ItemMusic {
        border-radius: 0.6rem;
        margin: 4px;
        overflow: hidden;
    }

    .contcoment {
        text-align: right;
        padding: 3px;
    }

    .contcoment img {
        width: 25px;
        cursor: pointer;
        padding: 3px;
        border-radius: 50%;
    }

    .contcoment img:hover {
        background: #fff;
        transition: 1s;
    }
</style>
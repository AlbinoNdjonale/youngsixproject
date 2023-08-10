<template>
    <div id="eventus">

        <Header/>

        <main id = "main">
            <ImgIntro/>

            <div class="space">
                <section id = "welcome">
                    <article>
                        <h2> Eventus </h2>
                        veja aqui todos os nossos eventus.
                    </article>
                </section>

                <div v-for = "eventu in globais.eventus" :key = "eventu.id" class = "eventu">
                    <header>
                        <h3> {{ eventu.titulo }} </h3>
                        <small> Pulicado aos: {{ eventu.datapub }} </small>
                    </header>
                    <main>
                        <div v-if = "eventu.capa != null" class = "img">
                            <img :src="eventu.capa" alt="">
                        </div>
                        {{ eventu.conteudo }}
                    </main>
                    <div :style = "{background: '#777'}">
                        <footer>
                            <span>Data do Eventu: {{ eventu.dataevent }}</span>
                            <span>
                                <img @click = "displaycoment(eventu.id)" :src = "img.comentImg" alt = "erro">
                            </span>
                        </footer>
                    </div>
                    <section class = "comentarea" :id = "`comenta${eventu.id}`">
                        <div :style = "{padding: '5px'}">
                            <div v-for = "comentario in globais.comentarios" :key = "comentario.id">
                                <article v-if = "comentario.entidadename == 'eventos' && comentario.entidadeid == eventu.id">
                                    <div class = "cont">{{ comentario.conteudo }}</div>
                                    <small>
                                        <em>
                                            {{ comentario.data }}
                                        </em>
                                    </small>
                                </article>
                            </div>
                        </div>
                        <form @submit = "e => comentar(e, eventu.id)">
                            <textarea placeholder = "escreva um comentário" rows="1" :id = "`area${eventu.id}`"></textarea>
                            <button>
                                COMENTAR
                            </button>
                        </form>
                    </section>
                </div>

            </div>

        </main>

    </div>
</template>

<script>
    import data from "../Data/data"
    import axios from "../DataBack/config";

    // Importando Bases
    import Header from "../Base/header";
    import ImgIntro from '../Base/imgintro';

    import comentImg from "../img/comentar.png"

    export default {
        name: "eventus",
        data() {
            return {
                globais: data,
                img: {
                    comentImg
                }
            }
        },
        components: {
            Header,
            ImgIntro
        },
        methods: {
            displaycoment(id) {
                let el = document.getElementById(`comenta${id}`)

                el.style.display = el.style.display == "block"?"none":"block"
            },

            comentar(e, id) {
                e.preventDefault()
                let conteudo = document.getElementById(`area${id}`)
                  .value
                
                if (conteudo.trim() != "") {
                    axios.post(`api/comentar/eventos/${id}`, { conteudo })
                        .then(res => {
                            document.getElementById(`area${id}`).value = ""
                            this.globais.comentarios.push(res.data)
                        })
                }
            }
        },
        created() {
            this.globais.alterTitle("Eventus")
         }
    }
</script>

<style>
  .eventu {
    background: #fff;
    border-radius: 0.7rem;
    overflow: hidden;
    margin: auto;
    margin-bottom: 5px;
    max-width: 700px;
  }

  .eventu header, .eventu footer {
    background: #333;
    color: #eee;
    padding: 5px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .eventu footer {
    border-radius: 0 0 0.7rem 0.7rem;
  }

  .eventu footer img {
    width: 23px;
    cursor: pointer;
    padding: 3px;
    border-radius: 50%;
  }

  .eventu footer img:hover {
    background: #eee;
    transition: 1s;
  }

  .eventu main {
    padding: 5px;
    text-align: center;
  }

  .eventu div.img {
    max-height: 200px;
    overflow: hidden;
  }

  .eventu img {
    max-height: 100%;
  }

  #eventus .comentarea {
    max-height: 146px;
    background: #777;
    text-align: center;
    display: none;
    overflow: auto;
  }

  #eventus .comentarea article {
    background: #fff;
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 4px;
    border-radius: 0.4rem;
    padding: 4px;
  }

  #eventus .comentarea article .cont {
    word-break: break-all;
  }

  #eventus .comentarea form {
    background: #aaa;
    position: sticky;
    padding: 4px;
    bottom: 0;
    justify-content: space-between;
    display: flex;
    align-items: baseline;
  }

  #eventus .comentarea form textarea {
    min-width: 50%;
    max-width: 85%;
    border: none;
    outline: none;
    background: transparent;
  }

  #eventus .comentarea form button {
    padding: 4px;
    cursor: pointer;
    border: none;
    border-radius: 1rem;
    background: #44f;
    color: #eee;
  }
</style>
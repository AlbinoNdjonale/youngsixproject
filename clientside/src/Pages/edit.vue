<template>
    <div id = "edit">
        <form @submit = "update">
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
                    <div>
                        <small>
                            <em>
                                Valor atual:
                                <a :href = "isURL(entidade[attrs.campo])?entidade[attrs.campo]:`${DOMINIO}/api/getpath/${entidade[attrs.campo]}`">
                                    {{ entidade[attrs.campo] }}
                                </a> 
                            </em>
                        </small>
                    </div>
                </div>
            </section>
            <section>
                <button>
                    SALVAR
                </button>
            </section>
        </form>
        <section id = "del">
            <button @click = "Delete">
                DELETAR
            </button>
        </section>
    </div>
</template>

<script>
    import axios from "../DataBack/config"
    import data from "../Data/data"

    export default {
        name: "edit",
        data() {
            return {
                globais: data,
                DOMINIO: "localhost:5000",
                entidade: {},
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
            id: {
                required: true,
                type: String
            },
            aba: {
                required: true,
                type: String
            }
        },
        methods: {
            isURL(url) {
                const urlPattern = /^(https?:\/\/)?([\w.-]+\.[a-z]{2,})(\/[\w-.\/?%&=]*)?$/i
                return urlPattern.test(url);
            },

            update(e) {
                e.preventDefault()

                let body = new FormData()
                for (let attrs of this.entidades[this.aba]) {
                    if (attrs.model == undefined) {
                        let anexo = document.getElementById(attrs.campo)
                        console.log(attrs.campo)
                        if (anexo.files[0] == undefined) {
                            body.append(attrs.campo, this.entidade[attrs.campo])
                        } else {
                            body.append(attrs.campo, anexo.files[0])
                        }
                    } else {
                        body.append(attrs.campo, attrs.model != "" ? attrs.model : null)
                    }
                }

                axios({
                    method : "PUT",
                    url    : `/api/insert/${this.realynames[this.aba]}/${this.id}`,
                    headers: {
                        Authorization: this.globais.authorization
                    },
                    data   : body
                }).then(res => {
                    this.globais[this.aba] = this.globais[this.aba].map(item => {
                        if (item.id == res.data.id) return res.data
                        return item 
                    })
                    this.$router.replace(`/admin/${this.aba}/${this.campos[this.aba]}`)
                })
            },

            Delete() {
                axios({
                    method : "DELETE",
                    headers: {
                        Authorization: this.globais.authorization
                    },
                    url    : `/api/insert/${this.realynames[this.aba]}/${this.id}`
                }).then(() => {
                    this.globais[this.aba] = this.globais[this.aba].filter(item => {
                        if (item.id != this.id) return item
                    })
                    this.$router.replace(`/admin/${this.aba}/${this.campos[this.aba]}`)
                })
            }
        },
        created() {
            for (let item of this.globais[this.aba]) {
                if (item.id == this.id) {
                    this.entidade = item
                    for (let campo of this.entidades[this.aba]) {
                        if (campo.model != undefined) {
                            if ((typeof item[campo.campo]) == "object") {
                                if (item[campo.campo]) campo.model = item[campo.campo].id
                            } else {
                                campo.model = item[campo.campo]
                            }
                        }
                    }
                    break
                }
            }
        }
    }
</script>

<style>
    #edit #del {
        padding: 4px 0;
        text-align: right;
        max-width: 600px;
        margin: 0 auto;
    }

    #edit #del button {
        padding: 7px;
        border: none;
        border-radius: 0.4rem;
        color: #eee;
        background: red;
        cursor: pointer;
    }
</style>
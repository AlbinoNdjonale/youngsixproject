<template>
  <div id="login">
      <form @submit = "login">
        <h1> Login </h1>
        <hr/>
        <br/>
        <div>
            <section id = "erro" v-if = "errouser || errovazio">
              <div v-if = "errovazio">
                <small>
                  <em>
                    Campos Vazios
                  </em>
                </small>
              </div>
              <div v-if = "errouser">
                <small>
                  <em>
                    Verifica se digitou o nome ou senha corretamento
                  </em>
                </small>
              </div>
            </section>
            <section>
                <label for = "nome"> Nome </label>
                <input type = "text" id = "nome" v-model = "nome">
            </section>
            <section>
                <label for = "senha"> Senha </label>
                <input type = "text" id = "senha" v-model = "senha">
            </section>
        </div>

        <div id = "btnlogin">
            <button>
                ENTRAR
            </button>
        </div>
      </form>
  </div>
</template>

<script>
    import axios from "../DataBack/config"

    import data from "../Data/data"

    export default {
        name: "login",
        data() {
            return {
                globais  : data,
                nome     : "",
                senha    : "",
                errovazio: false,
                errouser : false 
            }
        },
        methods: {
            login(e) {
                e.preventDefault()

                this.errouser  = false
                this.errovazio = false

                if (this.nome.trim() == ""
                  || this.senha.trim() == "") {
                    this.errovazio = true
                } else {
                  axios
                    .post("api/login", {
                      nome: this.nome,
                      senha: this.senha
                  })
                  .then(res => {
                      if (res.data) {
                        this.globais.usuario = res.data.usuario
                        this.globais.authorization = res.data.authorization
                        this.$router.replace("/admin")
                        
                        localStorage.setItem("user", JSON.stringify({
                          nome: res.data.usuario.nome,
                          senha: res.data.usuario.senha
                        }))
                      } else {
                        this.errouser = true
                      }
                  })
                }
            }
        }
    }
</script>

<style>

  #login {
    background: #666;
    padding: 5px;
    height: 99vh;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  #login form {
    background: #333;
    border-radius: 0.4rem;
    padding: 5px;
    width: 350px;
    color: #eee;
  }

  #login #erro {
    background: #eee;
    color: red;
    padding: 4px;
    border-radius: 0.4rem;
  }

  #login form section {
    display: grid;
    margin-bottom: 20px;
  }

  #login form section input {
    padding: 5px;
    border: none;
    outline: none;
    border-radius: 0.3rem;
    font-weight: 600;
  }
  
  #btnlogin {
    text-align: center;
  }

  #btnlogin button {
    padding: 5px;
    background: #0f0;
    border: none;
    border-radius: 0.3rem;
    cursor: pointer;
    color: #111;
    font-weight: 600;
  }
</style>
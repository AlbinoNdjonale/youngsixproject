export default {
    infoOfGroup  : {},
    musicas      : [],
    eps          : [],
    albums       : [],
    eventus      : [],
    fotos        : [],
    usuarios     : [],
    comentarios  : [],
    authorization: null,
    usuario      : null,
    TEMA         : null,
    alterTitle   : newTitle => {
        let Title = document.getElementsByTagName("title")[0].innerText
        Title = Title.split("|")[0].trim()
        document.getElementsByTagName("title")[0].innerText = `${Title} | ${newTitle}`
    }
}
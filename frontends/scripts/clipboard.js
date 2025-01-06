const copyButton= document.querySelector("#copyButton")
const copyInput=document.querySelector("#copyInput")

copyButton.addEventListener("click",function(){
    const projectsUrls=copyInput.value

    navigator.clipboard.writeText(projectsUrls)
    .then(()=>{
        alert(`成功複製到剪貼版:${projectsUrls}`)
    })
    .catch((error)=>{
        alert("複製失敗，請重試")
    })
})

var edit_mode_options = {
  create: 'CREATE_NEW_BLOG',
  modify: 'MODIFY_OLD_BLOG'
}

var edit_mode = edit_mode_options.create
var blogid_modified
//console.log('mdit:', marked)
var editor = document.getElementById('markdown-editor')
var editor_value
var preview = document.getElementById("markdown-preview")

editor.addEventListener('input', onEditorValueChange) 

window.onload=()=>{
  let textarea = document.getElementById('markdown-editor')
  let content_modified=textarea.value

  if(content_modified){
    edit_mode_options = edit_mode_options.modify
    textarea.value = content_modified
    blogid_modified=window.location.pathname.split('/')[3]
    console.log('path:', window.location.pathname.split('/')[3])
  }
  console.log('修改模式下的待修改的内容', content_modified)
}

function onEditorValueChange(e){
  editor_value = e.target.value
  preview.innerHTML = marked(e.target.value,{
      highlight: function (code) {  //代码高亮
          return hljs.highlightAuto(code).value
      }
  })
}

function publishBlog(){
  console.log('要发布的博客内容:', editor_value)
  let blogTitle = document.getElementById('blog-title-input').value
  console.log('标题:', blogTitle)
  postBlog(editor_value, blogTitle)

}

function saveBlog(){
  console.log('暂存')
  let blogTitle = document.getElementById('blog-title-input').value
  postBlog(editor_value, blogTitle,false)
}

function uploadImg(){

}

async function postBlog(content,title,isPublish=true){
  if(!content) {
    alert('请输入内容！')
    return 
  }
  if(!title) {
    alert('请输入标题')
    return
  }
  let path
  if(edit_mode === edit_mode_options.create){
    path = '/blog/createblog'
  }else{
    path = '/blog/createblog/'+blogid_modified
  }
  let userid = readCookies().filter(cookie => cookie.key.trim()==='logined_user_userid')[0].value
  let res = await api_post(path, {content,title,isPublish,userid})
  if(res.code === 0 ){
    alert(res.msg)
  }else{
    alert(res.msg)
  }
}

function readCookies(){
  let cookie = document.cookie
  console.log('cookie:', cookie)

  let items = cookie.split(';')
  let cookiesArr = items.map(
    item => {
      let [key, value] =  item.split('=')
      return {key, value}
    }
  )

  console.log('cookies:', cookiesArr)
  return cookiesArr
}


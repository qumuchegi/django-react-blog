var Rrender = ReactDOM.render
var cele = React.createElement
var ReactCom = React.Component
var api_get = api_post, api_post=api_post
var baseUrl = 'http://127.0.0.1:8000'

var edit_mode_options = {
  create: 'CREATE_NEW_BLOG',
  modify: 'MODIFY_OLD_BLOG'
}
var global_tags_choiced=[]
var edit_mode = edit_mode_options.create
var blogid_modified

var editor = document.getElementById('markdown-editor')
var editor_value
var preview = document.getElementById("markdown-preview")

editor.addEventListener('input', onEditorValueChange) 

function onImgUploadInputChange(){
  let imgUploadInput = document.getElementById('img-upload')
  let imgWillUploadContainer = document.getElementById('img-upload-hide')
  let imgSuccess = document.getElementById('img-upload-success')
  imgWillUploadContainer.setAttribute('class','show-img-container')

  let imgBlob = imgUploadInput.files[0]
  let imgReader = new FileReader()
  imgReader.readAsDataURL(imgBlob)
  imgReader.onload=function(){
    Rrender(
      cele(
        'div',
        {id:'img-will-upload'},
        cele('h2',null,'确认上传此图片？'),
        cele(
          'img',{src: this.result}
        ),
        cele(
          'div',{className:'ensure-upload'},
          cele('div',{
            onClick:()=>okToupload()
          },'确定上传'),
          cele('div',{
            onClick:()=>cancelToupload()
          },'取消')
        )
      ),
      imgWillUploadContainer
    )
  }
  
  async function okToupload(){
    console.log('确认',)
    let formData = new FormData()
    formData.append('upload-img', imgBlob)
    console.log('上传图片 data url:', imgBlob)
    let res = await api_post('/blog/uploadimg',formData)
    if(res.code===0){
      imgSuccess.setAttribute('class','show-img-success')
      imgWillUploadContainer.setAttribute('class','hide-img-container')
      Rrender(
        cele(
          'div',{
            className:'img-url-provider'
          },
          '请复制以下的图片路径到您需要放置图片的任何地方:',
          cele('div',{className:'url'},
          `![](${baseUrl}${res.imgurl.replace('blog','')})`
          ),
          cele(
            'img',
            {
              className:'close-button',
              onClick:()=>closeImgUrl(),
              src: baseUrl+'/static/imgs/close.png'
            }
          )
        ),
        imgSuccess
      )
    }

  }

  function cancelToupload(){
    imgWillUploadContainer.setAttribute('class','hide-img-container')
  }
 
  function closeImgUrl(){
    imgSuccess.setAttribute('class','hide-img-success')
  }
}

window.onload=()=>{
  let textarea = document.getElementById('markdown-editor')
  let content_modified=textarea.value


  if(content_modified){
    edit_mode_options = edit_mode_options.modify
    textarea.value = content_modified
    blogid_modified=window.location.pathname.split('/')[3]
    //console.log('path:', window.location.pathname.split('/')[3])
  }
  //console.log('修改模式下的待修改的内容', content_modified)

  Rrender(
    cele(BlogTagsChoice),document.getElementById('choice-blog-tags')
  )
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

  let res = await api_post(path, {content,title,isPublish,userid,tags: global_tags_choiced})
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

class BlogTagsChoice extends ReactCom{
  constructor(props){
    super(props)
    this.state={
      tags_options:[
        '前端','后端','javascript','Node','React','React Native','Vue','Python','Express','Django','Koa','Electron','NW.js',
        'Flutter','C++','C','Java','Spring','Github','面试'
      ],
      tags_choiced:[]
    }
  }
  
  componenetDidMount(){
    this.setState({tags_choiced: global_tags_choiced})
  }
  choicetag(tagname){
    let new_tags = this.state.tags_choiced
    new_tags.push(tagname)
    global_tags_choiced = new_tags
    this.setState({tags_choiced: new_tags})
  }
  removeTag(tagname){
    let new_tags = this.state.tags_choiced.filter(tag=>tag!==tagname)
    global_tags_choiced = new_tags
    this.setState({
      tags_choiced: new_tags
    })
  }
  render(){
    return(
      [cele(
        'div',{className:'tags-choiced'},
        cele(
          'div',null,'选择文章标签'
        ),
        cele(
          'div',null,
          this.state.tags_choiced.map(
            tag=>
            cele(
              'div',{className:'tag-item-choiced'},tag,
              cele(
                'img',
                {
                  className:'remove-button',
                  onClick:()=>this.removeTag(tag),
                  src: baseUrl+'/static/imgs/close.png'
                }
              )
            )
          )
        )
      ),
      cele(
        'div',{className:'tags-options'},
        this.state.tags_options.map(
          tag=>
          cele(
            'div',
            {
              className:'tag-item-choiced',
              onClick:()=>this.choicetag(tag)
            },
            tag
          )
        )
      )
    ]
    )
  }
}
var Rrender = ReactDOM.render
var cele = React.createElement
var ReactCom = React.Component
var api_get = api_post, api_post=api_post
var baseUrl = 'http://127.0.0.1:8000'

window.onload=()=>{
  let a_tag_blog = document.getElementsByClassName('blog-url')
  for(let a of a_tag_blog){
    url = a.href
    
    let path = url.match(/blog\/blogdetails\?blogid=\d*&userid=\d*/)[0]
    console.log('blog url:', path)
    a.href = baseUrl+'/'+path
  }
}
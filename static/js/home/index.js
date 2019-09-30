baseUrl = 'http://127.0.0.1:8000'
var cele = React.createElement,
    Rrender = ReactDOM.render,
    ReactCom = React.Component
var apiGet = api_get, apiPost = api_post // api.js封装

function readCookies(){
  let cookie = document.cookie
  console.log('cookie:', cookie)

  let items = cookie.split(';')
  let cookiesArr = items.length>1 && items.map(
    item => {
      let [key, value] =  item.split('=')
      return {key, value}
    }
  )

  console.log('cookies:', cookiesArr)
  return cookiesArr
}

class LeftNav extends ReactCom{
  constructor(props){
    super(props)
    this.state={
      userid:'',
      logined_user_info:'',
    }
  }
  componentDidMount(){

   let cookieArr = readCookies()

   if(cookieArr){
      let userid = cookieArr.filter(cookie => cookie.key.trim()==='logined_user_userid')[0].value//
      console.log('已经登录的用户的ID：', userid)
      this.setState({userid})
      this.featchUserInfo(userid)
      .then(userinfo=>this.setState({logined_user_info: userinfo}))
   }
  }

  async featchUserInfo(userid){
    let res = await apiGet('/user/userinfo/',{userid})
    if(res.code===0){
      console.log('userinfo:', res.user)
      return res.user
    }
  }

  logout(){
    delCookie('logined_user_userid')
    delCookie('jwt_token')
    this.setState({userid:''})
    
    function delCookie(name) {
      document.cookie = name + '=;  expires=Thu, 01 Jan 1970 00:00:01 GMT;'
    }
  }

  render(){
    let user = this.state.logined_user_info
    let buttons = [
      {name:'消息',url:''},
      {name:'写文章',url:'/blog/createblog'},
    ]
    let logined =  cele(
      'div',{id:'home-nav'},
       cele(
         'div',
         {id: 'user-info'},
         cele('img', {src: baseUrl + String(user.avatar_url).replace('user','')}),
         cele(
           'div',{id:'name-sex'},
           cele('div',null,user.username),
           cele('img',
            {
              src: (user.sex==='男'?baseUrl+'/static/imgs/Male.png': baseUrl+'/static/imgs/FeMale.png'),
              id: 'sex-icon'
            })
         ),
         cele(
           'a',{id: 'to-my-page',href: baseUrl + `/user/mypage/?userid=${this.state.userid}`},'个人主页'
         ),
         cele(
          'img',
          {
            src: baseUrl+'/static/imgs/log-out.png',
            className:'logout-icon',
            onClick:()=>this.logout()
          },null
         )
       ),
       cele(
         'div',
         {id: 'buttons'},
         buttons.map(ele=>
            cele(
              'a',
              {
                className:'button',
                href: baseUrl+ele.url
              },
              ele.name
            )
          )
       ),
       
    )
    let not_logined = cele(
      'div',{id:'not-logined'},
      cele(
        'a',{href: baseUrl+'/user/login'},'去登录'
      )
    )
    return(
      this.state.userid ? logined:not_logined
     
    )
  }
}

class Bloglist extends ReactCom{
  constructor(props){
    super(props)
    this.state={
      blogs:[],
      pageNum:1,
      userid:''
    }
  }
  componentDidMount(){
    let cookieArr = readCookies()
    if(cookieArr){
      let userid = readCookies().filter(cookie => cookie.key.trim()==='logined_user_userid')[0].value//
      this.setState({userid})
    }
    this.featchAllPubBlogs(this.state.pageNum)
  }
  
  async featchAllPubBlogs(pageNum){
    console.log('pageNum:', pageNum)

    let res = await  apiGet('/allpubblogs',{pageNum})
    if(res.code===0){
      console.log('blogs:', res.blogs)
      this.setState({blogs: res.blogs})
    }
  }
  prePage(){
    this.setState(
      (preState)=>({pageNum: --preState.pageNum}),
      ()=>this.featchAllPubBlogs(this.state.pageNum)
    )
  }
  nextPage(){
    this.setState(
      (preState)=>({pageNum: ++preState.pageNum}),
      ()=>this.featchAllPubBlogs(this.state.pageNum)
    )
  }
  render(){
    let Paginator = cele(
      'div',{id:'paginator'},
      this.state.pageNum>1 && cele(
        'div',
        {
          id:'pre-button',
          onClick:()=>this.prePage()
        },'上一页'
      ),
      this.state.blogs.length>0 && cele(
        'div',
        {
          id:'next-button',
          onClick:()=>this.nextPage()
        },'下一页'
      )
    )
    let BlogItem = blog => cele(
      'a',{
        className:'blog-item',
        href: baseUrl + '/blog/blogdetails' + `?blogid=${blog.blog_id}&userid=${blog.author_id}`,
      },
      cele('div',{className:'header'},
        cele('img',{className: 'author-avatar',src: baseUrl + '/static/' + blog.author_avatar},null),
        cele('div',null,
          cele('div',{className: 'author-name'}, blog.author_name),
          cele('div',{className: 'blog-last-modified'}, blog.blog_last_modified)
        ),
      ),
      cele('h3',{className: 'blog-title'}, blog.blog_title),
      cele('div',{className: 'content-img'}, 
        cele(
          'div',{className:'content'},blog.blog_content.slice(0,60),
        ),
        matchImgFromMarkdown(blog.blog_content) && cele(
          'img',{className:'blog-img',src: matchImgFromMarkdown(blog.blog_content)}
        )
      )
    )
    return(
      cele(
        'div',null,this.state.blogs.map(blog=>BlogItem(blog)),Paginator
      )
    )
  }
}

window.onload=()=>{
  Rrender(cele(LeftNav), document.getElementById('left-nav'))
  Rrender(cele(Bloglist), document.getElementById('blog-list'))
}

function matchImgFromMarkdown(markdown){
  //console.log('markdown:', markdown)
  let matcher = new RegExp(/!\[.*\]?\((http.*)\)/)
  // 匹配出图片后抽出图片URL，math返回的第二个元素极为正则中第一个圆括号括号内匹配的内容
  let imgURL = markdown.match(matcher)
  imgURL = Array.isArray(imgURL) ? imgURL[1]:imgURL
  console.log('匹配出图片：', imgURL)
  return imgURL
}


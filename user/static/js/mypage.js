baseUrl = 'http://127.0.0.1:8000'
var apiGet = api_get, apiPost = api_post
var userid // 当前登录用户的id
var cele = React.createElement
var Rrender = ReactDOM.render
var ReactCom = React.Component
var allMyBlogs = []
const renderContentType={ // 内容去渲染类型
  DEFAULT: '', // 渲染默认的组件
  MSG_NOT_READ: '未读消息', //渲染未读消息组件的详情组件
  MORE_PUB_BLOGS: '我的已发布的博客', //渲染更多我的博客列表组件
}

async function featchMyBlogs(myid){
  let path = '/blog/allmyblogs'
  let qsObj = {
    userid: myid
  }
  let data = await api_get(path, qsObj)
  return data
}

async function featchMyMsgNotRead(myid){
  let path = '/message/msgnotread'
  let res = await api_get(path,{userid: myid})
  if(res.code === 0){
    console.log('未读消息：', res.msgs)
    render_Num_Msg_NotRead(res.msgs)
  }
}

async function readManyMsgs(msg_ids_srr){// 读多条未读消息
  let res = await api_post('/message/readmanymsgs',{msg_ids: msg_ids_srr})
  if(res.code===0){
    console.log('消息已读')
    return true
  }
}

async function readSignalMsg(msg_id){// 读单条未读消息
  let res = await api_post('/message/readmsg',{msg_id})
  if(res.code===0){
    console.log('消息已读')
  }
}

function render_Num_Msg_NotRead(msgs){
  let badge_msg_num = cele('div',{id:'badge-msg-num'},msgs.length||null)
  let msgNotreadCom  = cele(
    'div' ,
    {
      id:'msg-not-read-entery', 
      onClick: ()=>renderContentArea(renderContentType.MSG_NOT_READ, componentShowMsgNotReadToContent(msgs)),
    },
    cele(
      'div',
      null,'未读消息'
    ),
    badge_msg_num
    )
  msgs.length ?
   Rrender(msgNotreadCom, document.getElementById('msg-not-read-container'))
   :
   Rrender(null,document.getElementById('msg-not-read-container'))
}

function componentShowMsgNotReadToContent(msgs){
  // 读消息
  var msg_ids = msgs.map(e=>e.msg_id)
  readManyMsgs(msg_ids).then(isRead=>{
      console.log('是否已经读完所有消息：', isRead)
      render_Num_Msg_NotRead([])
     }
    )

  return cele(
    'div',{id: "msg-not-read-details-list"},
    msgs.map(
      msg=>
      cele(
        'div',{key: msg.msg_id,className: 'msg-item'},
        cele('div',{className:'msg-head'},
          cele(
            'img',{
              src: baseUrl + msg.sender_avatar.replace(/user/,''),
              className:'sender-avatar',
              onClick: ()=>toUserPage(msg.sender_id)
            },null
          ),
          cele('div',{className:'sender-name'}, msg.sender_name),
          cele('div',{className:'send-time'},msg.send_time)
        ),
        cele('div',{className:'msg-content'},
            msg.msg_content
        ),
        cele(
          'a',
          {
            className:'msg-source-blog',
            href: baseUrl+`/blog/blogdetails?blogid=${msg.source_blog_id}&userid=${msg.source_blog_author_id}`,
          },
           `查看原博客： ${msg.source_blog_title}`
        ) 
      )
    )
  )
}

function toUserPage(userid){

}

function toBlog(blogid){

}

function renderContentArea(renderType, warped_contentComponent){ // 根据条件在 content 区域渲染对应的数据
  console.log('type:', renderType)
  class ContentCom extends ReactCom{
    constructor(props){
      super(props)
      this.state={
        renderType,
        userid:'',
      }
    }
    componentWillMount(){
      userid = window.location.search.split('=')[1]
      this.setState({userid})
    }

    render(){
      return(
        cele('div',null,
          cele(contentHeader,{renderType: this.state.renderType, userid: this.state.userid}),
          cele(contentContent,{renderType: this.state.renderType})
        )
      )
    }
  }

  class contentHeader extends ReactCom{
    constructor(props){
      super(props)
      this.state={
        navs:[
          {name:'首页',url:'/',icon:'/static/imgs/home.png'},
          {name:'历史消息',url: baseUrl+'/message/historymsgs?userid='+this.props.userid,icon:'/static/imgs/message.png'},
          {name:'我赞过的',url: baseUrl+'/star/mystars/to-others?userid='+this.props.userid,icon:'/static/imgs/blog.png'},
          {name:'谁赞了我',url: baseUrl+'/star/mystars/to-me?userid='+this.props.userid,icon:'/static/imgs/people.png'},
          {name:'我的评论',url: baseUrl+'/comment/mycomments?userid='+this.props.userid,icon:'/static/imgs/comment.png'}
        ]
      }
    }

    componentDidMount(){
      
      console.log('userid:', userid)
      console.log('渲染类型：', this.props.renderType)
    }
    render(){
      return cele('div',null,
        cele('div',{id:'nav'},
          this.state.navs.map(
            nav=>
            cele(
              'div',
              {className:'nav-item'},
              cele('img',{src: nav.icon,className: 'nav-icon'}),
              cele('a',{href: nav.url},nav.name)
            )
          )
        ),
       cele(
         'h3',null,  this.props.renderType
       )
      )
    }
  }

  class contentContent extends ReactCom{
    constructor(props){
      super(props)
      this.state={
        
      }
    }
    render(){
      return cele('div',null,warped_contentComponent)}
  }

  Rrender(cele(ContentCom),document.getElementById('content'))

}

function renderBlogList(blog, isSampleList=true){
  return  cele( // 找不到支持 JSX 的方式，暂时不用 JSX
    'a',
    {
      className: isSampleList ? "blog-list-item" : "complex-blog-list-item",
      key: blog.pk,
      href: baseUrl + '/blog/blogdetails' + `?blogid=${blog.pk}&userid=${blog.fields.author_id}`,
      //target: '_blank'
    },
    isSampleList ?
    blog.fields.blog_title
    :
    cele(
      'div',
      {className:'my-blog-item'},
      cele(
        'h3',null,blog.fields.blog_title,
        cele(
          'span',
          {className:'last-modify'},
          blog.fields.last_modified
          .match(/\d*-\d*-\d*/)[0])
      ),
      cele(
        'div',{className:'part-content-and-img'},
        cele(
          'div',
          {className:'part-content'}, 
          blog.fields.blog_content.slice(0,60)
          .replace(/(!\[.*\]?\((http.*\))|#)/g,''),
        ),
        matchImgFromMarkdown(blog.fields.blog_content) && cele(
          'img',
          {
            className:'blog-first-img',
            src: matchImgFromMarkdown(blog.fields.blog_content)
          },null
        )
      )
    )
  )
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

function showMorePubBlog(){
  let isSampleList = false
  let blogs = allMyBlogs.filter(ele=>ele.fields.is_publish===true)
  let allPubBlogsCom = cele(
    'div',{id:'all-pub-blogs-list'},
    blogs.length > 0 ?
    blogs.map(blog=>renderBlogList(blog,isSampleList))
    :
    cele('div',{id:'no-blogs'},'您还没有发布任何博客, 快去发布吧')
  )
  renderContentArea(renderContentType.MORE_PUB_BLOGS, allPubBlogsCom)
}

window.onload=()=>{
  renderContentArea(renderContentType.DEFAULT)
  userid = window.location.search.split('=')[1]
 
  featchMyMsgNotRead(userid)

  featchMyBlogs(userid)
  .then(data=>{
    console.log('blogs:', data.blogs)
    allMyBlogs = data.blogs
    Rrender(
      cele(
        'div',
        null,
        data.blogs
        .filter(ele=>ele.fields.is_publish===true)
        .sort((pre,next) => pre.fields.stars_num>next.fields.stars_num)
        .slice(0,3)
        .map(blog=> renderBlogList(blog))
      )
      ,
      document.getElementById('my-blog-list')
    )

    Rrender(
      cele(
        'div',
        null,
        data.blogs
        .filter(ele=>ele.fields.is_publish===false)
        .map(blog=>renderBlogList(blog))
      ),document.getElementById('my-blog-list-not-pub')
    )
  })
}



baseUrl = 'http://127.0.0.1:8000'
var cele = React.createElement
var render = ReactDOM.render
var ReactCom = React.Component
var comments =[]
var myAvatar
var blogid
var readerid , blogownerid

function readCookies(){
  let cookie = document.cookie

  let items = cookie.split(';')
  let cookiesArr = items.length>1 && items.map(
    item => {
      let [key, value] =  item.split('=')
      return {key, value}
    }
  )

  return cookiesArr
}

async function getBlog(blogid,authorid){

  let res = await api_post('/blog/blogdetails',{blogid,authorid})
  if(res.code === 0){
    console.log('blog:', res.blog, 'author:',res.author)
    renderBlog(res.blog[0].fields, res.author[0].fields)
  }
}

function renderBlog(blog,author){
  let {blog_content,blog_title, created_time} = blog

  myAvatar = baseUrl + '/' + author.avatar_url.replace('user/','')

  let sampleInfo = cele(
    'div',
    {id:'sample-info'},
    
    cele(
      'img',
      {
        id:'author-avatar',
        src: myAvatar
      },
      null
    ),
    cele(
      'div',
      {id:'time-authorname'},
      cele(
        'div',
        {id: 'author'},
        author.username
      ),
      cele(
        'div',
        {id: 'created-time'},
        created_time.match(/\d{4}-\d*-\d*/)[0]
      )
    ),
    blogownerid === readerid &&
    cele(
      'a',{href: baseUrl+'/blog/createblog/' + blogid, id:'modify-blog'},'编辑'
    )
  )

  document.getElementById('blog-content').innerHTML = 
  marked(blog_content,{
    highlight: function (code) {  //代码高亮
        return hljs.highlightAuto(code).value
    }
  })

  render(
    cele(
      'div',
      {id: 'blog-body'},
      sampleInfo,
      cele(
        'h3',
        {id: 'title'},
        blog_title
      )
    ),
    document.getElementById('blog-header')
  )
}

function renderComments(comments){

  class CommentsList extends ReactCom{
    constructor(props){
      super(props)
      this.state={
        comment_id_replying : null, // 正在被回复的评论的ID
        reply_id_replying: null // 正在被回复的回复的ID
      }
    }

    onClickComment(comment_id){
      this.setState(
        (prevState)=>prevState.comment_id_replying ? ({comment_id_replying: null}):({comment_id_replying: comment_id})
      )
    }

    onClickReply(reply_id){
      this.setState(
        (prevState)=>prevState.reply_id_replying ? ({reply_id_replying: null}):({reply_id_replying: reply_id})
      )
    }

    async starComment(commentid, comment_owner_id){
        let res = await api_post('/star/givestar',{
          star_from_userid: readerid,
          star_to_userid: comment_owner_id,
          star_for_type: 'comment',
          star_for_id: commentid
        })
        if(res.code===0){
          alert('点赞成功')
        }else if(res.code===1){
          alert('您已经赞过了！')
        }
    }

    async sendReply(receiver_id,comment_id,reply_id=''){
      let reply_content 
      if(!reply_id){
        reply_content = document.getElementById(`reply-input-${comment_id}`).value
      }else if(reply_id){
        reply_content = document.getElementById(`reply-to-reply-input-${reply_id}`).value
      }
      console.log('回复内容：', reply_content)
      if(!reply_content){
        return alert('请输入回复内容！')
      }
      let res = await api_post('/message/',{
        sender_id: readerid,
        receiver_id,
        content: reply_content,
        blogid: blogid,
        commentid: comment_id
      })
      if(res.code===0){
        alert('回复成功')
      }
    }

    render(){
      return comments.map(
        comment=>{
          let name_time =  cele(
            'div',
            {className:'commenter-name-time'},
            cele(
              'div',
              {className:'name'},
              comment.owner_name
            ),
            cele(
              'div',
              {className:'time'},
              comment.created_time.replace(/[TZ]/g,' ')
            )
          )
  
          let header = cele(
            'div',
            {className:'comment-item-header'},
            cele(
              'img',
              {className:'commenter-avatar',
              src: comment.owner_name === '我' ? comment.avatar : baseUrl + comment.avatar.replace('user','')
              },
              null
            ),
           name_time
          )
          let content = cele(
            'div',
            {className:'content'},
            comment.comment_content
          )
          let footer = cele(
            'div',{className: 'footer'},
            cele('div',{className:'icon'},
              cele(
                'div',null,
                cele('img',
                {
                  src: baseUrl+'/static/imgs/love-1.png',
                  onClick:()=>this.starComment(comment.comment_id, comment.owner_id)
                }),
               cele('div',{className: 'star-num'}, comment.star_num),
              ),
              cele('img',{src: baseUrl+'/static/imgs/comment.png',onClick:()=>this.onClickComment(comment.comment_id)})
            ),
            cele(
              'div',
              {
                className:'reply-input-container',
                id: this.state.comment_id_replying === comment.comment_id ? 'reply-input-show':'reply-input-hide'
              },
              cele(
                'input',
                {
                  type:'text',
                  placeholder: '尽情发炎吧',
                  id:`reply-input-${comment.comment_id}`,
                  className:'reply-input'
                },
              ),
              cele(
                'div',
                {className:'send-reply-button',onClick:()=>this.sendReply(comment.owner_id, comment.comment_id)},
                '发送'
              )
            )
          )
          let commentReply = cele(
            'div',{className:'comment-reply'},
            comment.comment_reply && 
            comment.comment_reply.map(reply=>
              cele(
                'div',{className: 'reply-item'},
                cele('div',{className:'reply-header'},
                  cele(
                    'div',{className:'reply-from-user'},
                    cele(
                      'img',{className:'avatar',src: baseUrl+reply.reply_from_user_avatar.replace('user','')}
                    ),
                    cele(
                      'div',{className:'name-time'},
                      cele(
                        'div',null,reply.reply_from_user_name
                      ),
                      cele(
                      'div',null,reply.reply_time
                    )
                    )
                  ),
                  cele('img',{className:'reply-direction',src: baseUrl+'/static/imgs/arrow-right.png'}),
                  cele(
                    'div',{className:'reply-to-user'},
                    cele(
                      'img',{className:'avatar',src: baseUrl+reply.reply_to_user_avatar.replace('user','')}
                    ),
                    cele(
                      'div',{className:'name-time'},
                      cele(
                        'div',null,reply.reply_to_user_name
                      )
                    )
                  ),
                
                ),
                 
                 cele(
                   'div',{className:'reply-content'},reply.reply_content
                 ),
                 cele(
                   'div',{className: 'reply-reply'},
                   cele('img',{src: baseUrl+'/static/imgs/reply.png',onClick:()=>this.onClickReply(reply.reply_id)}),
                   cele(
                    'div',
                    {
                      className:'reply-to-reply-input-container',
                      id: this.state.reply_id_replying === reply.reply_id ? 'reply-to-reply-input-show':'reply-to-reply-input-hide'
                    },
                    cele(
                      'input',
                      {
                        type:'text',
                        placeholder: '尽情发炎吧',
                        id:`reply-to-reply-input-${reply.reply_id}`,
                        className:'reply-to-reply-input'
                      },
                    ),
                    cele(
                      'div',
                      {
                        className:'send-reply-to-reply-button',
                        onClick:()=>this.sendReply(reply.reply_from_user_id, comment.comment_id,reply.reply_id)
                      },
                      '发送'
                    )
                  )
                 ),
              )
           )
          )
  
          return cele(
            'div',
            {className:'comment-item'},
            header,
            content,
            footer,
            commentReply
            )
        }
          
      )
    }
  }

  render(
    cele(CommentsList)
    ,
    document.getElementById('comments-list')
  )
}

window.onload = function(){
  var qs_arr = window.location.search.split('&')
  blogid = qs_arr[0].split('=')[1]
  blogownerid = qs_arr[1].split('=')[1]
  let cookiesArr = readCookies()
  if(cookiesArr){
    readerid =  cookiesArr.filter(cookie => cookie.key.trim()==='logined_user_userid')[0].value
  }
  getBlog(blogid,blogownerid)
  getBlogComment()
}

async function sendComment(){
  let commentContent = document.getElementById('comment-input').value
  console.log('评论内容：',commentContent)
  if(!commentContent){
    return alert('请输入评论！')
  }
  if(!readerid){
    return alert('请先登录！')
  }
  let res = await api_post('/comment/',{commentContent,readerid,blogid})
  if(res.code === 0){
    comments = comments.concat([{
      owner_name: '我',
      avatar: myAvatar,
      created_time: '现在',
      comment_content: commentContent
    }])
    console.log('现在的评论：', comments)
    renderComments(comments)
  }
}

async function getBlogComment(){
  let res = await api_get('/blog/blogcomments',{blogid})
  if(res.code === 0){
    console.log('获取评论：', res.comments)
    comments = res.comments
    renderComments(res.comments)
  }
}

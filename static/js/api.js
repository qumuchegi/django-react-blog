var baseurl = 'http://127.0.0.1:8000'

async function api_get(path, qsObj){
  let qs = ''
  for(let k in qsObj){
    qs += `${k}=${qsObj[k]}`
  }
  return _resHandler(await axios.get(baseurl + path + '?' + qs))
}

async function api_post(path, rqdata){
  //let csrftoken = document.cookie.split(";")[0].split("=")[1]
  //console.log('csrftoken:', csrftoken)
 
  return _resHandler(await axios.post(baseurl + path, rqdata))
}

const _resHandler = res => {
  let {data, status} = res
  console.log( "status", status, 'data', data);
  return data
}
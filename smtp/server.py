import sys
sys.path.insert(0,'..')
from settings import REDIRECT_URI
from flask import Flask,render_template, make_response,request
import base64,pickle,requests
from secret import CLIENT_ID,CLIENT_SECRET,TOKEN,NEWBIE,GUILD_ID
from Database import sql

db=sql.SQL()

app=Flask(__name__)

@app.errorhandler(404)
def not_found(e):
  return render_template("/HTML/404.html")

_url1="https://discord.com/api/oauth2/token"
_headers1= {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

_url2="https://discord.com/api/users/@me"

_headers3={
        'authorization':f'Bot {TOKEN}'
    }

headers = {'Content-Type': 'text/html'}

def get_role_id(role_name,header,guildID=GUILD_ID):
    resp=requests.get(url=f"https://discord.com/api/guilds/{guildID}/roles",headers=header).json()
    for role in resp:
        if(role['name']==role_name):
            return role['id']
    return 0

def update_role(userID,batch):
    newbie=get_role_id(NEWBIE,_headers3)
    batch=get_role_id(batch,_headers3)
    _url3=f"https://discord.com/api/guilds/{GUILD_ID}/members/{userID}/roles/{batch}"
    _url4=f"https://discord.com/api/guilds/{GUILD_ID}/members/{userID}/roles/{newbie}"
    requests.put(url=_url3,headers=_headers3)
    requests.delete(url=_url4,headers=_headers3)

@app.route('/verify',methods=['GET'])
def verify():
    state=request.args.get('state')
    code=request.args.get('code')
    if(state==None or code==None):
        return "Invalid"

    try:
        data=pickle.loads(base64.urlsafe_b64decode(state))
    except:
        return "Something went wrong"

    

    _data1={
        'client_id':CLIENT_ID,
        'client_secret':CLIENT_SECRET,
        'code':code,
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECT_URI,
        'scope': 'identify',
    }
    
    resp=requests.post(url=_url1,data=_data1,headers=_headers1).json()
    
    if("error" in resp.keys() or 'emailID' not in data.keys() or 'key' not in data.keys() or 'batch' not in data.keys()):
        return resp.get('error_description') or "some error"

    access_token=resp['access_token']
    token_type=resp['token_type']
    emailID=data['emailID']
    key=data['key']
    batch=data['batch']

    _headers2={
        'authorization': f'{token_type} {access_token}',
    }

    resp=requests.get(url=_url2,headers=_headers2).json()
    
    isPresent=requests.get(url=f"https://discord.com/api/guilds/{GUILD_ID}/members/{resp['id']}",headers=_headers3).json()
    
    if('message' in isPresent.keys()):
        return make_response(render_template('HTML/unknown_member.html'),200,headers)
        return isPresent['message']

    db.Connect()

    verified=db.isVerified(resp['id'],emailID)

    if(verified):
        return make_response(render_template('HTML/already_verified.html'),200,headers)
        return "already verified"
        
    ok=db.VerifyUser(resp['username']+resp['discriminator'],resp['id'],emailID,key)

    db.Close()

    if(ok):
        update_role(resp['id'],batch)
        return make_response(render_template('HTML/successfully_verified.html'),200,headers)
        return "successfully verified"
    
    return make_response(render_template('HTML/404.html'),200,headers)
    return "User Not Found"

if __name__ == "__main__":
    app.run()

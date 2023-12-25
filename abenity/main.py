from flask import Flask
from modules.abenity import Abenity
app = Flask(__name__)
 
@app.route('/abenity/v1/memberexport')
def member_export():
   abenity = Abenity()
   abenity.getMemberList()
   abenity.uploadMemberListToBlob()
   return {'status':'SUCCESS'}
 
if __name__ == '__main__':
   app.run(host='0.0.0.0',port=8081)
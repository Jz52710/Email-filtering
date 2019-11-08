from flask import Flask,render_template,request,jsonify,redirect
from isTrashEmail import GetRatio
from send import Send
S = Send()


app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/check",methods=['POST'])
def check():
    con = request.form['con']
    print(con)
    #计算概率
    flag = GetRatio(con) #正常邮件
    if flag:
        return jsonify({'code': 200, 'status': 'yes'})
    else:
        return jsonify({'code': 200, 'status': 'no'})

@app.route("/send",methods=['post'])
def send():
    email_to = request.form.get("email_to",None)
    item = request.form.get("item",None)
    con = request.form.get('con',None)
    S.sendEmail(con,email_to,item)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)

# -*- coding: utf-8
from flask import make_response ,request, Flask
from util import *
from db_module import DataBaseSystem
from register_module import RegisterSystem
from post_request import *
import base64

app = Flask(__name__)
host_addr = "0.0.0.0"
host_port = 5003
db_module = None

### 회원가입할때 단 한번만 씀
@app.route("/register/init", methods=["POST"])
def register_user():
    data = request.get_data().decode("utf-8")
    register_module = RegisterSystem.verify_user_data(data)
    if register_module.user_create:
        return json.dumps({
            "message": f"User with ID {register_module.user_id} is successfully created.", 
            "status": "true"
            }, ensure_ascii=False)
    elif not register_module.user_create:
        return json.dumps({
            "message": f"User with ID {register_module.user_id} already exists.", 
            "status": "false"
            }, ensure_ascii=False)
        
#=========================================DATABASE SYSTEMS============================================
### 여기서부터는 DataBase System
@app.route("/db/init", methods=["POST"])
def select_user_dbsys():
    global db_module
    data = request.json
    user_id = data["user_id"]
    db_module = DataBaseSystem.load_user_database(user_id)
    if db_module.user_create:
        return json.dumps({
            "message": f"Database file  of User with ID {user_id} is successfully created.", 
            "status": "true"
            }, ensure_ascii=False)
    elif not db_module.user_create: # false is not error -> existing user!
        return json.dumps({
            "message": f"Database file  of User with ID {user_id} is successfully selected.", 
            "status": "false"
            }, ensure_ascii=False)

@app.route("/db/create_update", methods=["POST"])
def create_update_dbsys():
    global db_module
    data = request.get_data().decode("utf-8")
    db_module.create_row(data)
    if db_module.row_create:
        return json.dumps({
            "message": f"data row of {db_module.user_id} is successfully created.", 
            "status": "true"
            }, ensure_ascii=False)
    elif not db_module.row_create: # status : false is updating existing rows.
        return json.dumps({
            "message": f"data row of {db_module.user_id} is successfully updated.", 
            "status": "false"
            }, ensure_ascii=False)
    

@app.route("/db/read_row", methods=["POST"])
def get_row():
    global db_module
    data = request.json
    date = data["date"]
    find_flag = db_module.find_target_row(date=date, display=False)
    if find_flag:
        response_dict = db_module.target_row.to_dict(orient="records")[0]
        print(response_dict)
        file_path = f"./user_id/{db_module.user_id}/data/img/{response_dict['img_filename']}"
        if os.path.exists(file_path):
            with open(file_path, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
                response_dict["image"] = encoded_image
        else:
            response_dict["image"] = ""
        if "song_indices" in response_dict.keys():
            response_dict["song_indices"] = list(map(int, response_dict["song_indices"].split("/")))
            try:
                response_dict["songs"] = json.loads(get_song_info(
                    response_dict["diary"], 
                    date, db_module.user_id, 
                    addr="141.223.140.4",
                    port=5004
                ).content)
            except:
                pass

        return json.dumps({
            "message": f"data row of {db_module.user_id} is successfully read.", 
            "status": "true", 
            "response": response_dict
            }, ensure_ascii=False)
    elif not find_flag:
        return json.dumps({
            "message": f"Error has occured. there is no row with User ID {db_module.user_id} and on {date}", 
            "status": "false"
            }, ensure_ascii=False)

@app.route("/db/remove_row", methods=["POST"])
def remove_row():
    global db_module
    data = request.get_data().decode("utf-8")
    delete_flag, date = db_module.delete_row(data)
    if delete_flag:
        return json.dumps({
            "message": f"data row of {db_module.user_id} with {date} is successfully deleted.", 
            "status": "true"
            }, ensure_ascii=False)
    elif not delete_flag:
        return json.dumps({
            "message": f"data row of {db_module.user_id} with {date} doesn't exist!", 
            "status": "false"
            }, ensure_ascii=False)

if __name__ == "__main__":
    app.run(
        host=host_addr,
        port=host_port,
        debug=True
    )
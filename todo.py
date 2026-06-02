from http.server import BaseHTTPRequestHandler, HTTPServer
import sqlite3
from urllib.parse import parse_qs



class ToDoApi(BaseHTTPRequestHandler):

    def do_GET(self):
        

        conn = sqlite3.connect(r"C:\Users\ELCOT\Desktop\python projects\todo.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM todo")
        result = cursor.fetchall()

        conn.close()

        html = """
        <html>
        <head>
        <title>TO-DO-LIST🗒️</title>
        <style>
        body{
        background-image:url("https://media.istockphoto.com/id/1419768610/photo/checklist-task-list-survey-and-assessment-quality-control-goals-achievement-and-business.jpg?s=612x612&w=0&k=20&c=U4cyMOKArfD0CRorhkLIrnTWPsTh1imDb8J2vvOw9MM=");
        background-size:cover;
        background-repeat:no-repeat;
        font-family:Serif;
        background-position:center;
        text-align:center;
        }
        input{
        width:250px;
        padding:10px;
        font-size:18px;
        }

        button{
         padding:10px;
         font-size:18px;
        }


        </style>
        </head>
        <body>
        <h1><center>TO-DO LIST</center></h1>


        <h2>Add Task</h2>
        <form method="POST">
            <input name="action" value="add" type="hidden">
            <input name="task" placeholder="Enter task">
            <button>Add</button>
        </form>

        <h2>Update Task</h2>
        <form method="POST">
            <input name="action" value="update" type="hidden">
            <input name="id" placeholder="Enter id">
            <input name="task" placeholder="New task">
            <button>Update</button>
        </form>

        <h2>Delete Task</h2>
        <form method="POST">
            <input name="action" value="delete" type="hidden">
            <input name="id" placeholder="Enter id">
            <button>Delete</button>
        </form>

        <h2>Tasks</h2>
        <ul>
        </body>
        </head>
        """

        for row in result:
            html += f"<li>{row[0]} - {row[1]}</li>"

        html += "</ul>"

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())


    def do_POST(self):
        length = int(self.headers['Content-Length'])
        body = self.rfile.read(length).decode()
        data = parse_qs(body)

        action = data["action"][0]
        conn = sqlite3.connect(r"C:\Users\ELCOT\Desktop\python projects\todo.db")
        cursor = conn.cursor()

        if action == "add":
            task = data["task"][0]
            cursor.execute("INSERT INTO todo(task) VALUES(?)", (task,))

        elif action == "update":
            task = data["task"][0]
            id = data["id"][0]
            cursor.execute("UPDATE todo SET task=? WHERE id=?", (task, id))

        elif action == "delete":
            id = data["id"][0]
            cursor.execute("DELETE FROM todo WHERE id=?", (id,))

        conn.commit()
        conn.close()

        self.send_response(303)
        self.send_header("Location", "/")
        self.end_headers()


server = HTTPServer(("localhost", 8000), ToDoApi)
print("Server running at http://localhost:8000")
server.serve_forever()
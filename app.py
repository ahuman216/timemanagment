from flask import Flask, render_template, request, redirect, url_for, Response
import threading
import time
import pomodoro
import todo
       
app = Flask(__name__)
@app.route("/pomodoro", methods=["GET", "POST"])
def pomodoro_page():
    if request.method == "POST":
        if "start" in request.form:
            pomodoro.start()
        elif "stop" in request.form:
            pomodoro.stop()
        return redirect(url_for("pomodoro_page"))

    phase, running, remaining, cycle = pomodoro.get_state()
    mins, secs = divmod(remaining, 60)
    return render_template(
        "pomodoro.html",
        phase=phase,
        is_running=running,
        cycle=cycle,
        time_left=f"{mins:02d}:{secs:02d}"
    )


@app.route("/pomodoro/stream")
def pomodoro_stream():
    def event_stream():
        import json, sys
        last_data = None
        while True:
            phase, running, remaining, cycle = pomodoro.get_state()
            data = {
                "phase": phase,
                "running": running,
                "remaining": remaining,
                "cycle": cycle
            }
            json_data = json.dumps(data)
            # Only send when data changes or every second (ensures refresh)
            if json_data != last_data:
                yield f"data: {json_data}\n\n"
                sys.stdout.flush()  # flush ensures browser receives instantly
                last_data = json_data
            time.sleep(1)

    # "text/event-stream" must NOT be buffered
    headers = {
        "Cache-Control": "no-cache",
        "X-Accel-Buffering": "no"  # for nginx/gunicorn later
    }
    return Response(event_stream(), headers=headers, mimetype="text/event-stream")
#todo
@app.route("/todo", methods=["GET", "POST"])
def todo_page():
    tasks = todo.load_tasks()

    if request.method == "POST":
        if "add" in request.form:
            task = request.form.get("task", "").strip()
            if task:
                tasks.append(task)
                todo.save_tasks(tasks)
        elif "delete" in request.form:
            index = int(request.form.get("delete"))
            if 0 <= index < len(tasks):
                tasks.pop(index)
                todo.save_tasks(tasks)

    return render_template("todo.html", tasks=tasks)

@app.route("/todols", methods=["GET", "POST"])
def todo_ls_page():
    return render_template("todo_ls.html")
    #return render_template("todo_localstorage.html")


#home
@app.route("/")
def home():
    return render_template("index.html")
if __name__ == "__main__":
    app.run(debug=True, threaded=True)


from flask import Flask, redirect, url_for

def create_app():
    app = Flask(__name__)
    
    @app.route("/")
    def hello_world():
        return "<p> Alo aloo </p>"
    


    @app.route("/admin")
    def admin():
        return redirect(url_for('user', name='Admin!' ))
    return app

if __name__ == "__main__":
    app.run()
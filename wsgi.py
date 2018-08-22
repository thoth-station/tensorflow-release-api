import connexion
from flask import redirect 

app = connexion.App(__name__)
app.add_api('swagger.yaml')
application = app.app

@app.route('/')
def base_url():
    """Redirect to UI by default."""
    return redirect('api/v1/ui')



if __name__ == '__main__':
    app.run(port=8080)
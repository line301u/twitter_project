from bottle import post, view

@get("/item")
@view("item")
def _():
    title = "Home"
    return dict(title=title, )

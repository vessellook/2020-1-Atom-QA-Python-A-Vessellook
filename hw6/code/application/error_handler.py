from application.my_handler import MyHandler


class ErrorHandler(MyHandler):
    def do_GET(self):
        self.make_response(code=500)

    def do_POST(self):
        self.make_response(code=500)

    def do_PUT(self):
        self.make_response(code=500)

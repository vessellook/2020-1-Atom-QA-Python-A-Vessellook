from locust import HttpUser, TaskSet, task, between
import time


class AdvancedUserBehavior(TaskSet):
    def on_start(self):
        r = self.client.get("/", auth=('advanced', "advanced"))
        self.client.headers.update({'Authorization': r.request.headers['Authorization']})

    def on_stop(self):
        self.client.get("/logout")

    @task
    def photo(self):
        self.client.get("/photos")
        for i in range(10):
            self.client.get(f"/photos/{i}")
            time.sleep(.5)

    @task
    def profile(self):
        self.client.get("/profile")

    @task
    def shareware(self):
        self.client.get('/shareware')


class BeginnerBehaviour(TaskSet):
    def on_start(self):
        self.client.get('/photos')
        r = self.client.get("/", auth=('beginner', "beginner"))
        self.client.headers.update({'Authorization': r.request.headers['Authorization']})

    def on_stop(self):
        self.client.get("/logout")

    @task
    def photo(self):
        for i in range(10):
            self.client.get("/photos")
            time.sleep(2)
            self.client.get(f"/photos/{i}")
            time.sleep(.5)

    @task
    def shareware(self):
        self.client.get("/shareware")
        self.client.get("/profile")
        self.client.get("/photos")
        self.client.get("/shareware")


class WebsiteUser(HttpUser):
    tasks = [AdvancedUserBehavior, BeginnerBehaviour]
    wait_time = between(1, 2)

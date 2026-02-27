from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def index(self):
        self.client.get("/")
    
    @task(3)
    def view_item(self):
        item_id = 1
        self.client.get(f"/item/{item_id}", name="/item/[id]")

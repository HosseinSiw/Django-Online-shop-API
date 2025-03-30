from locust import HttpUser, task


class LocustUser(HttpUser):
    @task
    def product_list(self):
        self.client.get("/products/api/v1/products/")

        
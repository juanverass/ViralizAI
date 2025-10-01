from fastapi import FastAPI
from interfaces.api import conta_controller
from interfaces.api.video_controller import video_controller

class RouterRegistrationBlock:
    def __init__(self):
        # lista de tuplas: (objeto router, prefix, tags)
        self.routers = [
            (video_controller.router, "/videos", ["Vídeos"]),
            (conta_controller.router, "/contas", ["Contas"]),
            (conta_controller.router, "/postagensagendadas", ["Postagens Agendadas"]),
            # (legenda_router.router, "/legendas", ["Legendas"]),
            # (dublagem_router.router, "/dublagens", ["Dublagens"]),
        ]

    def register_all(self, app: FastAPI):
        for router, prefix, tags in self.routers:
            app.include_router(router, prefix=prefix, tags=tags)
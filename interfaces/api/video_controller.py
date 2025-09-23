from fastapi import APIRouter, Depends, Request
from app.services.service_registration_block import ServiceRegistrationBlock

router = APIRouter()

def get_services(request: Request) -> ServiceRegistrationBlock:
    return request.app.state.services

@router.post("")
def create_video(
    title: str, 
    source_url: str, 
    services: ServiceRegistrationBlock = Depends(get_services)
):
    return services.video_service.create_video(title, source_url)
from typing import List
from domain.entities.postagens_agendadas.postagem_agendada import PostagemAgendada, StatusDaPostagem
from domain.entities.videos.video import Video
from domain.entities.contas.conta import Conta
from infrastructure.models.postagens_agendadas.postagem_agendada_db_mapping import PostagemAgendadaDbMapping
from infrastructure.models.videos.video_db_mapping import VideoDbMapping
from infrastructure.models.contas.conta_db_mapping import ContaDbMapping

class PostagemAgendadaPersistenceMapper:
    """Mapper entre PostagemAgendada (domínio) e PostagemAgendadaDbMapping (ORM)"""
    
    @staticmethod
    def to_model(entity: PostagemAgendada) -> PostagemAgendadaDbMapping:
        return PostagemAgendadaDbMapping(
            id=entity.id,
            descricao=entity.descricao,
            data_para_envio=entity.data_para_envio,
            status=entity.status,
            id_video=entity.video.id,
            video=VideoDbMapping(
                id=entity.video.id,
                title=entity.video.title,
                source_url=entity.video.source_url,
                local_path=entity.video.local_path,
                status=entity.video.status.value,
                duration=entity.video.duration,
                language=entity.video.language
            )
        )

    @staticmethod
    def to_entity(model: PostagemAgendadaDbMapping) -> PostagemAgendada:
        return PostagemAgendada(
            id=model.id,
            descricao=model.descricao,
            data_para_envio=model.data_para_envio,
            status=model.status,
            id_video=model.id_video,
            video=Video(
                id=model.video.id,
                title=model.video.title,
                source_url=model.video.source_url,
                local_path=model.video.local_path,
                status=model.video.status,
                duration=model.video.duration,
                language=model.video.language
            ),
            contas=[Conta(id=conta.id, plataforma=conta.plataforma) for conta in model.contas]
        )
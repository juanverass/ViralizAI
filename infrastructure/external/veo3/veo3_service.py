from google import genai
from google.genai import types
import time

API_KEY = "AIzaSyDfdrGlSdbA66IA_donv6NIzDdiHWPAsus";
client = genai.Client(api_key=API_KEY) 

class Veo3Service():
    def __init__(self):
        self.api_key = API_KEY
        

    
    # @staticmethod
    # def gerar_video_VEO3(roteiro: str) -> dict:
    #     operation = client.models.generate_videos(model='veo-3.0-generate-preview', prompt=roteiro)
    #     # Alternatively, you can use operation.name to get the operation.
    #     operation = types.GenerateVideosOperation(name=operation.name)

    #     # This loop checks the job status every 10 seconds.
    #     while not operation.done:
    #         time.sleep(10)
    #         # Refresh the operation object to get the latest status.
    #         operation = client.operations.get(operation)
        
    #     generated_video = operation.response.generated_videos[0]
    #     client.files.download(file=generated_video.video)
    #     generated_video.video.save("dialogue_example.mp4")

    #     print(f"Video: {generated_video}")
    #     return f"video: {generated_video}"
    
    def gerar_video_VEO3(roteiro: str) -> str:
        """
        Gera um vídeo usando o modelo Veo 3 do Google AI Studio (Gemini API).
        O método aguarda até o vídeo estar pronto e o salva localmente.
        """

        for model in client.models.list():
            print(model.name)

        print("🎬 Iniciando geração de vídeo com Veo 3...")
        print(f"Prompt enviado: {roteiro}")

        # Inicia a geração do vídeo (retorna uma operação longa)
        operation = client.models.generate_videos(
            model="veo-3.0-generate-preview",  # nome do modelo mais estável
            prompt=roteiro,
            config=types.GenerateVideosConfig(
                aspect_ratio="16:9"
            )
        )

        # A operação contém um nome de job (necessário para monitorar o progresso)
        operation_name = operation.name
        print(f"🕐 Operação iniciada: {operation_name}")

        # Cria um objeto de operação baseado no nome retornado
        op = types.GenerateVideosOperation(name=operation_name)

        # Espera até que o job seja concluído
        while not op.done:
            print("⌛ Ainda gerando... Aguardando 10s...")
            time.sleep(10)
            op = client.operations.get(op)  # atualiza o status

        if not op.response or not op.response.generated_videos:
            raise Exception("❌ Nenhum vídeo foi gerado. Verifique o prompt ou o status da API.")

        # Extrai o primeiro vídeo gerado
        generated_video = op.response.generated_videos[0]
        file_info = generated_video.video

        # Faz o download do arquivo
        print("📥 Fazendo download do vídeo gerado...")
        file_data = client.files.download(file=file_info)

        output_path = "C:/backups/meu_video.mp4"

        with open(output_path, "wb") as f:
            f.write(file_data)

        print("✅ Vídeo gerado e salvo como video_veo3.mp4")

        return "video_veo3.mp4"
        
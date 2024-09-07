from rest_framework.renderers import JSONRenderer


class CustomJSONRenderer(JSONRenderer):
    charset = "utf-8"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        # Définir une structure de réponse personnalisée
        response = {
            "status": renderer_context["response"].status_code,
            "message": (
                "Success" if renderer_context["response"].status_code < 400 else "Error"
            ),
            "data": data,
        }
        return super().render(response, accepted_media_type, renderer_context)

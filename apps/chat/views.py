"""
Chat - Vistas y endpoints para el chatbot
"""
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from .models import ChatSession, ChatMessage
from .services import get_chat_service


def chat_interface(request):
    """
    Vista principal del widget de chat.
    Renderiza la interfaz del chatbot.
    """
    # Crear o recuperar sesión
    session_id = request.session.get('chat_session_id')
    if not session_id:
        session = ChatSession.objects.create()
        request.session['chat_session_id'] = str(session.session_id)
        session_id = str(session.session_id)
    
    return render(request, 'chat/interface.html', {
        'session_id': session_id
    })


@require_POST
@csrf_exempt  # TODO: Implementar CSRF token en frontend
def send_message(request):
    """
    Endpoint para enviar mensajes al chatbot.
    
    POST /chat/message/
    Body: {"message": "...", "session_id": "..."}
    
    Response: {"response": "...", "sources": [...]}
    """
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    
    message = data.get('message', '').strip()
    session_id = data.get('session_id')
    
    if not message:
        return JsonResponse({'error': 'Mensaje vacío'}, status=400)
    
    # Obtener o crear sesión
    try:
        if session_id:
            session = ChatSession.objects.get(session_id=session_id)
        else:
            session = ChatSession.objects.create()
    except ChatSession.DoesNotExist:
        session = ChatSession.objects.create()
    
    # Guardar mensaje del usuario
    user_msg = ChatMessage.objects.create(
        session=session,
        role='user',
        content=message
    )
    
    # Procesar con servicio de chat
    chat_service = get_chat_service()
    result = chat_service.process_message(
        session_id=str(session.session_id),
        user_message=message
    )
    
    # Guardar respuesta del asistente
    assistant_msg = ChatMessage.objects.create(
        session=session,
        role='assistant',
        content=result['response'],
        sources=result.get('sources', []),
        metadata={
            'model': result.get('model'),
            'tokens': result.get('tokens'),
        }
    )
    
    # Actualizar contador de mensajes
    session.total_messages += 2
    session.save(update_fields=['total_messages', 'updated_at'])
    
    return JsonResponse({
        'response': result['response'],
        'sources': result.get('sources', []),
        'session_id': str(session.session_id),
        'message_id': assistant_msg.id,
    })


@require_GET
def get_history(request):
    """
    Obtiene el historial de mensajes de una sesión.
    
    GET /chat/history/?session_id=...
    """
    session_id = request.GET.get('session_id')
    if not session_id:
        return JsonResponse({'error': 'session_id requerido'}, status=400)
    
    try:
        session = ChatSession.objects.get(session_id=session_id)
    except ChatSession.DoesNotExist:
        return JsonResponse({'error': 'Sesión no encontrada'}, status=404)
    
    messages = session.messages.values('role', 'content', 'created_at')
    
    return JsonResponse({
        'session_id': str(session.session_id),
        'messages': list(messages)
    })


# =============================================================================
# Gemini Integration (New)
# =============================================================================
import google.generativeai as genai
import os

@require_POST
@csrf_exempt
def chat_with_gemini(request):
    """
    Controlador para chat directo con Gemini 2.0 Flask via API.
    Soporta memoria conversacional (Historía) basada en sesiones de Django.
    Endpoint: /chat/api/
    """
    try:
        # 1. Configuración
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            return JsonResponse({'error': 'API Key no configurada'}, status=500)
        
        genai.configure(api_key=api_key)
        
        # 2. Obtener datos
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)

        if not user_message:
            return JsonResponse({'error': 'Mensaje vacío'}, status=400)

        # 3. Configurar Personalidad (System Prompt)
        CONTEXTO_BESTIA = (
            "Eres el Consultor Técnico Senior de 'bestIA', ingeniería y desarrollo de software en Puerto Montt, Chile. "
            "Tu Identidad: Profesional técnico, sobrio, experto. No usas saludos robóticos. "
            "Base de Conocimiento: "
            "1. Ubicación: Puerto Montt, Región de Los Lagos. "
            "2. Servicios: Desarrollo a Medida (SaaS, Web Apps), Automatización IA, Consultoría de Arquitectura de Software. "
            "3. Cursos: 'IAlfabetización' (programa práctico de IA para empresas/ejecutivos, no para programadores). "
            "Reglas de Comportamiento: "
            "1. NO uses listas con viñetas (bullets) salvo que sea IMPRESCINDIBLE. Prefiere párrafos cortos y fluidos. "
            "2. Concisión Extrema: Máximo 3 oraciones por idea principal. Ve al grano. "
            "3. Tono: Conversacional de negocios. Evita 'Espero haberte ayudado'. "
            "4. Objetivo Comercial: Calificar el lead. Si preguntan 'qué hacen', explica brevemente y cierra con una pregunta "
            "como '¿Buscas esto para tu empresa o para formación personal?'. Si hay intención de compra clara, sugiere contactar por WhatsApp."
        )

        # 4. Inicializar Modelo
        model_name = "gemini-2.0-flash-exp"
        try:
            model = genai.GenerativeModel(
                model_name=model_name,
                system_instruction=CONTEXTO_BESTIA
            )
        except Exception:
            model_name = "gemini-1.5-flash"
            model = genai.GenerativeModel(
                model_name=model_name,
                system_instruction=CONTEXTO_BESTIA
            )

        # 5. Gestión de Memoria (Historial en Sesión)
        # Recuperar historial de la sesión (o lista vacía)
        # Estructura esperada por SDK Python: [{'role': 'user', 'parts': [...]}, {'role': 'model', 'parts': [...]}]
        history_key = 'gemini_chat_history'
        raw_history = request.session.get(history_key, [])
        
        # Validar y limpiar historial si es necesario (para evitar errores de formato antiguos)
        validated_history = []
        for msg in raw_history:
            if 'role' in msg and 'parts' in msg:
                validated_history.append(msg)
        
        # Iniciar chat con historial
        chat = model.start_chat(history=validated_history)

        # 6. Generar Respuesta
        response = chat.send_message(user_message)
        
        # 7. Actualizar y Guardar Historial
        # El objeto 'chat' actualiza su history interno, pero debemos serializarlo para guardar en sesión
        # Lo hacemos manualmente para asegurar compatibilidad JSON simple
        
        # Agregamos el nuevo turno a nuestro historial validado
        new_history = validated_history + [
            {'role': 'user', 'parts': [user_message]},
            {'role': 'model', 'parts': [response.text]}
        ]
        
        # Guardar en sesión
        request.session[history_key] = new_history
        request.session.modified = True
        
        return JsonResponse({
            "response": response.text,
            "status": "success",
            "model": model_name
        })

    except Exception as e:
        print(f"Error en Gemini Chat: {e}")
        # En caso de error (ej. token limit), podrías querer limpiar el historial
        # request.session['gemini_chat_history'] = [] 
        return JsonResponse({'error': str(e), 'status': 'error'}, status=500)

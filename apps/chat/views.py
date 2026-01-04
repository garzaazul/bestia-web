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
    PERSISTENCIA: Usa base de datos (ChatSession.history).
    """
    try:
        # 1. Configuración
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            return JsonResponse({'error': 'API Key no configurada'}, status=500)
        
        genai.configure(api_key=api_key)
        
        # 2. Obtener datos y Sesión DB
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)

        if not user_message:
            return JsonResponse({'error': 'Mensaje vacío'}, status=400)

        # Recuperar ID de sesión de la cookie (o crear nueva)
        session_id_str = request.session.get('chat_session_id')
        chat_session = None

        if session_id_str:
            try:
                chat_session = ChatSession.objects.get(session_id=session_id_str)
            except ChatSession.DoesNotExist:
                pass
        
        if not chat_session:
            chat_session = ChatSession.objects.create()
            request.session['chat_session_id'] = str(chat_session.session_id)

        # 3. Configurar Personalidad (System Prompt con Contexto Dinámico)
        # ID de sesión para referencia
        current_id = str(chat_session.session_id)
        
        # Lógica de Handoff (WhatsApp)
        wa_number = "56972420708"
        wa_text = f"Hola, vengo del chat web (Ref: {current_id}). Quiero hablar con un humano."
        wa_link = f"https://wa.me/{wa_number}?text={wa_text.replace(' ', '%20')}"

        CONTEXTO_BESTIA = (
            f"Tu ID de sesión es: {current_id}. "
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
            "4. SMART HANDOFF: Cuando detectes que el usuario quiere contactar a un humano o contratar, genera un enlace de WhatsApp. "
            f"El formato del enlace DEBE ser: {wa_link} "
            "Aclara siempre: 'Te paso con un ingeniero humano. Haz clic aquí para abrir WhatsApp con tu referencia de caso'."
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

        # 5. Gestión de Memoria (DB Persistence)
        # Recuperar historial de la BD
        raw_history = chat_session.history if chat_session.history else []
        
        # Validar formato (lista de dicts con 'role' y 'parts')
        validated_history = []
        if isinstance(raw_history, list):
            for msg in raw_history:
                if isinstance(msg, dict) and 'role' in msg and 'parts' in msg:
                    validated_history.append(msg)
        
        # Iniciar chat con historial
        chat = model.start_chat(history=validated_history)

        # 6. Generar Respuesta
        response = chat.send_message(user_message)
        
        # 7. Actualizar y Guardar Historial en BD
        new_history = validated_history + [
            {'role': 'user', 'parts': [user_message]},
            {'role': 'model', 'parts': [response.text]}
        ]
        
        chat_session.history = new_history
        chat_session.total_messages += 2
        chat_session.save()
        
        return JsonResponse({
            "response": response.text,
            "status": "success",
            "model": model_name,
            "session_id": current_id
        })

    except Exception as e:
        print(f"Error en Gemini Chat: {e}")
        return JsonResponse({'error': str(e), 'status': 'error'}, status=500)

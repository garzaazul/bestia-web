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

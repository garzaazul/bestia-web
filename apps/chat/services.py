"""
Chat - Capa de servicios para integración con LLMs

ARQUITECTURA DE SERVICIOS:
- ChatService: Orquesta la conversación
- LLMProvider: Interfaz abstracta para LLMs (OpenAI, Anthropic, etc.)
- RAGService: Retrieval-Augmented Generation (futura implementación)

NOTA: Esta es la ARQUITECTURA preparada, no la implementación completa.
La lógica de IA se implementará en una fase posterior.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class Message:
    """Mensaje en formato estándar para comunicación con LLMs."""
    role: str  # 'user', 'assistant', 'system'
    content: str


@dataclass
class LLMResponse:
    """Respuesta del LLM."""
    content: str
    model: str
    tokens_used: Dict[str, int]  # {'prompt': X, 'completion': Y, 'total': Z}
    finish_reason: str
    raw_response: Optional[Any] = None


@dataclass
class RetrievedDocument:
    """Documento recuperado del vector store (RAG)."""
    content: str
    source: str
    score: float
    metadata: Dict[str, Any]


# =============================================================================
# ABSTRACT INTERFACES
# =============================================================================

class LLMProvider(ABC):
    """
    Interfaz abstracta para proveedores de LLM.
    Implementar para cada proveedor: OpenAI, Anthropic, etc.
    """
    
    @abstractmethod
    def generate(
        self,
        messages: List[Message],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> LLMResponse:
        """Genera una respuesta dado un historial de mensajes."""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Verifica si el proveedor está disponible y configurado."""
        pass


class VectorStore(ABC):
    """
    Interfaz abstracta para almacenamiento vectorial (RAG).
    Implementar para: Pinecone, Qdrant, pgvector, etc.
    """
    
    @abstractmethod
    def search(
        self,
        query: str,
        top_k: int = 5,
        filter: Optional[Dict] = None
    ) -> List[RetrievedDocument]:
        """Busca documentos relevantes para la query."""
        pass
    
    @abstractmethod
    def upsert(
        self,
        document_id: str,
        content: str,
        metadata: Dict[str, Any]
    ) -> bool:
        """Indexa o actualiza un documento."""
        pass


# =============================================================================
# SERVICE IMPLEMENTATIONS (STUBS)
# =============================================================================

class PlaceholderLLMProvider(LLMProvider):
    """
    Proveedor placeholder para desarrollo.
    Retorna respuestas predefinidas sin llamar a APIs externas.
    """
    
    def generate(
        self,
        messages: List[Message],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> LLMResponse:
        logger.warning("Using PlaceholderLLMProvider - no real LLM integration")
        
        # Respuesta placeholder
        last_message = messages[-1].content if messages else ""
        
        return LLMResponse(
            content=(
                "Gracias por tu mensaje. El chatbot de bestIA aún está en desarrollo. "
                "Por favor, contacta a contacto@bestia.cl para más información."
            ),
            model="placeholder",
            tokens_used={'prompt': 0, 'completion': 0, 'total': 0},
            finish_reason="placeholder"
        )
    
    def is_available(self) -> bool:
        return True


class PlaceholderVectorStore(VectorStore):
    """Placeholder para vector store - sin implementación real."""
    
    def search(
        self,
        query: str,
        top_k: int = 5,
        filter: Optional[Dict] = None
    ) -> List[RetrievedDocument]:
        logger.warning("Using PlaceholderVectorStore - no RAG available")
        return []
    
    def upsert(
        self,
        document_id: str,
        content: str,
        metadata: Dict[str, Any]
    ) -> bool:
        logger.warning("Using PlaceholderVectorStore - document not indexed")
        return False


# =============================================================================
# MAIN CHAT SERVICE
# =============================================================================

class ChatService:
    """
    Servicio principal de chat.
    Orquesta la conversación, integra RAG y maneja el historial.
    """
    
    def __init__(
        self,
        llm_provider: Optional[LLMProvider] = None,
        vector_store: Optional[VectorStore] = None
    ):
        self.llm = llm_provider or PlaceholderLLMProvider()
        self.vector_store = vector_store or PlaceholderVectorStore()
        
        # System prompt base
        self.system_prompt = """Eres un asistente de bestIA Engineering, una consultora de IA B2B.
Tu objetivo es ayudar a potenciales clientes a entender cómo la inteligencia artificial 
puede optimizar sus procesos empresariales.

Áreas de expertise:
- Agentes Autónomos y RAG
- Automatización (RPA + IA)
- Consultoría Estratégica de IA
- Programa de IAlfabetización Digital

Mantén un tono profesional pero accesible. Si no puedes responder algo, 
sugiere contactar directamente a contacto@bestia.cl."""

    def process_message(
        self,
        session_id: str,
        user_message: str,
        use_rag: bool = True
    ) -> Dict[str, Any]:
        """
        Procesa un mensaje del usuario y genera respuesta.
        
        Args:
            session_id: ID de la sesión de chat
            user_message: Mensaje del usuario
            use_rag: Si True, busca en base de conocimiento
        
        Returns:
            Dict con respuesta y metadatos
        """
        # 1. Recuperar contexto relevante (RAG)
        context_docs = []
        if use_rag:
            context_docs = self.vector_store.search(user_message, top_k=3)
        
        # 2. Construir mensajes para el LLM
        messages = [Message(role='system', content=self.system_prompt)]
        
        # Agregar contexto de documentos si existe
        if context_docs:
            context_text = "\n\n".join([
                f"[Documento: {doc.source}]\n{doc.content}"
                for doc in context_docs
            ])
            messages.append(Message(
                role='system',
                content=f"Contexto relevante:\n{context_text}"
            ))
        
        # TODO: Agregar historial de conversación desde la sesión
        
        # Agregar mensaje del usuario
        messages.append(Message(role='user', content=user_message))
        
        # 3. Generar respuesta
        response = self.llm.generate(messages)
        
        return {
            'response': response.content,
            'sources': [doc.source for doc in context_docs],
            'model': response.model,
            'tokens': response.tokens_used,
        }


# =============================================================================
# FACTORY
# =============================================================================

def get_chat_service() -> ChatService:
    """
    Factory para obtener el servicio de chat configurado.
    En el futuro, aquí se inyectarán los proveedores reales.
    """
    # TODO: Detectar configuración de entorno y usar proveedores reales
    # from decouple import config
    # if config('OPENAI_API_KEY', default=None):
    #     llm = OpenAIProvider(api_key=config('OPENAI_API_KEY'))
    # ...
    
    return ChatService()

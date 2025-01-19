from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from saju_rag.di.config import Settings

from saju_rag.core.usecase.extract_saju_usecase import ExtractSajuUseCase
from saju_rag.core.usecase.answer_with_external_info_usecase import (
    AnswerWithExternalInfoUsecase,
)

from saju_rag.component.llm.gpt import ChatGptClient

from saju_rag.component.repositories.saju_webapi import ShinhanSajuWebApi
from saju_rag.component.repositories.elasticsearch import ElasticsearchRepository

from saju_rag.core.infra.zenrows import get_zenrows_client
from saju_rag.core.infra.es_client import get_es_client
from saju_rag.core.infra.embedding import load_model, load_tokenizer
from saju_rag.core.infra.gpt_client import get_gpt_client

from saju_rag.component.connector import ConnectorProvider


class BaseContainer(DeclarativeContainer):
    config: Settings = providers.Configuration()
    # infra
    zenrows_client = providers.Resource(
        get_zenrows_client, api_key=config.zenrows_api_key
    )
    openai_client = providers.Resource(get_gpt_client, api_key=config.openai_api_key)

    embedding_model = providers.Resource(
        load_model, model_name=config.embedding_model_name
    )

    embedding_tokenizer = providers.Resource(
        load_tokenizer, model_name=config.embedding_model_name
    )

    es_client = providers.Resource(
        get_es_client,
        es_url=config.elasticsearch_url,
        es_username=config.elasticsearch_username,
        es_password=config.elasticsearch_password,
    )

    # repository
    saju_web_api_repository = providers.Factory(
        ShinhanSajuWebApi, zenrows_client=zenrows_client, host=config.shinhan_saju_host
    )

    es_repository = providers.Factory(
        ElasticsearchRepository,
        es_client=es_client,
    )

    # module
    chat_gpt_client = providers.Factory(ChatGptClient, client=openai_client)

    connector_provider = providers.Factory(
        ConnectorProvider,
        model=embedding_model,
        tokenizer=embedding_tokenizer,
        es_repository=es_repository,
        openai_client=openai_client
    )

    # usecase
    gpt_extract_saju_usecase = providers.Singleton(
        ExtractSajuUseCase,
        saju_extractor=chat_gpt_client,
        saju_repository=saju_web_api_repository,
    )

    gpt_answer_with_external_info_usecase = providers.Singleton(
        AnswerWithExternalInfoUsecase,
        select_connector_port=chat_gpt_client,
        answer_with_connector_info_port=chat_gpt_client,
        connector_provider_port=connector_provider,
    )

from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from saju_rag.di.config import Settings

from saju_rag.core.usecase.extract_saju_usecase import ExtractSajuUseCase
from saju_rag.core.usecase.answer_with_external_info_usecase import (
    AnswerWithExternalInfoUsecase,
)

from saju_rag.component.llm.gpt import ChatGptClient

from saju_rag.component.repositories.saju_webapi import ShinhanSajuWebApi

from saju_rag.core.infra.zenrows import get_zenrows_client


class BaseContainer(DeclarativeContainer):
    config: Settings = providers.Configuration()

    # infra
    zenrows_client = providers.Resource(
        get_zenrows_client, api_key=config.zenrows_api_key
    )
    chat_gpt_client = providers.Resource(ChatGptClient, api_key=config.openai_api_key)

    # repository
    saju_web_api_repository = providers.Factory(
        ShinhanSajuWebApi, zenrows_client=zenrows_client, host=config.shinhan_saju_host
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
    )

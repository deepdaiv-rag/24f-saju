from dependency_injector.wiring import Provide, inject

from saju_rag.core.usecase.extract_saju_usecase import ExtractSajuUseCase
from saju_rag.core.usecase.answer_with_external_info_usecase import (
    AnswerWithExternalInfoUsecase,
)
from saju_rag.core.entity.request_entity import SajuRequest

from saju_rag.di.config import Settings
from saju_rag.di.base import BaseContainer


async def init():
    container = BaseContainer()
    container.wire(modules=[__name__])
    config = Settings()
    container.config.from_pydantic(config)
    container.init_resources()
    print("container initialized")


@inject
async def extract_saju(
    request: SajuRequest,
    extract_saju_usecase: ExtractSajuUseCase = Provide[
        BaseContainer.gpt_extract_saju_usecase
    ],
) -> SajuRequest:
    request = await extract_saju_usecase.execute(request)
    return request


@inject
async def chat_with_saju(
    request: SajuRequest,
    answer_with_external_info_usecase: AnswerWithExternalInfoUsecase = Provide[
        BaseContainer.gpt_answer_with_external_info_usecase
    ],
) -> str:
    result = await answer_with_external_info_usecase.execute(request)
    return result


if __name__ == "__main__":
    pass

from fastapi import (
    APIRouter,
    HTTPException,
    Response,
    Request,
    Security,
)
from loguru import logger
from starlette import status
from tortoise import exceptions
from typing import (
    Any,
    List,
    Optional,
)

from app.promotion import models, schemas
from app.utils.pydantic_utils import filter_none_fields


router = APIRouter()


@router.get(
    path="/campaigns"
)
async def list_campaigns() -> List[schemas.CampaignResponse]:
    try:
        campaigns = await models.Campaign.all()
        return campaigns
    except Exception as e:
        logger.error(f"failed to list campaigns. error: {e}")
        raise HTTPException(
            detail="internal server error",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.get(
    path="/campaigns/{campaign_id}"
)
async def get_campaign(
    campaign_id: int,
) -> schemas.CampaignResponse:
    try:
        campaign = await models.Campaign.get(id=campaign_id)
        return campaign
    except exceptions.DoesNotExist:
        raise HTTPException(
            detail="not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        logger.error(f"failed to get a campaign. campaign_id: {campaign_id}. error: {e}")
        raise HTTPException(
            detail="internal server error",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.post(
    path="/campaigns"
)
async def create_campaign(
    payload: schemas.CampaignCreate,
) -> schemas.CampaignResponse:
    try:
        payload_as_dict = await filter_none_fields(payload.dict())
        campaign = await models.Campaign.create(**payload_as_dict)
        return campaign
    except Exception as e:
        logger.error(f"failed to create a new campaign. error: {e}")
        raise HTTPException(
            detail="internal server error",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.put(
    path="/campaigns/{campaign_id}"
)
async def update_campaign(
    campaign_id: int,
    payload: schemas.CampaignUpdate,
) -> Optional[schemas.CampaignResponse]:
    try:
        campaign = await models.Campaign.get(id=campaign_id)
    except exceptions.DoesNotExist:
        raise HTTPException(
            detail="not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        logger.error(f"failed to get a campaign. campaign_id: {campaign_id}. error: {e}")
        raise HTTPException(
            detail="internal server error",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    
    if campaign.status not in [
        models.ValidCampaignStatus.DRAFT,
        models.ValidCampaignStatus.WAITING,
    ]:
        raise HTTPException(
            detail="can not update",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    try:
        payload_as_dict = await filter_none_fields(payload.dict())
        await models.Campaign.get(id=campaign_id).update(**payload_as_dict)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        logger.error(f"failed to update new campaign. error: {e}")
        raise HTTPException(
            detail="internal server error",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.get(
    path="/campaigns/{campaign_id}/actions"
)
async def action_campaign(
    campaign_id: int,
    action_type: str,
) -> Any:
    campaign = await models.Campaign.get(id=campaign_id)
    if not campaign:
        raise HTTPException(
            detail="campaign is not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    
    action_type = action_type.lower()
    if action_type == "start":
        if campaign.status == models.ValidCampaignStatus.DRAFT:
            campaign.status = models.ValidCampaignStatus.WAITING
            await campaign.save()
            return Response(
                detail="start successfully",
                status_code=status.HTTP_200_OK,
            )
        else:
            raise HTTPException(
                detail="failed to start",
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
            )
    elif action_type == "pause":
        if campaign.status in [models.ValidCampaignStatus.WAITING,
                               models.ValidCampaignStatus.RUNNING]:
            campaign.status = models.ValidCampaignStatus.PAUSE
            await campaign.save()
            return Response(
                detail="pause successfully",
                status_code=status.HTTP_200_OK,
            )
        else:
            raise HTTPException(
                detail="failed to pause",
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
            )
    elif action_type == "resume":
        if campaign.status == models.ValidCampaignStatus.PAUSE:
            campaign.status = models.ValidCampaignStatus.RUNNING
            await campaign.save()
            return Response(
                detail="pause successfully",
                status_code=status.HTTP_200_OK,
            )
        else:
            raise HTTPException(
                detail="failed to pause",
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
            )
    else:
        raise HTTPException(
            detail="invalid action",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

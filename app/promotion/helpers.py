from datetime import datetime
from loguru import logger

from app.promotion import models


async def is_match_condition(
        message: dict, 
        condition: models.Condition, 
        campaign: models.Campaign
) -> bool:
    logger.debug(f"-----> message: {message}")
    logger.debug(f"-----> condition: {condition.id}")
    if condition.type == models.ValidConditionType.EVENT:
        condition_value = condition.value
        message_value = message.get("action_type")

        if condition.value_type == models.ValidConditionValueType.INT:
            condition_value = int(condition_value)
            message_value = int(message_value)
        elif condition.value_type == models.ValidConditionValueType.FLOAT:
            condition_value = float(condition_value)
            message_value = float(message_value)
        else:
            condition_value = str(condition_value)
            message_value = str(message_value)

        if condition_value == message_value:
            return True
    else:
        logger.warning(f"condition type is not supported. type: {condition.type}")
    return False


async def process_result(
        message: dict, 
        result: models.Result, 
        campaign: models.Campaign
) -> None:
    user_id = message.get('user_id')
    logger.debug("process result. "
                    f"user_id: {user_id}. "
                    f"result_id: {result.id}. "
                    f"campaign_id: {campaign.id}. "
                )
    
    if result.type == models.ValidResultType.VOUCHER:
        if campaign.total_vouchers < 1:
            logger.warning(f"there is no voucher left. campaign_id: {campaign.id}")
        
        claimed_voucher = await models.Voucher.filter(
            campaign=campaign,
            user_id=user_id,
        ).first()
        if claimed_voucher:
            logger.warning("user was claimed this campaign's voucher. "
                    f"user_id: {user_id}. "
                    f"claimed_voucher_id: {claimed_voucher.id}. "
                    f"campaign_id: {campaign.id}. "
                )
            return

        create_payload = {}
        if campaign.end_at:
            create_payload["expired_at"] = campaign.end_at
        create_payload["campaign"] = campaign
        create_payload["user_id"] = message.get("user_id")
        
        value = result.value
        if result.value_unit == models.ValidResultValueUnit.NUMBER:
            create_payload["value"] = float(value)
            create_payload["type"] = models.ValidVoucherType.DIRECT_DISCOUNT
            create_payload["value_unit"] = models.ValidVoucherValueUnit.NUMBER
        elif models.ValidResultValueUnit.PERCENT:
            create_payload["value"] = float(value)
            create_payload["type"] = models.ValidVoucherType.DIRECT_DISCOUNT
            create_payload["value_unit"] = models.ValidVoucherValueUnit.PERCENT
        else:
            create_payload["value"] = str(value)
            create_payload["type"] = models.ValidVoucherType.GIFT
            create_payload["value_unit"] = models.ValidVoucherValueUnit.STRING

        voucher  = await models.Voucher.create(**create_payload)
        campaign.total_vouchers = campaign.total_vouchers - 1
        await campaign.save()
        logger.warning(f"********************** issue voucher. voucher: {voucher.id} **********************")
    elif result.type == models.ValidResultType.CASH:
        logger.warning("********************** change balance **********************")
    else:
        logger.error(f"this result type is not supported. type: {result.type}")

from telegram import Update
from telegram.ext import ContextTypes

from src.utils import message_is_poll, is_message_from_group_chat


async def _pass_checks(
    msg_with_poll, update, context
) -> bool:  # TODO async checks and move somewhere else
    # check reply msg exists
    if not msg_with_poll:
        await update.effective_message.reply_text(
            "You will record result by replying to my poll. Have you started the game by /game command?"
        )
        return False
    # check reply msg is from group chat
    if not is_message_from_group_chat(msg_with_poll):
        await update.effective_message.reply_text(
            "You can only save game in a group chat where other players can see the results."
        )
        return False
    # check reply msg is a poll
    if not message_is_poll(msg_with_poll):
        await update.effective_message.reply_text(
            "Please reply to a poll to stop and record results."
        )
        return False
    # check reply msg is from the bot
    if msg_with_poll.from_user.id != context.bot.id:
        await update.effective_message.reply_text(
            f"Please reply to poll created by me @{context.bot.username}."
        )
        return False
    # check user is creator of the poll
    if (
        update.effective_user.id
        != context.bot_data[msg_with_poll.poll.id]["creator_id"]
    ):
        await update.effective_message.reply_text(
            f"You are not the creator of the game! "
            f"Only @{context.bot_data[msg_with_poll.poll.id]['creator_username']} can stop this poll."
        )
        return False
    # check the poll is in the same chat as the reply msg
    if update.effective_chat.id != context.bot_data[msg_with_poll.poll.id]["chat_id"]:
        await update.effective_message.reply_text(
            f"You can only save game in a group chat where other players can see the results."
        )
        return False

    return True


async def save(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Saves a game
    Replying /save to the poll message (created by the bot) stops the poll
    It can only be done by the creator of the poll
    Save poll results
    """

    msg_with_poll = (
        update.effective_message.reply_to_message
    )  # get a poll from reply message
    if await _pass_checks(msg_with_poll, update, context):
        await context.bot.stop_poll(update.effective_chat.id, msg_with_poll.id)
        poll_results = context.bot_data[msg_with_poll.poll.id]["results"]
        await update.effective_message.reply_text(
            "Poll stopped. Results: {}".format(poll_results)
        )
    else:
        await update.effective_message.reply_text(
            "Something went wrong. Can't process your request."
        )
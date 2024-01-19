from .CotConfig import CotConfig
from .message import compose_message
from .SocketConnection import SocketConnection


def push_cot(cot_config: CotConfig, client_address: str, client_port: int = 4242):
    """
    Push cursor on target message to client. For cot messages with attachments,
    see `CotServer.push_cot`.

    :param cot_config: cursor on target message information
    :param client_address: cot destination address
    :param client_port: cot destination port
    """
    # Validate config
    if len(cot_config.attachment_paths) > 0:
        raise ValueError(
            "Pushing cursor on target messages with attachments requires a "
            "file server to serve attachments. Please use `CotServer.push_cot` "
            "instead"
        )

    # Compose message
    message = compose_message(cot_config)

    # Send message
    with SocketConnection(client_address, client_port) as socket_connection:
        socket_connection.send(message)

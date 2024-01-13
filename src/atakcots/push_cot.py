
from .CotConfig import CotConfig
from .message import compose_message
from .SocketConnection import SocketConnection


def push_cot(cot_config: CotConfig, client_hostname: str, client_port: int):
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
    with SocketConnection(client_hostname, client_port) as socket_connection:
        socket_connection.send(message)
"""ZeroMQ REQ
"""
import asyncio
import logging
import zmq
#-
import aiozmq
import async_timeout

class MessageBrokerClient():
    """ZeroMQ REQ
    """
    SOCKET_READ_TIMEOUT = 10000 # msecs

    server_url = None
    socket = None

    read_timeout = None
    retries = 3

    socket_task = None

    logger = None
    running = None

    def __init__(self, server_url):
        self.server_url = server_url
        self.logger = logging.getLogger(type(self).__name__)
        self.running = True
        self.read_timeout = self.SOCKET_READ_TIMEOUT / 1000.0


    async def start(self):
        """Start connection
        """
        await self._reconnect()


    async def _reconnect(self):
        """ Connect or reconnect to REP server.
        """
        if self.socket:
            self.socket.close()

        self.socket = await aiozmq.create_zmq_stream(zmq.REQ)

        self.logger.debug('Connecting to server at %s', self.server_url)
        await self.socket.transport.connect(self.server_url)


    async def send(self, message, timeout=None, retries=None):
        """ Send request to server and get reply by hook or crook.

        Takes ownership of request message and destroys it when sent.
        Returns the reply message or None if there was no reply.
        """
        self.logger.debug('Send request to server')

        if self.socket is None:
            await self._reconnect()

        payload = [message]

        if retries is None:
            retries = self.retries
        while self.running and retries > 0:
            self.socket.write(payload)
            try:
                with async_timeout.timeout(timeout or self.read_timeout):
                    self.socket_task = asyncio.ensure_future(
                            self.socket.read())

                    message = await self.socket_task

                self.logger.debug('Received reply')

                return message
            except asyncio.TimeoutError:
                retries -= 1
                self.logger.warning('No reply, reconnecting..')
                await self._reconnect()
                self.logger.warning('After reconnecting..')
            except asyncio.CancelledError:
                retries -= 1


    def stop(self):
        """Disconnect
        """
        self.running = False
        if self.socket_task is not None:
            self.socket_task.cancel()


    async def destroy(self, *args):
        """Cleanup
        """
        if self.socket_task is not None:
            try:
                await self.socket_task
            except asyncio.CancelledError:
                pass

        if self.socket:
            self.socket.close()

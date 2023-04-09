"""ZeroMQ REP server
"""
import asyncio
import logging
import zmq
#-
import aiozmq

class MessageBrokerServer():
    """ZeroMQ REP Server
    """
    url = None
    socket = None
    on_request = None
    socket_task = None

    def __init__(self, url):
        self.url = url

        self.logger = logging.getLogger(type(self).__name__)
        self.running = True


    async def start(self):
        """Start the server
        """
        self.socket = await aiozmq.create_zmq_stream(zmq.REP)
        await self.socket.transport.bind(self.url)

        while self.running:
            self.socket_task = asyncio.ensure_future(self.socket.read())

            try:
                message = await self.socket_task
            except asyncio.CancelledError:
                continue

            if callable(self.on_request):
                await self.on_request(message) # pylint:disable=not-callable


    def stop(self):
        """Stop listening
        """
        self.running = False
        self.socket_task.cancel()


    async def destroy(self):
        """Cleanup
        """
        self.socket.close()


    async def send(self, message):
        """Send the reply
        """
        self.socket.write([message])

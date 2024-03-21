from .stream_process_thread import StreamProcessorThread

class StreamProcessManager:
    """
    This class is responsible for managing the stream processor thread.
    
    It holds a reference to the stream processor thread as a class variable and provides methods to start and stop the thread."""

    stream_processor: StreamProcessorThread = None

    def set_stream_processor(self):
        """
        Sets the stream processor thread.
        
        Args:
            None
        
        Returns:
            None"""
        if not self.__class__.stream_processor:
            self.__class__.stream_processor = StreamProcessorThread()

    def get_stream_processor(self):
        """
        Gets the stream processor thread.
        
        Args:
            None
            
        Returns:
            StreamProcessorThread: The stream processor thread."""
        return self.__class__.stream_processor
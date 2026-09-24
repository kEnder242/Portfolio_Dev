async def get_stream_dump(self):
    self.archive.call_tool("get_stream_dump", arguments={})
    raise
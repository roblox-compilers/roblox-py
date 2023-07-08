async def async_with():
    with open('test.txt') as f:
        contents = await f.read()
        print(contents)
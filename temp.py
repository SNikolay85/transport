import asyncio


async def foo():
    return 42

def ggg():
    df_1 = asyncio.run(foo())
    df_2 = asyncio.run(foo())
    return df_1, df_2

if __name__ == '__main__':
    print(ggg())
    #print(asyncio.run(ggg()))

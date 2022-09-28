from pysint import Pysint
import asyncio


async def main():
    await Pysint.ascii()
    await Pysint.command_input()


if __name__ == "__main__":
    asyncio.run(main())
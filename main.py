from pysint import Pysint
import asyncio

# Made by Shell

async def main():
    await Pysint.ascii()
    await Pysint.command_input()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
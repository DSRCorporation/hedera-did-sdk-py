import asyncio
from typing import Any

from hedera import Client, PrivateKey, Query, Transaction, TransactionReceipt


async def sign_hcs_transaction_async(transaction: Transaction, signing_keys: list[PrivateKey]) -> Transaction:
    def sign_transaction():
        signed_transaction = transaction
        for signing_key in signing_keys:
            signed_transaction = signed_transaction.sign(signing_key)
        return signed_transaction

    signing_task = asyncio.create_task(asyncio.to_thread(sign_transaction))
    await signing_task

    return signing_task.result()


async def execute_hcs_transaction_async(transaction: Transaction, client: Client) -> TransactionReceipt:
    def execute_transaction():
        transaction_response = transaction.execute(client)
        return transaction_response.getReceipt(client)

    execution_task = asyncio.create_task(asyncio.to_thread(execute_transaction))
    await execution_task

    return execution_task.result()


async def execute_hcs_query_async(query: Query, client: Client) -> Any:
    query_task = asyncio.create_task(asyncio.to_thread(lambda: query.execute(client)))
    await query_task
    return query_task.result()

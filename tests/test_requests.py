


# def test_repository_can_save_a_batch(session):
#     batch = model.Batch("batch1", "RUSTY-SOAPDISH", 100, eta=None)
#     repo = repository.SqlAlchemyRepository(session) repo.add(batch) 
#     session.commit() 
#         rows = list(session.execute(
#     'SELECT reference, sku, _purchased_quantity, eta FROM "batches"'  ))
#         assert rows == [("batch1", "RUSTY-SOAPDISH", 100, None)]
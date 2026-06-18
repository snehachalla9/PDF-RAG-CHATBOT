def retrieve_documents(
    db,
    query,
    k
):

    return db.similarity_search(
        query,
        k=k
    )
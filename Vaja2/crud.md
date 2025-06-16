# Implementacija CRUD

CRUD metode implementiramo s podobnimi zahtevami. Ali metoda potrebuje vhodni podatek? kaj mora storiti podatkovna baza ter kaj moramo dobiti kot odgovor?

```python
    async def create_item(item: ItemCreate, session: AsyncSession = Depends(get_session)): # Ustvarimo asinhrono funkcijo, pošljemo parametre ki ustrezajo modelu, 
    db_item = ItemModel(name=item.name, description=item.description) # Ustvarimo model, ki ustreza podatkovni bazi
    session.add(db_item) # Dodamo trenutni element v čakalno vrsto za bazo
    await session.commit() # Zapišemno v bazo
    await session.refresh(db_item) # Vrnemo novo stanje
    return db_item
```
Po podobnem principu lahko pridobimo samo en zapis v podatkovni bazi.
```python
      @app.get("/items/{item_id}", response_model=ItemRead) 
      @version(1)
      async def read_item(item_id: int, session: AsyncSession = Depends(get_session)): # Ustvarimo asinhrono funkcijo in kot parametere podamo ID Item, ki ga želimo izpisati
          result = await session.execute(select(ItemModel).where(ItemModel.id == item_id)) # Izvedemo SQL stavek, da poišče natančno ta zapis v podatkovni bazi
          item = result.scalar_one_or_none() 
          if not item: # Preverimo ali obstaja Item
              raise HTTPException(status_code=404, detail="Item not found")
          return item # Vrnemo iskani Item

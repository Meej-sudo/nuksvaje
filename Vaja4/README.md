# Vaja 4

Namen vaje je nadgradnja vaje 3 tako, da dokeriziramo aplikacija iz prve in druge laboratorijske vaje.
Ko želimo zgraditi container svoje aplikacije se je potrebno vprašati naslednje stvari.
- Kateri image bomo vzeli kot osnovo.
- Katere direktorije potrebujemo znotraj containerja
- Katere datoteko moramo prekopirati v container
- Ali obstajajo odvisnosti, ki jih potrebujemo.
- Katere porte moramo izpostaviti
- Kateri ukaz se bo izvedel, ko zaženemo container.

## Primer

```dockerfile
# Use an official Python image
FROM python:3.11-slim

# Create app directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose FastAPI port
EXPOSE 8000

# Run the app using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```
1. Kot osnovo bomo vzeli python image saj smo načrtovali python aplikacijo.
2. V containerju bomo ustvarili direktorij /app
3. V ta direktorij bomo skopirali vse kar je v lokalnem direktoriju (opcija . .). Lahko bi poimensko specificirali datoteke.
4. Kopirali bomo requirements.txt ter z pip-om namestili vse potrebne python knjižnice.
5. Izpostavili bomo port 8000 na katerem bo aplikacija dosegljiva.
6. izvedli bomo ukaz ki zažene uvicorn strežnik.

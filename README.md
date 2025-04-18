# Projeto Django

Um pequeno projeto feito em django que controla um estoque de itens

---

## Instalação

1. **clone o projeto**
```bash
git clone git@github.com:asafe-fernandes/stockManager.git
cd stockManager/stockManager
```

2. **Faca o build to container**
```bash
docker buildx build -t stockmanager .
```

3. **Rode o container**
```bash
docker run -it -p 8000:8000 stockmanager
```

4. acesse o projeto pelo [link](http://http://127.0.0.1:8000/)

## Steps for Running Mental Health Consultation System with Gen AI

### 1. Installing
```shell
  pip install -r requirements.txt
```

### 2. Insert Model mental health to folder models

### 3. Running with uvicorn
```shell
  uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```


## API
```
POST [BASE_URL]/v1/generate
```
#### Request
```json
{
  "question": "I'm very burnout in my job, so in the future can posibility i have mental illness?"
}
```
#### Response
```json
{
    "question": "I'm very burnout in my job, so in the future can posibility i have mental illness?",
    "answer": "Yes! If you're thinking about asking for help or need support from someone else who's already dealing with your feelings or just want to let them know that they don't necessarily care, then this might be an excellent time opportunity to reach out towards some friends of yours on their journey together"
}
```

### Steps Running Evaluate Model
```shell
  python evaluate_model.py > evaluate.log
```

### Result Evaluate Model
```
Text: What is a panic attack?
Perplexity: 33.36

Text: How to manage stress?
Perplexity: 40.27
```


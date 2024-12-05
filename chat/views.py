from django.shortcuts import render
import requests



def chat_view(request):
    response = None
    if request.method == 'POST':
        user_question = request.POST.get('question')
        response = get_answer_from_api(user_question)
    
    return render(request, 'chat.html', {'response': response})

def get_answer_from_api(question):
    api_url = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"
    headers = {"Authorization": "Bearer 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"}
    context = [
        'Привет - Привет!!',
        'Дела - Хорошо'
    ]
    combined_context = " ".join(context)
    data = {
        "inputs": {
            "question": question,
            "context": combined_context
        }
    }
    
    response = requests.post(api_url, headers=headers, json=data)
    if response.status_code == 200:
        answer = response.json()
        return answer.get('answer', 'Ответ не найден.')
    else:
        return "Ошибка обращения к API"

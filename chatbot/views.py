import requests
from django.http import JsonResponse
from django.shortcuts import render
from .models import ChatHistory

# 从图片URL中提取狗狗品种
def get_breed_from_url(url):
    return url.split('/')[4]  # 获取品种名

# 获取狗狗图片，并处理可能的重复品种
def fetch_dog_images(num_dogs):
    images = []
    unique_breeds = set()  # 用于存储唯一品种

    while len(images) < num_dogs:
        # 获取缺少的狗狗图片
        response = requests.get(f"https://dog.ceo/api/breeds/image/random/{num_dogs - len(images)}")
        result = response.json()
        new_images = result['message']

        for img in new_images:
            breed = get_breed_from_url(img)  # 从URL中获取品种
            if breed not in unique_breeds:
                unique_breeds.add(breed)  # 添加到唯一品种集合
                images.append({"url": img, "breed": breed})

    return images

# 处理狗狗聊天机器人请求
def dog_chatbot(request):
    user_input = request.GET.get('input')  # 获取用户输入
    try:
        # 将输入转换为整数
        num_dogs = int(user_input)

        if 1 <= num_dogs <= 8:
            images = fetch_dog_images(num_dogs)  # 获取狗狗图片和品种

            # 保存聊天记录
            ChatHistory.objects.create(
                input=user_input,
                result=str([i['url'] for i in images]),
                is_valid=True
            )

            # 返回结果作为JsonResponse
            return JsonResponse({'images': images})

        else:
            raise ValueError  # 非法输入范围

    except (ValueError, TypeError):
        # 处理无效输入
        ChatHistory.objects.create(
            input=user_input,
            result="请输入介于 1 到 8 之间的任何数字",
            is_valid=False
        )

        return JsonResponse({'error': "请输入介于 1 到 8 之间的任何数字"})

    except Exception as e:
        # 捕获所有其他异常
        ChatHistory.objects.create(
            input=user_input,
            result=f"出现错误：{str(e)}",
            is_valid=False
        )

        return JsonResponse({'error': f"出现错误：{str(e)}"})

# 显示聊天机器人页面
def show_chatbot(request):
    return render(request, "dog_chatbot.html")  # 渲染模板


# 获取整个聊天历史记录
def get_chat_history(request):
    # 获取最近的100条记录，并按时间顺序排列
    history = ChatHistory.objects.order_by('-execution_time')[:100]

    # 构建JSON数据
    history_data = []
    for record in history:
        history_data.append({
            "input": record.input,
            "result": record.result
        })

    return JsonResponse({"history": history_data})

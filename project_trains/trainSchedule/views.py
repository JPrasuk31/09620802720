from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.utils import timezone
import requests

JOHNDOE_API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTA1Mzc3MDcsImNvbXBhbnlOYW1lIjoiUHJhc3VrIFRyYWluIENlbnRyYWwiLCJjbGllbnRJRCI6IjM0ZjkyN2U2LTZiZWYtNGYzNy1iMjFmLTRmZTkxZDYwMzg0ZSIsIm93bmVyTmFtZSI6IiIsIm93bmVyRW1haWwiOiIiLCJyb2xsTm8iOiIwOTYyMDgwMjcyMCJ9.v793lSjL8a1rurZ8WBoY9o6GY4hZB_AObBJ2sSXA2_0'
JOHNDOE_API_URL = 'http://20.244.56.144/train'

@require_GET
def train_schedule(request):
    try:
        # Fetch data from John Doe Railways API
        response = requests.get(JOHNDOE_API_URL, headers={'Authorization': f'Bearer {JOHNDOE_API_KEY}'}, params={'duration': 720})  # 12 hours in minutes

        # Check if the request was successful
        response.raise_for_status()

        # Parse and filter the response data
        train_schedule = []
        current_time = timezone.now()
        twelve_hours_later = current_time + timezone.timedelta(hours=12)

        for train in response.json().get(f"trains Authorization: Bearer {JOHNDOE_API_KEY}", []):
            departure_time = timezone.datetime.fromisoformat(train.get('departure_time'))
            if current_time <= departure_time <= twelve_hours_later:
                train_schedule.append(train)

        return JsonResponse(train_schedule, safe=False)

    except requests.exceptions.RequestException as e:
        print('Error fetching train schedule:', str(e))
        return JsonResponse({'error': 'Internal Server Error'}, status=500)
